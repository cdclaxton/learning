from functools import lru_cache
import pickle
import lmdb
import os
import sqlite3

from typing import Any, Dict, List, Optional, Set
from loguru import logger
from domain import (
    Tokens,
    assert_external_entity_id_valid,
    assert_internal_entity_id_valid,
    assert_tokens_valid,
)
from lookup.lookup import Lookup

# Sqlite database table name and column names
TOKEN_TO_ENTITY_ID_TABLENAME = "TokenToEntityID"
ENTITY_ID_COLUMN = "entityId"
TOKEN_COLUMN = "token"

# LMDB map size in bytes
LMDB_MAP_SIZE = 1000 * 1000 * 1000 * 100

# The key-value structure is:
#
# E<entity ID> = <pickled list of tokens>
# T<token> = <pickled list of internal entity IDs>
# S<token> = <space separated string of internal entity IDs>
# M = <maximum number of tokens for an entity (across all entities)>
# N = <maximum internal entity ID>
# C<internal entity ID> = <number of tokens for the entity>
# I<internal entity ID> = <external entity ID>

# Key for the key-value pair for the maximum number of tokens for an entity
MAX_TOKENS_KEY = "M"

# Key for the maximum entity ID
MAX_ENTITY_ID_KEY = "N"

# Key for the mapping from an internal entity ID to an external entity ID
INT_TO_EXT_ENTITY_ID = "I"


def pickle_list(l: List[int]) -> bytes:
    """Pickle a list for storage in the database."""
    assert type(l) == list
    return pickle.dumps(l)


def unpickle_list(b: bytes) -> List[int]:
    """Unpickle a list from storage in the database."""
    assert type(b) == bytes
    return pickle.loads(b)


def pickle_list_str(l: List[str]) -> bytes:
    """Pickle a list of strings for storage in the database."""
    assert type(l) == list
    return pickle.dumps(l)


def unpickle_list_str(b: bytes) -> List[str]:
    """Unpickle a list of strings from storage in the database."""
    assert type(b) == bytes
    return pickle.loads(b)


def internal_entity_id_to_key(internal_entity_id: int) -> bytes:
    """Internal entity ID to key in the LMDB."""
    return f"E{internal_entity_id}".encode("ascii")


def token_to_key(token: str) -> bytes:
    """Token to key in the LMDB."""
    return f"T{token}".encode("ascii")


def token_to_string_key(token: str) -> bytes:
    """Token to key in the LMDB."""
    return f"S{token}".encode("ascii")


def internal_entity_id_to_token_count_key(internal_entity_id: int) -> bytes:
    """Internal entity ID to key in LMDB to retrieve the number of tokens."""
    return f"C{internal_entity_id}".encode("ascii")


def count_to_bytes(count: int) -> bytes:
    """Convert the token count to bytes."""
    assert count <= 255
    return count.to_bytes(length=2, byteorder="big")


def bytes_to_count(b: bytes) -> int:
    """Convert bytes to a token count."""
    return int.from_bytes(bytes=b, byteorder="big")


def internal_entity_to_external_key(internal_entity_id: int) -> bytes:
    """Key for the mapping from an internal entity ID to an external ID."""
    return f"I{internal_entity_id}".encode("ascii")


class LmdbLookup(Lookup):
    """A lookup backed by an LMDB."""

    def __init__(
        self,
        lmdb_folder: str,
        load_mode: bool,
        sqlite_filepath: Optional[str] = None,
        token_count_filepath: Optional[str] = None,
    ):
        assert type(lmdb_folder) == str
        assert type(load_mode) == bool
        assert sqlite_filepath is None or type(sqlite_filepath) == str
        assert token_count_filepath is None or type(token_count_filepath) == str

        self._lmdb_folder = lmdb_folder
        self._load_mode = load_mode
        self._token_to_count_filepath = token_count_filepath
        self._sqlite_filepath = sqlite_filepath

        # LMDB environment
        self._env: Any = None
        self._num_lmdb_adds: int = 0

        # Set of tokens (created during load mode)
        self._tokens: Set[str] = set()

        # Number of entities that have a given token
        self._token_to_count: Dict[str, int] = dict()

        # Maximum number of tokens for a single entity
        self._max_num_tokens: int = 0

        # Maximum entity ID
        self._max_entity_id: int = -1

        # Sqlite database connection and cursor for load mode
        self._conn: Optional[sqlite3.Connection] = None
        self._cursor: Optional[sqlite3.Cursor] = None
        self._num_adds: int = 0

        # Initialise the databse depending on the mode of operation
        if self._load_mode:
            self._initialise_load_mode()
        else:
            self._initialise_read_mode()

    def _initialise_load_mode(self):
        """Initialise two databases for loading."""

        logger.info("Lookup in load mode")

        self._initialise_lmdb_for_writing()
        self._initialise_sqlite_for_writing()

    def _initialise_read_mode(self):
        """Initialise the LMDB for reading."""

        logger.info("Lookup in read mode")

        self._env = lmdb.open(self._lmdb_folder, readonly=True)
        logger.debug(f"LMDB stats: {self._env.stat()}")

    def _initialise_lmdb_for_writing(self) -> None:
        """Initialise the LMDB for writing."""

        logger.info(f"Initialising the LMDB for writing in folder: {self._lmdb_folder}")

        # Open the LMDB environment for writing
        self._env = lmdb.open(
            self._lmdb_folder, map_size=LMDB_MAP_SIZE, sync=False, writemap=True
        )

    def _initialise_sqlite_for_writing(self) -> None:
        """Initialise the (temporary) Sqlite database for writing."""

        logger.info(
            f"Initialising the Sqlite database for writing at filepath: {self._sqlite_filepath}"
        )

        if self._sqlite_filepath is None:
            raise Exception("Sqlite filepath is None")

        # Check that the a file with the Sqlite database filepath doesn't exist
        if os.path.exists(self._sqlite_filepath):
            raise Exception(
                f"Sqlite database file already exists: {self._sqlite_filepath}"
            )

        # Open a connection to the database
        self._conn = sqlite3.connect(self._sqlite_filepath)

        # Get a cursor
        self._cursor = self._conn.cursor()

        # Create the token to entity ID table
        logger.info(f"Creating Sqlite table: {TOKEN_TO_ENTITY_ID_TABLENAME}")
        self._cursor.execute(
            f"CREATE TABLE {TOKEN_TO_ENTITY_ID_TABLENAME}({TOKEN_COLUMN}, {ENTITY_ID_COLUMN});"
        )

    def add(
        self, internal_entity_id: int, external_entity_id: str, tokens: Tokens
    ) -> None:
        """Add an entity to the lookup."""

        assert_internal_entity_id_valid(internal_entity_id)
        assert_external_entity_id_valid(external_entity_id)
        assert_tokens_valid(tokens)

        # Add the entity ID to tokens mapping to the LMDB
        self._add_to_lmdb(internal_entity_id, external_entity_id, tokens)

        # Add the token to entity ID to Sqlite
        self._add_to_sqlite(internal_entity_id, tokens)

        # Update the maximum number of tokens for an entity
        self._max_num_tokens = max(self._max_num_tokens, len(tokens))

        # Update the maximum entity ID
        self._max_entity_id = max(self._max_entity_id, internal_entity_id)

        # Record the tokens for the entity in the counts
        self._record_tokens(tokens)

    def _record_tokens(self, tokens: Tokens) -> None:
        """Record the tokens for a single entity."""

        for token in tokens:
            # Store the tokens for the entity in the set
            self._tokens.add(token)

            # It is assumed that the tokens belong to a single entity
            if token in self._token_to_count:
                self._token_to_count[token] += 1
            else:
                self._token_to_count[token] = 1

    def _add_to_lmdb(
        self, internal_entity_id: int, external_entity_id: str, tokens: Tokens
    ) -> None:
        """Add an entity to the LMDB lookup."""

        with self._env.begin(write=True) as txn:

            # Add internal entity ID -> pickled list of strings
            txn.put(
                internal_entity_id_to_key(internal_entity_id), pickle_list_str(tokens)
            )

            # Add internal entity ID -> number of tokens
            txn.put(
                internal_entity_id_to_token_count_key(internal_entity_id),
                count_to_bytes(len(tokens)),
            )

            # Add internal entity ID -> external entity ID
            txn.put(
                internal_entity_to_external_key(internal_entity_id),
                external_entity_id.encode("ascii"),
            )

        self._num_lmdb_adds += 1
        if self._num_lmdb_adds % 10000 == 0:
            self._env.sync()
            self._num_lmdb_adds = 0
            logger.debug(f"LMDB stats: {self._env.stat()}")

    def _add_to_sqlite(self, entity_id: int, tokens: Tokens) -> None:
        """Add an entity to the Sqlite lookup."""

        if self._conn is None:
            raise Exception("Sqlite connection is None")
        elif self._cursor is None:
            raise Exception("Sqlite cursor is None")

        # Add the token to entity ID mapping
        for token in tokens:
            self._cursor.execute(
                f"INSERT INTO " + TOKEN_TO_ENTITY_ID_TABLENAME + " VALUES(?,?);",
                (token, entity_id),
            )

        # One more entity and its tokens have been added
        self._num_adds += 1

        # Commit the inserts if the insert threshold has been met
        if self._num_adds == 1000:
            self._conn.commit()
            self._num_adds = 0

    def finalise(self) -> None:

        logger.info(f"Performing lookup finalisation")

        if self._conn is None:
            raise Exception("Sqlite connection is None")
        elif self._cursor is None:
            raise Exception("Sqlite cursor is None")

        # Commit any remaining Sqlite insert operations
        if self._num_adds > 0:
            self._conn.commit()

        # Commit any remaining LMDB put operations
        if self._num_lmdb_adds > 0:
            self._env.sync()

        # Write the maximum number of tokens for a single entity
        logger.info(f"Writing the maximum number of tokens for an entity")
        self._write_max_num_tokens()

        # Write the maximum entity ID
        logger.info(f"Writing maximum entity ID ({self._max_entity_id})")
        self._write_max_entity_id()

        # Add an index to the Sqlite token to entity ID table
        logger.info(f"Adding index to Sqlite database")
        self._cursor.execute(
            "CREATE INDEX index2 ON "
            + TOKEN_TO_ENTITY_ID_TABLENAME
            + " ( "
            + TOKEN_COLUMN
            + ");"
        )
        self._conn.commit()

        # Add token to entity IDs to LMDB
        self._write_token_to_entity_ids_lmdb()

        # Delete the temporary Sqlite store
        self._conn.close()

        if self._sqlite_filepath is None:
            raise Exception("Sqlite filepath is None")

        logger.info(f"Deleting temporary Sqlite database: {self._sqlite_filepath}")
        os.remove(self._sqlite_filepath)

        # Write the token counts to file
        self._write_token_counts()

    def _write_token_counts(self):
        """Pickle the token counts and write to file."""

        if self._token_to_count_filepath is None:
            return

        logger.info(
            f"Writing token-to-count dict to file: {self._token_to_count_filepath}"
        )
        with open(self._token_to_count_filepath, "wb") as fp:
            pickle.dump(self._token_to_count, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def _write_token_to_entity_ids_lmdb(self):
        """Write the token to entity IDs to LMDB."""

        logger.info(
            f"Building the token to entity IDs lookup in LMDB for {len(self._tokens)} tokens"
        )

        num_tokens = len(self._tokens)

        with self._env.begin(write=True) as txn:
            for idx, token in enumerate(self._tokens):

                # Get the entity IDs for the token from the Sqlite table
                entity_ids = self._entity_ids_for_token_sqlite(token)
                assert entity_ids is not None

                # Deduplicate the entity IDs (this is required for entities that
                # have repeated tokens)
                entity_ids = list(set(entity_ids))

                # Store the token to a pickled list of entity IDs in LMDB
                txn.put(token_to_key(token), pickle_list(entity_ids))

                # Store the token to a string of entity IDs in LMDB
                s = " ".join([str(e) for e in entity_ids])
                txn.put(token_to_string_key(token), s.encode("ascii"))

                if idx % 100 == 0:
                    logger.info(f"Processed {idx+1} of {num_tokens} tokens")
                    logger.debug(f"LMDB stats: {self._env.stat()}")
                    self._env.sync()

        self._env.sync()
        logger.info(f"Processed {num_tokens} tokens")

    def _entity_ids_for_token_sqlite(self, token: str) -> Optional[List[int]]:
        """Returns the entity IDs for a token from Sqlite."""

        if self._cursor is None:
            raise Exception("Sqlite cursor is None")

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

    def _write_max_num_tokens(self) -> None:
        """Write the maximum number of tokens for an entity to LMDB."""

        with self._env.begin(write=True) as txn:
            value = str(self._max_num_tokens).encode("ascii")
            txn.put(MAX_TOKENS_KEY.encode("ascii"), value)

        self._env.sync()

    def max_number_tokens_for_entity(self) -> int:
        """Get the maximum number of tokens for an entity."""

        with self._env.begin() as txn:
            value = txn.get(MAX_TOKENS_KEY.encode("ascii"))

        assert value is not None
        return int(value)

    @lru_cache(maxsize=100000)
    def tokens_for_entity(self, internal_entity_id: int) -> Optional[Tokens]:
        """Get tokens for an entity given its internal ID."""

        assert_internal_entity_id_valid(internal_entity_id)

        with self._env.begin() as txn:
            result = txn.get(internal_entity_id_to_key(internal_entity_id))

        if result is None:
            return None

        return unpickle_list_str(result)

    @lru_cache(maxsize=100000)
    def entity_ids_for_token(self, token: str) -> Optional[Set[int]]:
        """Get the internal entity IDs for a given token."""

        entity_ids = self.entity_ids_for_token_list(token)
        if entity_ids is None:
            return None

        return set(entity_ids)

    @lru_cache(maxsize=100000)
    def entity_ids_for_token_list(self, token: str) -> Optional[List[int]]:
        """Get the internal entity IDs as a list for a given token."""

        with self._env.begin() as txn:
            result = txn.get(token_to_key(token))

        if result is None:
            return None

        return unpickle_list(result)

    @lru_cache(maxsize=100000)
    def entity_ids_for_token_string(self, token: str) -> Optional[str]:
        """Get the internal entity IDs as a string for a given token."""

        with self._env.begin() as txn:
            result = txn.get(token_to_string_key(token))

        if result is None:
            return None

        # Convert the bytes returned by LMDB to a string
        return result.decode("ascii")

    def matching_entries(self, tokens: Tokens) -> Optional[Set[int]]:
        """Find the matching internal entities in the lookup given the tokens."""

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

    def num_tokens_for_entity(self, internal_entity_id: int) -> Optional[int]:
        """Number of tokens for an entity given its internal ID."""

        with self._env.begin() as txn:
            result = txn.get(internal_entity_id_to_token_count_key(internal_entity_id))

        if result is None:
            return None

        return bytes_to_count(result)

    def max_entity_id(self) -> int:
        """Maximum entity ID."""

        with self._env.begin() as txn:
            value = txn.get(MAX_ENTITY_ID_KEY.encode("ascii"))

        assert value is not None
        return int(value)

    def _write_max_entity_id(self) -> None:
        """Write the maximum entity ID to LMDB."""

        with self._env.begin(write=True) as txn:
            value = str(self._max_entity_id).encode("ascii")
            txn.put(MAX_ENTITY_ID_KEY.encode("ascii"), value)

        self._env.sync()

    def external_entity_id(self, internal_entity_id: int) -> Optional[str]:
        """Get the external entity ID given its internal ID."""

        with self._env.begin() as txn:
            value = txn.get(internal_entity_to_external_key(internal_entity_id))

        if value is None:
            return None

        return value.decode("ascii")

    def close(self):
        logger.info(f"Closing lookup. LMDB stats: {self._env.stat()}")
        self._env.close()
