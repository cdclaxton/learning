# Build a database-backed lookup from a SQL database.
import mysql.connector
import sys

from datetime import datetime
from loguru import logger
from lookup.lmdb_lookup import LmdbLookup

from lookup.lookup import Lookup


def load_lookup(lookup: Lookup, username: str, password: str):
    """Load the database-backed lookup from another SQL database."""

    conn = mysql.connector.connect(
        host="localhost",
        database="address_base_v5",
        user=username,
        password=password,
    )

    cur = conn.cursor()
    cur.execute("SELECT address_id, address_base_source_full FROM address")

    num_rows_processed = 0
    start_time = datetime.now()
    start_time_batch = datetime.now()
    batch_size = 10000

    # Use a locally-generated entity ID
    entity_id = 0

    while True:
        result = cur.fetchone()
        if result is None:
            break

        # Extract the tokens from the database row
        tokens = [ri.replace(",", "").lower() for ri in result[1].split()]

        # Add the entity to the lookup
        lookup.add(entity_id, tokens)

        if num_rows_processed % batch_size == 0:
            end_time_batch = datetime.now()
            time_diff = (end_time_batch - start_time_batch).total_seconds()
            logger.info(
                f"Processed {num_rows_processed} rows (batch of {batch_size} took {time_diff} seconds)"
            )
            start_time_batch = datetime.now()

        num_rows_processed += 1
        entity_id += 1

    logger.info(f"Processed {num_rows_processed} rows")

    # Close the connection to the database
    conn.close()

    end_time = datetime.now()
    logger.info(
        f"Time taken to load: {(end_time - start_time).total_seconds()} seconds"
    )


if __name__ == "__main__":

    # Get the username and password from the command line arguments
    if len(sys.argv) != 3:
        print("Usage: {sys.argv[0]} <username> <password>")
        exit()

    username = sys.argv[1]
    password = sys.argv[2]

    # Location of the database file
    # database_filepath = "./data/full-database.db"

    # Initialise the database-backed lookup for loading
    start_script = datetime.now()
    # lookup = DatabaseBackedLookup(database_filepath, True)

    lmdb_folder = "./data/lmdb"
    sqlite_database = "./data/sqlite.db"
    token_to_count_filepath = "./data/token-to-count.pickle"
    lookup = LmdbLookup(lmdb_folder, True, sqlite_database, token_to_count_filepath)

    # Load the lookup
    load_lookup(lookup, username, password)

    # Finalise the entries
    start_finalise = datetime.now()
    lookup.finalise()
    logger.info(
        f"Time taken to finalise: {(datetime.now() - start_finalise).total_seconds()} seconds"
    )

    # Close the connection to the database
    lookup.close()

    logger.info(
        f"Total time to build database: {(datetime.now() - start_script).total_seconds()} seconds"
    )
