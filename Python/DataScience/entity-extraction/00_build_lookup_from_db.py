# Build a database-backed lookup from a SQL database.

from lookup.database_lookup import DatabaseBackedLookup


def load_lookup(lookup: DatabaseBackedLookup):
    """Load the database-backed lookup from another SQL database."""

    num_rows_processed = 0

    if num_rows_processed % 10000 == 0:
        print(f"Processed {num_rows_processed} rows")


if __name__ == "__main__":

    # Location of the database file
    database_filepath = "./data/full-database.db"

    # Initialise the database-backed lookup for loading
    lookup = DatabaseBackedLookup(database_filepath, True)

    # Load the lookup
    load_lookup(lookup)

    # Finalise the entries and close the connection to the database
    lookup.finalise()
    lookup.close()
