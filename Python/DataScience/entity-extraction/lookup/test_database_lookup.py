import os
from lookup.database_lookup import DatabaseBackedLookup


def test_database_lookup():

    database_filepath = "./data/test-database.db"

    # Check the file doesn't exist
    if os.path.exists(database_filepath):
        os.remove(database_filepath)

    # Initialise the lookup for loading
    lookup = DatabaseBackedLookup(database_filepath, True)

    # Add entities
    lookup.add("e-1", ["A", "B"])
    lookup.add("e-2", ["A", "C", "D"])

    # Finalise the entries and close the connection
    lookup.finalise()
    lookup.close()

    # Initialise a lookup for reading
    lookup = DatabaseBackedLookup(database_filepath, False)

    lookup._debug()

    # Get the tokens for the entities
    assert lookup.tokens_for_entity("e-1") == ["A", "B"]
    assert lookup.tokens_for_entity("e-2") == ["A", "C", "D"]

    # Get the entities for the tokens
    assert lookup.entity_ids_for_token("A") == set(["e-1", "e-2"])
    assert lookup.entity_ids_for_token("B") == set(["e-1"])
    assert lookup.entity_ids_for_token("C") == set(["e-2"])
    assert lookup.entity_ids_for_token("D") == set(["e-2"])
    assert lookup.entity_ids_for_token("E") is None

    # Close the database connection in the lookup
    lookup.close()

    # Delete the database file
    os.remove(database_filepath)
