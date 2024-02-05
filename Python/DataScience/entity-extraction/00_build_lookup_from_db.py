# Build a database-backed lookup from a SQL database.
import mysql.connector
import sys

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
    res = cur.execute(
        "SELECT address_id, address_base_source_full FROM address limit 10"
    )

    num_rows_processed = 0

    while True:
        result = res.fetchone()
        if result is None:
            break
        print(result)

        if num_rows_processed % 10000 == 0:
            print(f"Processed {num_rows_processed} rows")

    # Close the connection to the database
    conn.close()


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

    # Finalise the entries and close the connection to the database
    lookup.finalise()
    lookup.close()
