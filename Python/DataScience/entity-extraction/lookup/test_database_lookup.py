import os
from lookup.database_lookup import DatabaseBackedLookup, pickle_set, unpickle_set


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

    # Get the tokens for the entities
    assert lookup.tokens_for_entity("e-1") == ["A", "B"]
    assert lookup.tokens_for_entity("e-2") == ["A", "C", "D"]
    assert lookup.tokens_for_entity("e-3") is None

    # Get the entities for the tokens
    assert lookup.entity_ids_for_token("A") == {"e-1", "e-2"}
    assert lookup.entity_ids_for_token("B") == {"e-1"}
    assert lookup.entity_ids_for_token("C") == {"e-2"}
    assert lookup.entity_ids_for_token("D") == {"e-2"}
    assert lookup.entity_ids_for_token("E") is None

    # Get the matching entities
    assert lookup.matching_entries(["A"]) == {"e-1", "e-2"}
    assert lookup.matching_entries(["B"]) == {"e-1"}
    assert lookup.matching_entries(["A", "B"]) == {"e-1"}
    assert lookup.matching_entries(["A", "D", "C"]) == {"e-2"}
    assert lookup.matching_entries(["A", "B", "E"]) is None

    # Check the maximum number of tokens for an entity
    assert lookup.get_max_tokens() == 3

    # Close the database connection in the lookup
    lookup.close()

    # Delete the database file
    os.remove(database_filepath)


def test_pickle_unpickle():
    s = {"a", "b", "c"}
    assert s == unpickle_set(pickle_set(s))
