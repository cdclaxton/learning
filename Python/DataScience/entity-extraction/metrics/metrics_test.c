#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "metrics.h"

void test_allocate_and_initalise_array(void)
{
    printf("Testing allocate_and_initalise_array()\n");

    // Test cases of the number of elements
    uint32_t num_elements[] = {1, 10, 100, 100};

    for (int idx = 0; idx < 4; idx++)
    {
        uint32_t test_case = num_elements[idx];
        uint8_t *arr = allocate_and_initialise_array(test_case);

        // Check the array has zeros
        for (uint32_t i = 0; i < test_case; i++)
        {
            assert(arr[i] == 0);
        }

        free(arr);
    }
}

bool arrays_equal(uint8_t *expected, uint8_t *actual, int num_elements)
{
    for (int i = 0; i < num_elements; i++)
    {
        if (expected[i] != actual[i])
        {
            printf("Expected=%d, actual=%d\n", expected[i], actual[i]);
            return false;
        }
    }

    return true;
}

bool check_counts_starts_ends(uint8_t *expected_counts,
                              uint8_t *expected_starts,
                              uint8_t *expected_ends,
                              uint8_t *actual_counts,
                              uint8_t *actual_starts,
                              uint8_t *actual_ends,
                              uint32_t max_entity_id)
{
    if (!arrays_equal(expected_counts, actual_counts, max_entity_id + 1))
    {
        return false;
    }

    if (!arrays_equal(expected_starts, actual_starts, max_entity_id + 1))
    {
        return false;
    }

    if (!arrays_equal(expected_ends, actual_ends, max_entity_id + 1))
    {
        return false;
    }

    return true;
}

void test_update_1(void)
{
    printf("Testing update() [1]\n");

    // Create an array of counts, starts and ends
    uint32_t max_entity_id = 5;
    uint8_t *counts = allocate_and_initialise_array(max_entity_id);
    uint8_t *starts = allocate_and_initialise_array(max_entity_id);
    uint8_t *ends = allocate_and_initialise_array(max_entity_id);

    uint8_t expected_counts[] = {0, 0, 0, 1, 0, 0};
    uint8_t expected_starts[] = {0, 0, 0, 2, 0, 0};
    uint8_t expected_ends[] = {0, 0, 0, 2, 0, 0};

    // Entity 3 found in batch 2
    update(2, 3, max_entity_id, counts, starts, ends);
    assert(check_counts_starts_ends(expected_counts, expected_starts, expected_ends,
                                    counts, starts, ends, max_entity_id));

    // Entity 3 found in batch 4
    update(4, 3, max_entity_id, counts, starts, ends);
    expected_counts[3] = 2;
    expected_ends[3] = 4;
    assert(check_counts_starts_ends(expected_counts, expected_starts, expected_ends,
                                    counts, starts, ends, max_entity_id));

    free(counts);
    free(starts);
    free(ends);
}

void test_update_2(void)
{
    printf("Testing update() [2]\n");

    // Create an array of counts, starts and ends
    uint32_t max_entity_id = 32000000;
    uint8_t *counts = allocate_and_initialise_array(max_entity_id);
    uint8_t *starts = allocate_and_initialise_array(max_entity_id);
    uint8_t *ends = allocate_and_initialise_array(max_entity_id);

    uint8_t *expected_counts = allocate_and_initialise_array(max_entity_id);
    uint8_t *expected_starts = allocate_and_initialise_array(max_entity_id);
    uint8_t *expected_ends = allocate_and_initialise_array(max_entity_id);

    // Update the first entity (0)
    update(2, 0, max_entity_id, counts, starts, ends);
    expected_counts[0] = 1;
    expected_starts[0] = 2;
    expected_ends[0] = 2;
    assert(check_counts_starts_ends(expected_counts, expected_starts, expected_ends,
                                    counts, starts, ends, max_entity_id));

    // Update the first entity (0) again
    update(3, 0, max_entity_id, counts, starts, ends);
    expected_counts[0] = 2;
    expected_ends[0] = 3;
    assert(check_counts_starts_ends(expected_counts, expected_starts, expected_ends,
                                    counts, starts, ends, max_entity_id));

    // Update the last entity (with ID 32,000,000)
    update(4, 32000000, max_entity_id, counts, starts, ends);
    expected_counts[32000000] = 1;
    expected_starts[32000000] = 4;
    expected_ends[32000000] = 4;
    assert(check_counts_starts_ends(expected_counts, expected_starts, expected_ends,
                                    counts, starts, ends, max_entity_id));

    free(counts);
    free(starts);
    free(ends);

    free(expected_counts);
    free(expected_starts);
    free(expected_ends);
}

bool entity_spans_equal(EntitySpan expected, EntitySpan actual)
{
    if (expected.entity_id != actual.entity_id)
    {
        printf("Expected entity ID=%d, actual=%d\n", expected.entity_id,
               actual.entity_id);
        return false;
    }

    if (expected.count != actual.count)
    {
        printf("Expected count=%d, actual=%d\n", expected.count,
               actual.count);
        return false;
    }

    if (expected.start_index != actual.start_index)
    {
        printf("Expected start index=%d, actual=%d\n", expected.start_index,
               actual.start_index);
        return false;
    }

    if (expected.end_index != actual.end_index)
    {
        printf("Expected end index=%d, actual=%d\n", expected.end_index,
               actual.end_index);
        return false;
    }

    return true;
}

bool result_sets_equal(ResultSet expected, ResultSet actual)
{
    if (expected.n != actual.n)
    {
        printf("Expected n=%d, actual=%d\n", expected.n, actual.n);
        return false;
    }

    for (uint32_t i = 0; i < expected.n; i++)
    {
        if (!entity_spans_equal(expected.arr[i], actual.arr[i]))
        {
            printf("Check failed for element %d\n", i);
            return false;
        }
    }

    return true;
}

void set_entity_span(EntitySpan *entity_span,
                     uint32_t entity_id,
                     uint8_t count,
                     uint8_t start_index,
                     uint8_t end_index)
{
    entity_span->entity_id = entity_id;
    entity_span->count = count;
    entity_span->start_index = start_index;
    entity_span->end_index = end_index;
}

void test_collect_1(void)
{
    printf("Testing collect() [1]\n");

    uint32_t max_entity_id = 5;
    uint8_t counts[] = {1, 0, 1, 0, 2, 3};
    uint8_t starts[] = {10, 0, 11, 0, 12, 13};
    uint8_t ends[] = {20, 0, 21, 0, 22, 23};

    EntitySpan expected_spans[4];
    set_entity_span(&expected_spans[0], 0, 1, 10, 20);
    set_entity_span(&expected_spans[1], 2, 1, 11, 21);
    set_entity_span(&expected_spans[2], 4, 2, 12, 22);
    set_entity_span(&expected_spans[3], 5, 3, 13, 23);

    ResultSet expected;
    expected.n = 4;
    expected.arr = expected_spans;

    ResultSet actual = collect(counts, starts, ends, max_entity_id, 1);

    if (!result_sets_equal(expected, actual))
    {
        printf("Expected:\n");
        print_result_set(expected);
        printf("Actual:\n");
        print_result_set(actual);
        assert(false);
    }
}

void test_collect_2(void)
{
    printf("Testing collect() [2]\n");

    uint32_t max_entity_id = 32000000;

    uint8_t *counts = allocate_and_initialise_array(max_entity_id + 1);
    uint8_t *starts = allocate_and_initialise_array(max_entity_id + 1);
    uint8_t *ends = allocate_and_initialise_array(max_entity_id + 1);

    // Set entity 0
    counts[0] = 2;
    starts[0] = 10;
    ends[0] = 12;

    // Set entity 100
    counts[100] = 5;
    starts[100] = 120;
    ends[100] = 130;

    // Set entity 100000
    counts[100000] = 6;
    starts[100000] = 200;
    ends[100000] = 210;

    // Set entity 100000
    counts[32000000] = 7;
    starts[32000000] = 230;
    ends[32000000] = 236;

    EntitySpan expected_spans[4];
    set_entity_span(&expected_spans[0], 0, 2, 10, 12);
    set_entity_span(&expected_spans[1], 100, 5, 120, 130);
    set_entity_span(&expected_spans[2], 100000, 6, 200, 210);
    set_entity_span(&expected_spans[3], 32000000, 7, 230, 236);

    ResultSet expected;
    expected.n = 4;
    expected.arr = expected_spans;

    ResultSet actual = collect(counts, starts, ends, max_entity_id, 1);

    free(counts);
    free(starts);
    free(ends);

    if (!result_sets_equal(expected, actual))
    {
        printf("Expected:\n");
        print_result_set(expected);
        printf("Actual:\n");
        print_result_set(actual);
        assert(false);
    }
}

void check_calc_result(char *str,
                       uint32_t max_entity_id,
                       ResultSet expected)
{
    ResultSet actual = calc(str, max_entity_id, 1);

    if (!result_sets_equal(expected, actual))
    {
        printf("Expected:\n");
        print_result_set(expected);
        printf("Actual:\n");
        print_result_set(actual);
        assert(false);
    }
}

void test_calc_1(void)
{
    printf("Testing calc() [1]\n");
    uint32_t max_entity_id = 32000000;

    EntitySpan expected_spans[1];
    set_entity_span(&expected_spans[0], 0, 1, 0, 0);

    ResultSet expected;
    expected.n = 1;
    expected.arr = expected_spans;

    check_calc_result("0", max_entity_id, expected);
}

void test_calc_2(void)
{
    printf("Testing calc() [2]\n");
    uint32_t max_entity_id = 32000000;

    EntitySpan expected_spans[1];
    set_entity_span(&expected_spans[0], 0, 2, 0, 1);

    ResultSet expected;
    expected.n = 1;
    expected.arr = expected_spans;

    check_calc_result("0|0", max_entity_id, expected);
}

void test_calc_3(void)
{
    printf("Testing calc() [3]\n");
    uint32_t max_entity_id = 32000000;

    EntitySpan expected_spans[2];
    set_entity_span(&expected_spans[0], 0, 2, 0, 1);
    set_entity_span(&expected_spans[1], 1, 1, 0, 0);

    ResultSet expected;
    expected.n = 2;
    expected.arr = expected_spans;

    check_calc_result("0 1|0", max_entity_id, expected);
}

void test_calc_4(void)
{
    printf("Testing calc() [4]\n");
    uint32_t max_entity_id = 32000000;

    EntitySpan expected_spans[2];
    set_entity_span(&expected_spans[0], 0, 2, 0, 1);
    set_entity_span(&expected_spans[1], 1, 2, 0, 3);

    ResultSet expected;
    expected.n = 2;
    expected.arr = expected_spans;

    check_calc_result("0 1|0||1", max_entity_id, expected);
}

void test_calc_5(void)
{
    printf("Testing calc() [5]\n");
    uint32_t max_entity_id = 32000000;

    EntitySpan expected_spans[3];
    set_entity_span(&expected_spans[0], 0, 2, 0, 2);
    set_entity_span(&expected_spans[1], 1, 1, 0, 0);
    set_entity_span(&expected_spans[2], 32000000, 1, 1, 1);

    ResultSet expected;
    expected.n = 3;
    expected.arr = expected_spans;

    check_calc_result("0 1|32000000|0", max_entity_id, expected);
}

void test_calc_6(void)
{
    printf("Testing calc() [6]\n");
    uint32_t max_entity_id = 32000000;

    EntitySpan expected_spans[5];
    set_entity_span(&expected_spans[0], 0, 2, 0, 2);
    set_entity_span(&expected_spans[1], 1, 1, 0, 0);
    set_entity_span(&expected_spans[2], 1000, 1, 2, 2);
    set_entity_span(&expected_spans[3], 31000123, 2, 1, 3);
    set_entity_span(&expected_spans[4], 32000000, 3, 1, 4);

    ResultSet expected;
    expected.n = 5;
    expected.arr = expected_spans;

    check_calc_result("0 1|32000000 31000123|1000 0|31000123 32000000|32000000",
                      max_entity_id, expected);
}

void test_calc_7(void)
{
    printf("Testing calc() [7]\n");
    uint32_t max_entity_id = 32000000;

    EntitySpan expected_spans[5];
    set_entity_span(&expected_spans[0], 0, 2, 0, 6);
    set_entity_span(&expected_spans[1], 1, 1, 0, 0);
    set_entity_span(&expected_spans[2], 1000, 1, 2, 2);
    set_entity_span(&expected_spans[3], 31000123, 2, 1, 3);
    set_entity_span(&expected_spans[4], 32000000, 3, 1, 4);

    ResultSet expected;
    expected.n = 5;
    expected.arr = expected_spans;

    check_calc_result("0 1||||3|1000 0|31000123 32000000|32000000",
                      max_entity_id, expected);
}

int main(void)
{
    printf("Running unit tests ...\n");
    test_allocate_and_initalise_array();
    test_update_1();
    test_update_2();
    test_collect_1();
    test_collect_2();
    test_calc_1();
    test_calc_2();
    test_calc_3();
    test_calc_4();
    test_calc_5();
    test_calc_6();
    test_calc_7();
}