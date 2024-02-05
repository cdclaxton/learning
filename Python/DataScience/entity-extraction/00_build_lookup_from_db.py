# Build a database-backed lookup from a SQL database.
import mysql.connector
import sys

from datetime import datetime
from lookup.database_lookup import DatabaseBackedLookup


def load_lookup(lookup: DatabaseBackedLookup, username: str, password: str):
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

    while True:
        result = cur.fetchone()
        if result is None:
            break

        # Extract the entity ID and parse the tokens from the database row
        entity_id = result[0]
        tokens = [ri.replace(",", "").lower() for ri in result[1].split()]

        # Add the entity to the lookup
        lookup.add(entity_id, tokens)

        if num_rows_processed % 10000 == 0:
            end_time_batch = datetime.now()
            time_diff = (end_time_batch - start_time_batch).total_seconds()
            print(f"Processed {num_rows_processed} rows ({time_diff} seconds)")
            start_time_batch = datetime.now()

        num_rows_processed += 1

    # Close the connection to the database
    conn.close()

    end_time = datetime.now()
    print(f"Time taken to load: {(end_time - start_time).total_seconds()} seconds")


if __name__ == "__main__":

    # Get the username and password from the command line arguments
    if len(sys.argv) != 3:
        print("Usage: {sys.argv[0]} <username> <password>")
        exit()

    username = sys.argv[1]
    password = sys.argv[2]

    # Location of the database file
    database_filepath = "./data/full-database.db"

    # Initialise the database-backed lookup for loading
    lookup = DatabaseBackedLookup(database_filepath, True)

    # Load the lookup
    load_lookup(lookup, username, password)

    # Finalise the entries
    start = datetime.now()
    lookup.finalise()
    print(f"Time taken to finalise: {(datetime.now() - start).total_seconds()} seconds")

    # Close the connection to the database
    lookup.close()
