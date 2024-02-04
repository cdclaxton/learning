import logging
import os
import sqlite3
from typing import Optional, Set
from domain import Tokens, assert_entity_id_valid, assert_tokens_valid

from lookup.lookup import Lookup


FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

# Database table names
ENTITY_ID_TO_TOKENS_TABLENAME = "EntityIdToTokens"
TOKEN_TO_ENTITY_ID_TABLENAME = "TokenToEntityID"

# Database column names
ENTITY_ID_COLUMN = "entityId"
TOKENS_COLUMN = "tokens"
TOKEN_COLUMN = "token"

TOKEN_SEPARATOR = " "


class DatabaseBackedLookup(Lookup):
    """Database-backed entity to tokens lookup."""

    def __init__(self, filepath: str, load_mode: bool):
        assert type(filepath) == str
        assert type(load_mode) == bool

        self._filepath = filepath
        self._load_mode = load_mode
        self._conn: Optional[sqlite3.Connection] = None
        self._cursor: Optional[sqlite3.Cursor] = None

        self._initialise_database()

    def _initialise_database(self):
        """Initialise the Sqlite database depending on the mode of operation."""

        if self._load_mode:
            self._initialise_load_mode()
        else:
            self._initialise_read_mode()

    def _table_exists(self, table_name: str) -> bool:
        """Does the table exist?"""
        res = self._cursor.execute(
            "SELECT name FROM sqlite_master WHERE name='" + table_name + "';"
        )
        return res.fetchone() is not None

    def _initialise_load_mode(self):
        """Initialise the database for load mode."""

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

    def _initialise_read_mode(self):
        """Initialise the database for reading."""

        logging.info("Database in read mode")
        logging.info(f"Opening connection to database: {self._filepath}")

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

    def add(self, entity_id: str, tokens: Tokens) -> None:
        """Add an entity to the lookup."""

        assert_entity_id_valid(entity_id)
        assert_tokens_valid(tokens)

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

        # Commit the inserts
        self._conn.commit()

    def finalise(self) -> None:
        """Finalise the entries in the lookup."""

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

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def tokens_for_entity(self, entity_id: str) -> Optional[Tokens]:
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

    def entity_ids_for_token(self, token: str) -> Optional[Set[str]]:
        """Get the entity IDs for a given token."""

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

    def _debug(self):
        """Create debug output (only for small databases)."""

        res = self._cursor.execute("SELECT name FROM sqlite_master;")
        print(res.fetchall())
        print("")

        print("Entity ID to tokens:")
        res = self._cursor.execute("SELECT * FROM " + ENTITY_ID_TO_TOKENS_TABLENAME)
        print(res.fetchall())
        print("")

        print("Token to entity ID:")
        res = self._cursor.execute("SELECT * FROM " + TOKEN_TO_ENTITY_ID_TABLENAME)
        print(res.fetchall())

    def matching_entries(self, tokens: Tokens) -> Optional[Set[str]]:
        """Find the matching entities in the lookup given the tokens."""
        pass

    def __repr__(self):
        return f"DatabaseBackedLookup(filepath={self._filepath})"

    def __str__(self):
        return self.__repr__()
