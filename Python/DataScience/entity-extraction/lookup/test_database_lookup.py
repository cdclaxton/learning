import os
from lookup.database_lookup import (
    DatabaseBackedLookup,
    pickle_list,
    pickle_set,
    unpickle_list,
    unpickle_set,
)


def test_database_lookup():

    database_filepath = "./data/test-database.db"

    # Check the file doesn't exist
    if os.path.exists(database_filepath):
        os.remove(database_filepath)

    # Initialise the lookup for loading
    lookup = DatabaseBackedLookup(database_filepath, True)

    # Add entities
    lookup.add(1, ["A", "B"])
    lookup.add(2, ["A", "C", "D"])

    # Finalise the entries and close the connection
    lookup.finalise()
    lookup.close()

    # Initialise a lookup for reading
    lookup = DatabaseBackedLookup(database_filepath, False)

    # Get the tokens for the entities
    assert lookup.tokens_for_entity(1) == ["A", "B"]
    assert lookup.tokens_for_entity(2) == ["A", "C", "D"]
    assert lookup.tokens_for_entity(3) is None

    # Get the entities for the tokens
    assert lookup.entity_ids_for_token("A") == {1, 2}
    assert lookup.entity_ids_for_token("B") == {1}
    assert lookup.entity_ids_for_token("C") == {2}
    assert lookup.entity_ids_for_token("D") == {2}
    assert lookup.entity_ids_for_token("E") is None

    assert lookup.entity_ids_for_token_list("A") == [1, 2]
    assert lookup.entity_ids_for_token_list("B") == [1]
    assert lookup.entity_ids_for_token_list("C") == [2]
    assert lookup.entity_ids_for_token_list("D") == [2]
    assert lookup.entity_ids_for_token_list("E") is None

    # Get the matching entities
    assert lookup.matching_entries(["A"]) == {1, 2}
    assert lookup.matching_entries(["B"]) == {1}
    assert lookup.matching_entries(["A", "B"]) == {1}
    assert lookup.matching_entries(["A", "D", "C"]) == {2}
    assert lookup.matching_entries(["A", "B", "E"]) is None

    # Check the maximum number of tokens for an entity
    assert lookup.max_number_tokens_for_entity() == 3

    # Check the number of tokens for an entity
    assert lookup.num_tokens_for_entity(1) == 2
    assert lookup.num_tokens_for_entity(2) == 3
    assert lookup.num_tokens_for_entity(100) is None  # Doesn't exist

    # Close the database connection in the lookup
    lookup.close()

    # Delete the database file
    os.remove(database_filepath)


def test_pickle_unpickle():
    s = {1, 2, 3}
    assert s == unpickle_set(pickle_set(s))

    l = [1, 2, 3]
    assert l == unpickle_list(pickle_list(l))
