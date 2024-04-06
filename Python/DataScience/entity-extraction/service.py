# Runs the API service for entity extraction.

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from domain import Tokens, assert_tokens_valid
from entity.matcher import (
    ProbabilisticMatch,
    most_likely_matches,
)
from entity.matcher_add_remove import EntityMatcherAddRemove
from likelihood.likelihood_add_remove import (
    make_likelihood_add_remove_symmetric,
)

from loguru import logger

import os
import uvicorn

from lookup.lmdb_lookup import LmdbLookup
from text.tokeniser import tokenise_text

app = FastAPI()


class ExtractionRequest(BaseModel):
    text: str = Field(description="Text to process")
    threshold: float
    min_tokens_to_check: int


class ExtractionMatch(BaseModel):
    entity_id: str  # External entity ID
    entity: str  # Entity tokens
    matched_text: str  # Text that matched the entity
    probability: float  # Probability of the match
    start: int  # Start index in the text
    end: int  # End index in the text


class ExtractionResponse(BaseModel):
    matches: List[ExtractionMatch]
    most_likely_matches: List[List[ExtractionMatch]]
    message: str
    num_matches: int


def probability_match_to_extraction_match(
    prob_match: ProbabilisticMatch, tokens: Tokens
) -> ExtractionMatch:
    """Convert a ProbabilisticMatch to an ExtractionMatch."""

    assert type(prob_match) == ProbabilisticMatch
    assert_tokens_valid(tokens)

    # Get the entity's tokens from the lookup
    entity_tokens = lookup.tokens_for_entity(prob_match.entity_id)
    assert entity_tokens is not None
    entity = " ".join(entity_tokens)

    assert prob_match.start >= 0 and prob_match.start < len(tokens)
    assert prob_match.end >= 0 and prob_match.end < len(tokens)

    # Look up the external entity ID given the internal entity ID
    external_entity_id = lookup.external_entity_id(prob_match.entity_id)
    assert external_entity_id is not None

    return ExtractionMatch(
        entity_id=external_entity_id,
        entity=entity,
        matched_text=" ".join(tokens[prob_match.start : prob_match.end + 1]),
        probability=prob_match.probability,
        start=prob_match.start,
        end=prob_match.end,
    )


def convert_matches(
    matches: List[ProbabilisticMatch], tokens: Tokens
) -> List[ExtractionMatch]:
    """Convert matches for returning via the API"""

    assert type(matches) == list
    assert_tokens_valid(tokens)

    return [
        probability_match_to_extraction_match(prob_match, tokens)
        for prob_match in matches
    ]


def convert_most_likely_matches(
    matches: List[List[ProbabilisticMatch]], tokens: Tokens
) -> List[List[ExtractionMatch]]:
    """Convert the list of list of probabilistic matches to extraction matches."""

    assert type(matches) == list
    return [convert_matches(m, tokens) for m in matches]


def error_response(message: str) -> ExtractionResponse:
    """Returns an ExtractionResponse for the error case."""

    assert type(message) == str
    return ExtractionResponse(
        matches=[],
        most_likely_matches=[],
        message=message,
        num_matches=0,
    )


@app.post("/")
async def root(req: ExtractionRequest) -> ExtractionResponse:

    # Check the request
    if req.threshold < 0.0 or req.threshold > 1.0:
        return error_response("invalid threshold")

    if len(req.text) == 0:
        return error_response("empty text")

    if req.min_tokens_to_check <= 0:
        return error_response("invalid minimum number of tokens to check")

    # Instantiate the entity matcher
    matcher = EntityMatcherAddRemove(
        lookup=lookup,
        likelihood=likelihood_symmetric,
        min_window=req.min_tokens_to_check,
        max_window=max_window,
        min_probability=req.threshold,
        max_entity_id=max_entity_id,
    )

    # Tokenise the text
    tokens = tokenise_text(req.text)
    assert tokens is not None
    logger.debug(
        f"Request: tokens={tokens}, threshold={req.threshold}, min tokens={req.min_tokens_to_check}"
    )

    # Send the tokens to the entity matcher
    for token in tokens:
        matcher.next_token(token)

    # Retain results above threshold
    matches = matcher.get_sorted_matches_above_threshold(req.threshold)

    if len(matches) == 0:
        return ExtractionResponse(
            matches=[], most_likely_matches=[], message="no matches", num_matches=0
        )

    # Find the most likely matches
    most_likely = most_likely_matches(matches)

    # Return the response
    return ExtractionResponse(
        matches=convert_matches(matches, tokens),
        most_likely_matches=convert_most_likely_matches(most_likely, tokens),
        message="success",
        num_matches=len(matches),
    )


def make_test_database(
    lmdb_folder: str,
    sqlite_filepath: str,
    token_count_filepath: str,
    entities: List[str],
) -> None:
    """Make a test database."""

    assert type(lmdb_folder) == str
    assert type(sqlite_filepath) == str
    assert type(token_count_filepath) == str
    assert type(entities) == list

    # Make a database-backed lookup
    lookup = LmdbLookup(lmdb_folder, True, sqlite_filepath, token_count_filepath)

    # Add all entities
    for idx, ent in enumerate(entities):
        tokens = tokenise_text(ent)
        assert tokens is not None

        external_entity_id = str(idx + 100)
        lookup.add(idx, external_entity_id, tokens)

    # Finalise and close the lookup
    lookup.finalise()
    lookup.close()


if __name__ == "__main__":

    # Locations of the databases
    lmdb_folder = "./data/lmdb"
    token_to_count_file = "./data/token-to-count.pickle"
    sqlite_database = "./data/sqlite.db"

    # If the database doesn't exist, make a test database for demo purposes.
    # Note that if entities are added below, be sure to delete the existing
    # database using:
    # rm -rf ./data/lmdb
    if not os.path.exists(lmdb_folder):
        logger.info(f"Making a test database as {lmdb_folder} doesn't exist")
        entities = [
            "78 Straight Street London",
            "6 The Walk London",
            "10 The Mews Birmingham",
            "12 The Mews Birmingham",
        ]
        make_test_database(lmdb_folder, sqlite_database, token_to_count_file, entities)

    # Initialise a lookup for reading and initialise the matcher
    lookup = LmdbLookup(lmdb_folder, False)

    max_window = lookup.max_number_tokens_for_entity()
    logger.info(f"Maximum window size: {max_window}")

    max_entity_id = lookup.max_entity_id()
    logger.info(f"Maximum entity ID: {max_entity_id}")

    # Make the likelihood function
    logger.info("Instantiating the likelihood function")
    likelihood_symmetric = make_likelihood_add_remove_symmetric(0.2, 0.9, 0.7, 0.1)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
