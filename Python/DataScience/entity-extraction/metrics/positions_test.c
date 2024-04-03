#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "positions.h"

bool test_counts(char *str, uint32_t max_entity_id, uint8_t *expected)
{
    uint8_t *counts = count_occurrences(str, max_entity_id);
    if (counts == NULL)
    {
        return false;
    }

    bool success = true;
    for (uint32_t i = 0; i < (max_entity_id + 1); i++)
    {
        if (counts[i] != expected[i])
        {
            printf("Index: %d, Expected=%d, Actual=%d\n",
                   i, expected[i], counts[i]);
            fflush(stdout);
            success = false;
            break;
        }
    }

    free(counts);

    return success;
}

void test_count_occurrences_1(void)
{
    printf("Running test_count_occurrences_1()\n");

    // Empty string
    uint8_t expected_counts_1[5] = {0, 0, 0, 0, 0};
    assert(test_counts("", 4, expected_counts_1));

    // One entity
    uint8_t expected_counts_2[5] = {0, 1, 0, 0, 0};
    assert(test_counts("1", 4, expected_counts_2));

    // Two entities
    uint8_t expected_counts_3[5] = {0, 1, 0, 0, 1};
    assert(test_counts("1 4", 4, expected_counts_3));

    // One entity occurs twice
    uint8_t expected_counts_4[5] = {0, 2, 0, 0, 0};
    assert(test_counts("1|1", 4, expected_counts_4));

    // One entity occurs twice
    uint8_t expected_counts_5[5] = {0, 2, 0, 0, 0};
    assert(test_counts("1||||||1", 4, expected_counts_5));
}

void test_count_occurrences_2(void)
{
    printf("Running test_count_occurrences_2()\n");

    uint32_t max_entity_id = 32000000;
    uint8_t *expected = calloc(max_entity_id, sizeof(uint8_t));
    expected[0] = 3;
    expected[3] = 1;
    expected[4] = 1;
    expected[150000] = 2;
    expected[32000000] = 1;

    bool success = test_counts("0||0|32000000 150000|3 4|0|150000",
                               max_entity_id, expected);

    free(expected);
    assert(success);
}

void test_count_occurrences_3(void)
{
    printf("Running test_count_occurrences_3()\n");

    uint8_t *counts = count_occurrences("0|2|5000|0", 250);
    assert(counts == NULL);
}

void test_initialise_position_results_1(void)
{
    printf("Running test_initialise_position_results_1()\n");

    uint32_t max_entity_id = 4U;
    uint8_t counts[] = {2, 0, 1, 0, 3};
    int16_t expected_n[] = {0, -1, 0, -1, 0};

    DenseEntityPositions *actual = initialise_position_results(counts, max_entity_id, 1);
    bool success = true;
    for (uint32_t i = 0; i < (max_entity_id + 1); i++)
    {
        if (actual[i].n != expected_n[i])
        {
            success = false;
        }
    }

    free(actual);
    assert(success);
}

bool dense_entity_positions_equal(DenseEntityPositions expected,
                                  DenseEntityPositions actual)
{
    if (expected.n != actual.n)
    {
        printf("Expected n=%d, actual=%d\n", expected.n, actual.n);
        return false;
    }

    if (expected.n > 0)
    {
        for (int16_t i = 0; i < expected.n; i++)
        {
            if (expected.arr[i] != actual.arr[i])
            {
                return false;
            }
        }
    }

    return true;
}

bool dense_entity_positions_arrays_equal(DenseEntityPositions *expected,
                                         DenseEntityPositions *actual,
                                         uint32_t n)
{
    for (uint32_t i = 0; i < n; i++)
    {
        if (dense_entity_positions_equal(expected[i], actual[i]) == false)
        {
            printf("dense_entity_positions_arrays_equal: Failure at index %d\n",
                   i);
            return false;
        }
    }

    return true;
}

bool entity_positions_equal(EntityPositions expected,
                            EntityPositions actual)
{
    if (expected.n != actual.n)
    {
        printf("Expected n=%d, actual=%d\n", expected.n, actual.n);
        return false;
    }

    if (expected.entity_id != actual.entity_id)
    {
        printf("Expected entity ID=%d, actual=%d\n", expected.entity_id,
               actual.entity_id);
        return false;
    }

    if (expected.n > 0)
    {
        for (uint8_t i = 0; i < expected.n; i++)
        {
            if (expected.arr[i] != actual.arr[i])
            {
                return false;
            }
        }
    }

    return true;
}

bool entity_positions_array_equal(EntityPositions *expected,
                                  EntityPositions *actual,
                                  uint32_t n)
{
    for (uint32_t i = 0; i < n; i++)
    {
        if (entity_positions_equal(expected[i], actual[i]) == false)
        {
            printf("entity_positions_array_equal: Failure with index %d\n", i);
            fflush(stdout);
            return false;
        }
    }

    return true;
}

void test_populate_position_results_1(void)
{
    printf("Running test_populate_position_results_1()\n");

    uint32_t max_entity_id = 3;
    char str[] = "0 3|2 3|2";

    DenseEntityPositions expected[4];

    // Entity 0
    expected[0].n = 1;
    uint8_t arr_0[] = {0};
    expected[0].arr = arr_0;

    // Entity 1 (doesn't occur)
    expected[1].n = -1;

    // Entity 2
    expected[2].n = 2;
    uint8_t arr_2[] = {1, 2};
    expected[2].arr = arr_2;

    // Entity 3
    expected[3].n = 2;
    uint8_t arr_3[] = {0, 1};
    expected[3].arr = arr_3;

    uint8_t *counts = count_occurrences(str, max_entity_id);
    assert(counts != NULL);

    DenseEntityPositions *actual = populate_position_results(str,
                                                             max_entity_id,
                                                             1U,
                                                             counts);
    bool success = dense_entity_positions_arrays_equal(expected,
                                                       actual,
                                                       max_entity_id + 1);

    free(counts);
    free(actual);
    assert(success);
}

bool check_sparse_position_results(SparsePositionResults expected,
                                   SparsePositionResults actual)
{
    if (expected.n != actual.n)
    {
        printf("check_sparse_position_results: Expected n=%d, actual=%d",
               expected.n, actual.n);
        return false;
    }

    if (entity_positions_array_equal(expected.results,
                                     actual.results,
                                     expected.n) == false)
    {
        printf("check_sparse_position_results: EntityPositions don't match\n");
        return false;
    }

    if (strcmp(expected.error_message, actual.error_message) != 0)
    {
        printf("check_sparse_position_results: Expected error_message=%s, actual=%s\n",
               expected.error_message, actual.error_message);
        return false;
    }

    return true;
}

void test_compact_1(void)
{
    printf("Running test_compact_1()\n");

    SparsePositionResults expected;
    expected.n = 0;
    expected.error_message[0] = '\0';

    char str[] = "2|3|2";
    uint32_t max_entity_id = 5;

    uint8_t *counts = count_occurrences(str, max_entity_id);
    assert(counts != NULL);

    // Setting min count to 3 so no results are generated
    DenseEntityPositions *dense = populate_position_results(str,
                                                            max_entity_id,
                                                            3U,
                                                            counts);

    SparsePositionResults actual = compact(dense, max_entity_id);

    bool success = check_sparse_position_results(expected, actual);

    free(counts);
    free(dense);
    free_sparse_position_results(&actual);

    assert(success);
}

void test_compact_2(void)
{
    printf("Running test_compact_2()\n");

    SparsePositionResults expected;
    expected.n = 3;
    expected.error_message[0] = '\0';

    EntityPositions entity_positions[3];

    // Entity ID 0
    entity_positions[0].entity_id = 0;
    entity_positions[0].n = 1;
    uint8_t entity_pos_0[] = {1};
    entity_positions[0].arr = entity_pos_0;

    // Entity ID 1000
    entity_positions[1].entity_id = 1000;
    entity_positions[1].n = 2;
    uint8_t entity_pos_1[] = {0, 1};
    entity_positions[1].arr = entity_pos_1;

    // Entity ID 32000000
    entity_positions[2].entity_id = 32000000;
    entity_positions[2].n = 1;
    uint8_t entity_pos_2[] = {2};
    entity_positions[2].arr = entity_pos_2;

    expected.results = entity_positions;

    char str[] = "1000|0 1000|32000000";
    uint32_t max_entity_id = 32000000;

    uint8_t *counts = count_occurrences(str, max_entity_id);
    assert(counts != NULL);

    DenseEntityPositions *dense = populate_position_results(str,
                                                            max_entity_id,
                                                            1U,
                                                            counts);

    SparsePositionResults actual = compact(dense, max_entity_id);

    bool success = check_sparse_position_results(expected, actual);

    free(counts);
    free(dense);
    free_sparse_position_results(&actual);

    assert(success);
}

void test_positions_1(void)
{
    printf("Running test_positions_1()\n");

    char str[] = "1000|0 1000|32000000";
    uint32_t max_entity_id = 32000000;
    uint8_t min_count = 3U;

    SparsePositionResults expected;
    expected.n = 0;
    expected.error_message[0] = '\0';

    SparsePositionResults actual = positions(str, max_entity_id, min_count);

    bool success = check_sparse_position_results(expected, actual);
    free_sparse_position_results(&actual);

    assert(success);
}

void test_positions_2(void)
{
    printf("Running test_positions_2()\n");

    char str[] = "1000|0 1000|32000000";
    uint32_t max_entity_id = 32000000;
    uint8_t min_count = 1U;

    SparsePositionResults expected;
    expected.n = 3;
    expected.error_message[0] = '\0';

    EntityPositions entity_positions[3];

    // Entity ID 0
    entity_positions[0].entity_id = 0;
    entity_positions[0].n = 1;
    uint8_t entity_pos_0[] = {1};
    entity_positions[0].arr = entity_pos_0;

    // Entity ID 1000
    entity_positions[1].entity_id = 1000;
    entity_positions[1].n = 2;
    uint8_t entity_pos_1[] = {0, 1};
    entity_positions[1].arr = entity_pos_1;

    // Entity ID 32000000
    entity_positions[2].entity_id = 32000000;
    entity_positions[2].n = 1;
    uint8_t entity_pos_2[] = {2};
    entity_positions[2].arr = entity_pos_2;

    expected.results = entity_positions;

    SparsePositionResults actual = positions(str, max_entity_id, min_count);

    bool success = check_sparse_position_results(expected, actual);
    free_sparse_position_results(&actual);

    assert(success);
}

int main(void)
{
    printf("Running tests ...\n");
    test_count_occurrences_1();
    test_count_occurrences_2();
    test_count_occurrences_3();
    test_initialise_position_results_1();
    test_populate_position_results_1();
    test_compact_1();
    test_compact_2();
    test_positions_1();
    test_positions_2();
}
