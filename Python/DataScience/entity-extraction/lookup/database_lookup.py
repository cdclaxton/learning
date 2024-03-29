from collections import defaultdict
import os
import pickle
import sqlite3

from functools import lru_cache
import time
from typing import List, Optional, Set
from domain import (
    Tokens,
    assert_entity_id_valid,
    assert_token_valid,
    assert_tokens_valid,
)
from lookup.lookup import Lookup
from loguru import logger

# Database table names
ENTITY_ID_TO_TOKENS_TABLENAME = "EntityIdToTokens"
TOKEN_TO_ENTITY_ID_TABLENAME = "TokenToEntityID"
TOKEN_TO_ENTITY_IDS_TABLENAME = "TokenToEntityIDs"
MAX_TOKENS_TABLENAME = "MaxTokens"

# Database column names
ENTITY_ID_COLUMN = "entityId"
SET_ENTITY_IDS_COLUMN = "setEntityIds"
LIST_ENTITY_IDS_COLUMN = "listEntityIds"
TOKENS_COLUMN = "tokens"
TOKEN_COLUMN = "token"
MAX_TOKENS_COLUMN = "maxTokens"

# Token separator
TOKEN_SEPARATOR = " "

# Minimum number of entities for a token to be added to the fast cache
MIN_ENTITIES_FOR_CACHE = 10


def pickle_set(s: Set[int]) -> bytes:
    """Pickle a set for storage in the database."""
    assert type(s) == set
    return pickle.dumps(s)


def unpickle_set(b: bytes) -> Set[int]:
    """Unpickle a set from storage in the database."""
    assert type(b) == bytes
    return pickle.loads(b)


def pickle_list(l: List[int]) -> bytes:
    """Pickle a list for storage in the database."""
    assert type(l) == list
    return pickle.dumps(l)


def unpickle_list(b: bytes) -> List[int]:
    """Unpickle a list from storage in the database."""
    assert type(b) == bytes
    return pickle.loads(b)


class DatabaseBackedLookup(Lookup):
    """Database-backed entity to tokens lookup."""

    def __init__(self, filepath: str, load_mode: bool):
        assert type(filepath) == str
        assert type(load_mode) == bool

        self._filepath = filepath
        self._load_mode = load_mode
        self._conn: Optional[sqlite3.Connection] = None
        self._cursor: Optional[sqlite3.Cursor] = None

        # Number of times the add() method has been called since a database commit
        self._num_adds: int = 0

        # Maximum number of tokens for a single entity
        self._max_num_tokens: int = 0

        # Token to number of entities count
        self._token_to_count = defaultdict(int)

        # Initialise the database for loading or reading
        self._initialise_database()

    def _initialise_database(self):
        """Initialise the Sqlite database depending on the mode of operation."""

        if self._load_mode:
            self._initialise_load_mode()
        else:
            self._initialise_read_mode()

    def _table_exists(self, table_name: str) -> bool:
        """Does the table exist?"""
        assert type(table_name) == str

        res = self._cursor.execute(
            "SELECT name FROM sqlite_master WHERE name='" + table_name + "';"
        )
        return res.fetchone() is not None

    def _initialise_load_mode(self):
        """Initialise the database for load mode."""

        logger.info("Database in load mode")
        logger.info(f"Opening connection to database: {self._filepath}")

        # Check that the a file with the database filepath doesn't exist
        if os.path.exists(self._filepath):
            raise Exception(f"File already exists: {self._filepath}")

        # Open a connection to the database
        self._conn = sqlite3.connect(self._filepath)

        # Get a cursor
        self._cursor = self._conn.cursor()

        # Create the entity ID to tokens table
        self._cursor.execute(
            f"CREATE TABLE {ENTITY_ID_TO_TOKENS_TABLENAME}({ENTITY_ID_COLUMN}, {TOKENS_COLUMN});"
        )

        # Create the token to entity ID table
        self._cursor.execute(
            f"CREATE TABLE {TOKEN_TO_ENTITY_ID_TABLENAME}({TOKEN_COLUMN}, {ENTITY_ID_COLUMN});"
        )

        # Create the token to the set of entity IDs and list of entity IDs table
        self._cursor.execute(
            f"CREATE TABLE {TOKEN_TO_ENTITY_IDS_TABLENAME}({TOKEN_COLUMN}, {SET_ENTITY_IDS_COLUMN}, {LIST_ENTITY_IDS_COLUMN});"
        )

        # Create a table to hold the maximum number of tokens for a entity
        self._cursor.execute(
            f"CREATE TABLE {MAX_TOKENS_TABLENAME}({MAX_TOKENS_COLUMN});"
        )

    def _initialise_read_mode(self):
        """Initialise the database for reading."""

        logger.info("Database in read mode")
        logger.info(f"Opening connection to database: {self._filepath}")

        # Check a database file exists
        if not os.path.exists(self._filepath):
            raise Exception(f"Database doesn't exist: {self._filepath}")

        # Open a connection to the database
        self._conn = sqlite3.connect(self._filepath)

        # Get a cursor
        self._cursor = self._conn.cursor()

        # Check to see if the required tables exist
        if not self._table_exists(ENTITY_ID_TO_TOKENS_TABLENAME):
            raise Exception(
                f"Database doesn't contain table: {ENTITY_ID_TO_TOKENS_TABLENAME}"
            )

        if not self._table_exists(TOKEN_TO_ENTITY_ID_TABLENAME):
            raise Exception(
                f"Database doesn't contain table: {TOKEN_TO_ENTITY_ID_TABLENAME}"
            )

        # Get a cursor
        self._cursor = self._conn.cursor()

    def add(self, entity_id: int, tokens: Tokens) -> None:
        """Add an entity to the lookup."""

        assert_entity_id_valid(entity_id)
        assert_tokens_valid(tokens)

        for token in tokens:
            self._token_to_count[token] += 1

        # Add the entity to tokens mapping
        self._cursor.execute(
            f"INSERT INTO " + ENTITY_ID_TO_TOKENS_TABLENAME + " VALUES(?,?);",
            (entity_id, TOKEN_SEPARATOR.join(tokens)),
        )

        # Add the token to entity mapping
        for token in tokens:
            self._cursor.execute(
                f"INSERT INTO " + TOKEN_TO_ENTITY_ID_TABLENAME + " VALUES(?,?);",
                (token, entity_id),
            )

        # Update the maximum number of tokens for an entity
        self._max_num_tokens = max(self._max_num_tokens, len(tokens))

        # One more entity and its tokens have been added
        self._num_adds += 1

        # Commit the inserts if the insert threshold has been met
        if self._num_adds == 1000:
            self._conn.commit()
            self._num_adds = 0

    def finalise(self) -> None:
        """Finalise the entries in the lookup."""

        # Commit any remaining insert operations
        if self._num_adds > 0:
            self._conn.commit()

        # Write the maximum number of tokens for an entity
        self._cursor.execute(
            f"INSERT INTO " + MAX_TOKENS_TABLENAME + " VALUES(?);",
            (self._max_num_tokens,),
        )

        start_time = time.time()

        # Add an index to the tables
        self._cursor.execute(
            "CREATE INDEX index1 ON "
            + ENTITY_ID_TO_TOKENS_TABLENAME
            + " ( "
            + ENTITY_ID_COLUMN
            + ");"
        )

        self._cursor.execute(
            "CREATE INDEX index2 ON "
            + TOKEN_TO_ENTITY_ID_TABLENAME
            + " ( "
            + TOKEN_COLUMN
            + ");"
        )

        self._conn.commit()

        logger.info(
            f"Time taken to create the indices: {time.time() - start_time} seconds"
        )

        # Populate the token to entity IDs table
        start_time = time.time()
        self._build_token_to_entity_ids_table()
        logger.info(
            f"Time taken to build the fast token to entity IDs lookup: {time.time() - start_time} seconds"
        )

        # Create an index on the token to entity IDs table
        start_time = time.time()
        self._cursor.execute(
            "CREATE INDEX index3 ON "
            + TOKEN_TO_ENTITY_IDS_TABLENAME
            + " ( "
            + TOKEN_COLUMN
            + ");"
        )

        self._conn.commit()
        logger.info(
            f"Time taken to create the token-to-entity IDs index: {time.time() - start_time} seconds"
        )

    def _add_token_to_entities(self, token: str, set_entities: Set[int]) -> None:
        """Add a token to entity IDs mapping for fast lookup."""

        assert_token_valid(token)
        assert type(set_entities) == set

        list_entities = list(set_entities)

        self._cursor.execute(
            f"INSERT INTO " + TOKEN_TO_ENTITY_IDS_TABLENAME + " VALUES(?,?,?);",
            (token, pickle_set(set_entities), pickle_list(list_entities)),
        )
        self._num_adds += 1

        # Commit the inserts if the insert threshold has been met
        if self._num_adds == 1000:
            self._conn.commit()
            self._num_adds = 0

    def _build_token_to_entity_ids_table(self) -> None:
        """Build a token to entity IDs table for tokens with lots of entity IDs."""

        total_tokens = len(self._token_to_count)
        logger.info(
            f"Building the token to entity IDs fast lookup ({total_tokens} tokens)"
        )

        self._num_adds = 0
        num_tokens_processed = 0
        num_additions = 0

        for token, count in self._token_to_count.items():
            num_tokens_processed += 1

            if count >= MIN_ENTITIES_FOR_CACHE:
                # Get the entities for the token and add to the dedicated lookup
                # table
                entities = self._entity_ids_for_token_slow(token)
                self._add_token_to_entities(token, entities)
                num_additions += 1

            if num_tokens_processed % 10000 == 0:
                percentage_processed = 100.0 * num_tokens_processed / total_tokens
                percentage_added = 100 * num_additions / num_tokens_processed
                logger.info(
                    f"Processed {num_tokens_processed} tokens ({percentage_processed} %), {num_additions} ({percentage_added :.4f} %) added for fast lookup"
                )

        logger.info(
            f"There are {total_tokens} unique tokens, {num_additions} ({100 * num_additions/total_tokens :.4f} %) added for fast lookup"
        )

        if self._num_adds > 0:
            self._conn.commit()

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    @lru_cache(maxsize=100000)
    def tokens_for_entity(self, entity_id: int) -> Optional[Tokens]:
        """Get tokens for an entity given its ID."""

        assert_entity_id_valid(entity_id)

        res = self._cursor.execute(
            "SELECT "
            + TOKENS_COLUMN
            + " FROM "
            + ENTITY_ID_TO_TOKENS_TABLENAME
            + " WHERE "
            + ENTITY_ID_COLUMN
            + "=?;",
            (entity_id,),
        )

        result = res.fetchall()

        if len(result) == 0:
            return None

        assert len(result) == 1

        return result[0][0].split(TOKEN_SEPARATOR)

    @lru_cache(maxsize=100)
    def _entity_ids_for_token_slow(self, token: str) -> Optional[Set[int]]:
        """Get the entity IDs for a given token without using the dedicated table."""

        res = self._cursor.execute(
            "SELECT "
            + ENTITY_ID_COLUMN
            + " FROM "
            + TOKEN_TO_ENTITY_ID_TABLENAME
            + " WHERE "
            + TOKEN_COLUMN
            + "=?",
            (token,),
        )

        result = res.fetchall()

        if len(result) == 0:
            return None

        return {ri[0] for ri in result}

    @lru_cache(maxsize=100)
    def _entity_ids_for_token_list_slow(self, token: str) -> Optional[Set[int]]:
        """Get the entity IDs for a given token without using the dedicated table."""

        res = self._cursor.execute(
            "SELECT "
            + ENTITY_ID_COLUMN
            + " FROM "
            + TOKEN_TO_ENTITY_ID_TABLENAME
            + " WHERE "
            + TOKEN_COLUMN
            + "=?",
            (token,),
        )

        result = res.fetchall()

        if len(result) == 0:
            return None

        return [ri[0] for ri in result]

    @lru_cache(maxsize=100)
    def entity_ids_for_token(self, token: str) -> Optional[Set[int]]:
        """Get the entity IDs for a given token."""

        assert_token_valid(token)

        # Check to see if the token is in the token-to-entity IDs table
        res = self._cursor.execute(
            "SELECT "
            + SET_ENTITY_IDS_COLUMN
            + " FROM "
            + TOKEN_TO_ENTITY_IDS_TABLENAME
            + " WHERE "
            + TOKEN_COLUMN
            + "=?",
            (token,),
        )

        result = res.fetchone()

        # Unpickle and return a set if there is an entry
        if result is not None:
            return unpickle_set(result[0])

        return self._entity_ids_for_token_slow(token)

    @lru_cache(maxsize=100)
    def entity_ids_for_token_list(self, token: str) -> Optional[List[int]]:
        """Get the entity IDs as a list for a given token."""

        assert_token_valid(token)

        # Check to see if the token is in the token-to-entity IDs table
        res = self._cursor.execute(
            "SELECT "
            + LIST_ENTITY_IDS_COLUMN
            + " FROM "
            + TOKEN_TO_ENTITY_IDS_TABLENAME
            + " WHERE "
            + TOKEN_COLUMN
            + "=?",
            (token,),
        )

        result = res.fetchone()

        # Unpickle and return a set if there is an entry
        if result is not None:
            return unpickle_list(result[0])

        return self._entity_ids_for_token_list_slow(token)

    def entity_ids_for_token_string(self, token: str) -> Optional[str]:
        """Get the entity IDs as a string for a given token."""

        raise Exception("unimplemented")

    def _debug(self):
        """Create debug output (only for small databases)."""

        res = self._cursor.execute("SELECT name FROM sqlite_master;")
        while True:
            result = res.fetchone()
            if result is None:
                break
            print(f"Table: {result[0]}")

        print("")

        print("Entity ID to tokens:")
        res = self._cursor.execute("SELECT * FROM " + ENTITY_ID_TO_TOKENS_TABLENAME)
        print(res.fetchall())
        print("")

        print("Token to entity ID:")
        res = self._cursor.execute("SELECT * FROM " + TOKEN_TO_ENTITY_ID_TABLENAME)
        print(res.fetchall())
        print("")

        print("Token to entity IDs:")
        res = self._cursor.execute(
            "SELECT " + TOKEN_COLUMN + " FROM " + TOKEN_TO_ENTITY_IDS_TABLENAME
        )
        print(res.fetchall())

    def matching_entries(self, tokens: Tokens) -> Optional[Set[int]]:
        """Find the matching entities in the lookup given the tokens."""

        assert type(tokens) == list
        assert all([type(t) == str for t in tokens])
        assert len(tokens) > 0

        # Get the entities for each token
        for idx, t in enumerate(tokens):
            es = self.entity_ids_for_token(t)

            if es is None:
                return None

            if idx == 0:
                entity_ids = es
            else:
                entity_ids = entity_ids.intersection(es)

            # No entries match, so there's no point looking at any further tokens
            if len(entity_ids) == 0:
                return None

        return entity_ids

    def max_number_tokens_for_entity(self) -> int:
        """Get the maximum number of tokens for an entity."""

        res = self._cursor.execute(
            "SELECT " + MAX_TOKENS_COLUMN + " FROM " + MAX_TOKENS_TABLENAME
        )
        num = res.fetchone()[0]
        assert type(num) == int

        return num

    def num_tokens_for_entity(self, entity_id: int) -> Optional[int]:
        """Number of tokens for an entity."""

        tokens = self.tokens_for_entity(entity_id)
        if tokens is None:
            return None

        return len(tokens)

    def __repr__(self):
        return f"DatabaseBackedLookup(filepath={self._filepath})"

    def __str__(self):
        return self.__repr__()
