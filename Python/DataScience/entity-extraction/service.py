# Runs the API service for entity extraction.

from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from domain import Tokens, assert_tokens_valid
from entity.matcher import (
    ProbabilisticMatch,
    feed_entity_matchers,
    most_likely_matches,
)
from entity.matcher_generic import GenericEntityMatcher
from entity.matcher_missing_token import MissingTokenEntityMatcher
from likelihood.likelihood import LikelihoodFunctionLogistic
from likelihood.likelihood_add_remove import make_likelihood_symmetric
from lookup.database_lookup import DatabaseBackedLookup
from nltk.tokenize import wordpunct_tokenize
from loguru import logger

import os
import string
import uvicorn

from lookup.lmdb_lookup import LmdbLookup

app = FastAPI()


class ExtractionRequest(BaseModel):
    text: str
    threshold: float
    min_tokens_to_check: int


class ExtractionMatch(BaseModel):
    entity_id: str  # Entity ID
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


def tokenise_text(text: str) -> Optional[Tokens]:
    """Tokenise the text into tokens and make each token lowercase."""

    if type(text) != str:
        return None

    if len(text) == 0:
        return None

    punct = set(string.punctuation)

    def only_punctuation(text: str) -> bool:
        """Is the text composed of just punctuation?"""
        return all([t in punct for t in text])

    # Tokenise the lowercase version of the text
    tokens = wordpunct_tokenize(text.lower())

    # Remove tokens that are only punctuation
    return [t for t in tokens if not only_punctuation(t)]


def probability_match_to_extraction_match(
    prob_match: ProbabilisticMatch, tokens: Tokens
) -> ExtractionMatch:
    """Convert a ProbabilisticMatch to an ExtractionMatch."""

    assert type(prob_match) == ProbabilisticMatch
    assert_tokens_valid(tokens)

    # Get the entity from the lookup
    entity = " ".join(lookup.tokens_for_entity(prob_match.entity_id))

    assert prob_match.start >= 0 and prob_match.start < len(tokens)
    assert prob_match.end >= 0 and prob_match.end < len(tokens)

    return ExtractionMatch(
        entity_id=prob_match.entity_id,
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

    # Make the entity matcher
    # matcher = MissingTokenEntityMatcher(
    #     lookup=lookup,
    #     max_window_width=max_window,
    #     likelihood_function=likelihood,
    #     min_probability=req.threshold,
    #     min_tokens_to_check=req.min_tokens_to_check,
    # )

    matcher = GenericEntityMatcher(
        lookup=lookup,
        likelihood=likelihood_symmetric,
        min_window=req.min_tokens_to_check,
        max_window=max_window,
        min_probability=req.threshold,
    )

    # All entity matchers
    entity_matchers = {"matcher": matcher}

    # Tokenise the text
    tokens = tokenise_text(req.text)
    logger.debug(
        f"Request: tokens={tokens}, threshold={req.threshold}, min tokens={req.min_tokens_to_check}"
    )

    # Send the tokens to the entity matchers
    feed_entity_matchers(tokens, entity_matchers)

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
    lmdb_folder: str, sqlite_filepath: str, entities: List[str]
) -> None:
    """Make a test database."""

    assert type(lmdb_folder) == str
    assert type(sqlite_filepath) == str
    assert type(entities) == list

    # Make a database-backed lookup
    # lookup = DatabaseBackedLookup(database_filepath, True)
    lookup = LmdbLookup(lmdb_folder, True, sqlite_filepath)

    # Add all of the entities
    for idx, ent in enumerate(entities):
        entity_id = f"e-{idx}"
        tokens = tokenise_text(ent)
        lookup.add(entity_id, tokens)

    # Finalise and close the lookup
    lookup.finalise()
    lookup.close()


if __name__ == "__main__":

    # Database file
    # database_filepath = "./data/full-database.db"

    lmdb_folder = "./data/lmdb"
    sqlite_database = "./data/sqlite.db"

    # If the database doesn't exist, make a test database for demo purposes.
    # Note that if entities are added below, be sure to delete the existing
    # database using:
    # rm ./data/full-database.db
    if not os.path.exists(lmdb_folder):
        logger.info(f"Making a test database as {lmdb_folder} doesn't exist")
        entities = [
            "78 Straight Street London",
            "6 The Walk London",
            "10 The Mews Birmingham",
            "12 The Mews Birmingham",
        ]
        make_test_database(lmdb_folder, sqlite_database, entities)

    # Initialise a lookup for reading and initialise the matcher
    # lookup = DatabaseBackedLookup(database_filepath, False)
    lookup = LmdbLookup(lmdb_folder, False)

    max_window = lookup.max_number_tokens_for_entity()
    logger.info(f"Maximum window size: {max_window}")

    # Make the logistic likelihood function
    logger.info("Instantiating the likelihood function")
    likelihood = LikelihoodFunctionLogistic(10.0, 0.5)
    likelihood_symmetric = make_likelihood_symmetric(0.2, 0.9, 0.5, 0.1, max_window)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
