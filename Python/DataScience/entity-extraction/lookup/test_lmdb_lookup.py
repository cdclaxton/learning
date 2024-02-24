import os
import shutil
from lookup.lmdb_lookup import LmdbLookup


TEST_LMDB_FOLDER = "./data/test"
TEST_SQLITE_DATABASE = "./data/test.db"


def delete_temp():
    # Delete the Sqlite database if it exists
    if os.path.exists(TEST_SQLITE_DATABASE):
        os.remove(TEST_SQLITE_DATABASE)

    # Delete the LMDB if it exists
    if os.path.exists(TEST_LMDB_FOLDER):
        shutil.rmtree(TEST_LMDB_FOLDER)


def lmdb_for_writing():
    delete_temp()
    return LmdbLookup(TEST_LMDB_FOLDER, True, TEST_SQLITE_DATABASE)


def lmdb_for_reading():
    return LmdbLookup(TEST_LMDB_FOLDER, False)


def cleanup(lookup: LmdbLookup) -> None:
    lookup.close()

    # Delete the Sqlite database if it exists
    if os.path.exists(TEST_SQLITE_DATABASE):
        os.remove(TEST_SQLITE_DATABASE)

    # Delete the LMDB if it exists
    if os.path.exists(TEST_LMDB_FOLDER):
        shutil.rmtree(TEST_LMDB_FOLDER)


def test_write_read_max_tokens():
    lookup = lmdb_for_writing()
    lookup._max_num_tokens = 10
    lookup._write_max_num_tokens()
    assert lookup.max_number_tokens_for_entity() == 10
    cleanup(lookup)


def test_add_entity_tokens_to_lmdb():
    lookup = lmdb_for_writing()

    lookup._add_to_lmdb("e-1", ["a"])
    assert lookup.tokens_for_entity("e-1") == ["a"]
    assert lookup.tokens_for_entity("e-2") is None

    lookup._add_to_lmdb("e-2", ["a", "b"])
    assert lookup.tokens_for_entity("e-1") == ["a"]
    assert lookup.tokens_for_entity("e-2") == ["a", "b"]

    cleanup(lookup)


def test_full_test():
    lookup = lmdb_for_writing()

    # Populate the lookup
    dataset = {"e-1": ["a"], "e-2": ["a", "b"], "e-3": ["b", "c", "d"]}

    for entity_id, tokens in dataset.items():
        lookup.add(entity_id, tokens)

    # Finalise the lookup
    lookup.finalise()
    lookup.close()

    # Open a new lookup for reading
    lookup = lmdb_for_reading()

    # Check the contents of the lookup
    for entity_id in dataset:
        actual_tokens = lookup.tokens_for_entity(entity_id)
        assert actual_tokens == dataset[entity_id]

    # Check the maximum number of tokens for an entity
    assert lookup.max_number_tokens_for_entity() == 3

    # Check the entity IDs for a given token
    assert set(lookup.entity_ids_for_token("a")) == {"e-1", "e-2"}
    assert set(lookup.entity_ids_for_token("b")) == {"e-2", "e-3"}
    assert set(lookup.entity_ids_for_token("c")) == {"e-3"}
    assert set(lookup.entity_ids_for_token("d")) == {"e-3"}
    assert lookup.entity_ids_for_token("z") is None

    # Check the entity IDs for a given token, returned as a list
    assert sorted(lookup.entity_ids_for_token_list("a")) == ["e-1", "e-2"]
    assert sorted(lookup.entity_ids_for_token_list("b")) == ["e-2", "e-3"]
    assert lookup.entity_ids_for_token_list("c") == ["e-3"]
    assert lookup.entity_ids_for_token_list("d") == ["e-3"]
    assert lookup.entity_ids_for_token_list("z") is None

    # Check the matching entities
    assert lookup.matching_entries(["a"]) == {"e-1", "e-2"}
    assert lookup.matching_entries(["a", "b"]) == {"e-2"}
    assert lookup.matching_entries(["b"]) == {"e-2", "e-3"}
    assert lookup.matching_entries(["b", "c"]) == {"e-3"}
    assert lookup.matching_entries(["b", "d", "c"]) == {"e-3"}
    assert lookup.matching_entries(["b", "e", "c"]) is None

    cleanup(lookup)
