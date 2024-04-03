import os
import shutil
from lookup.lmdb_lookup import LmdbLookup, bytes_to_count, count_to_bytes


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


def test_token_count():
    for i in range(0, 100):
        assert bytes_to_count(count_to_bytes(i)) == i


def test_full_test():
    lookup = lmdb_for_writing()

    # Populate the lookup
    dataset = {1: ["a"], 2: ["a", "b"], 3: ["b", "c", "d"]}

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

    # Check the maximum entity ID
    assert lookup.max_entity_id() == 3

    # Check the entity IDs for a given token
    assert set(lookup.entity_ids_for_token("a")) == {1, 2}
    assert set(lookup.entity_ids_for_token("b")) == {2, 3}
    assert set(lookup.entity_ids_for_token("c")) == {3}
    assert set(lookup.entity_ids_for_token("d")) == {3}
    assert lookup.entity_ids_for_token("z") is None

    # Check the entity IDs for a given token, returned as a list
    assert sorted(lookup.entity_ids_for_token_list("a")) == [1, 2]
    assert sorted(lookup.entity_ids_for_token_list("b")) == [2, 3]
    assert lookup.entity_ids_for_token_list("c") == [3]
    assert lookup.entity_ids_for_token_list("d") == [3]
    assert lookup.entity_ids_for_token_list("z") is None

    # Check the matching entities
    assert lookup.matching_entries(["a"]) == {1, 2}
    assert lookup.matching_entries(["a", "b"]) == {2}
    assert lookup.matching_entries(["b"]) == {2, 3}
    assert lookup.matching_entries(["b", "c"]) == {3}
    assert lookup.matching_entries(["b", "d", "c"]) == {3}
    assert lookup.matching_entries(["b", "e", "c"]) is None

    # Check the token count for an entity
    assert lookup.num_tokens_for_entity(1) == 1
    assert lookup.num_tokens_for_entity(2) == 2
    assert lookup.num_tokens_for_entity(3) == 3
    assert lookup.num_tokens_for_entity(100) is None

    cleanup(lookup)
