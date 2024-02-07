# Runs the API service for entity extraction.

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from domain import Tokens
from entity.matcher import feed_entity_matchers, threshold_matcher_results
from entity.matcher_missing_token import MissingTokenEntityMatcher
from likelihood.likelihood import LikelihoodFunctionLogistic
from lookup.database_lookup import DatabaseBackedLookup
from nltk.tokenize import wordpunct_tokenize


class ExtractionRequest(BaseModel):
    text: str
    threshold: float


class ExtractionMatch(BaseModel):
    match: str
    probability: float
    start: int
    end: int


class ExtractionResponse(BaseModel):
    matches: List[ExtractionMatch]
    message: str


def tokenise_text(text: str) -> Tokens:
    """Tokenise the text into tokens and make each token lowercase."""

    tokens = wordpunct_tokenize(text.lowercase())


app = FastAPI()

# Initialise a lookup for reading and initialise the matcher
lookup = DatabaseBackedLookup("./data/full-database.db", False)
max_window = lookup.get_max_tokens()
likelihood = LikelihoodFunctionLogistic(10.0, 0.5)
matcher = MissingTokenEntityMatcher(lookup, max_window, likelihood)


@app.post("/")
async def root(req: ExtractionRequest) -> ExtractionResponse:

    # Parse the request
    threshold = int(req.threshold)

    # All entity matchers
    entity_matchers = {"matcher": matcher}

    # Tokenise the text
    tokens = tokenise_text(req.text)

    # Send the tokens to the entity matchers
    feed_entity_matchers(tokens, entity_matchers)

    # Retain results above threshold

    # Return the response
