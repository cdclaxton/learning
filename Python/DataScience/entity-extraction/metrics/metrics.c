// Assumptions:
// * Entity IDs fit into 32 bits
// * Number of tokens < 255

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "metrics.h"

#define MAXIMUM_ENTITY_ID_WIDTH 21

// int main(void)
// {
//     ResultSet r = calc("1 2 3||||1 2 3|2 3|2 3", 4, 2);
//     print_result_set(r);

//     return EXIT_SUCCESS;
// }

uint8_t *allocate_and_initialise_array(uint32_t num_elements)
{
    // Allocate memory for the array
    uint8_t *arr = (uint8_t *)calloc(num_elements, sizeof(uint32_t));
    if (arr == NULL)
    {
        printf("Failed to allocate memory with %d elements\n", num_elements);
        return NULL;
    }

    return arr;
}

void print_array(uint8_t *arr, uint8_t num_elements)
{
    printf("[");
    for (uint8_t i = 0; i < num_elements; i++)
    {
        if (i < (num_elements - 1))
        {
            printf("%d, ", arr[i]);
        }
        else
        {
            printf("%d", arr[i]);
        }
    }
    printf("]\n");
}

void update(uint8_t batch, uint32_t entity_id, uint32_t max_entity_id,
            uint8_t *counts, uint8_t *starts, uint8_t *ends)
{
    if (entity_id > max_entity_id)
    {
        printf("Entity ID %d exceeds max entity ID %d\n", entity_id, max_entity_id);
        exit(-1);
    }

    if (counts[entity_id] == 0)
    {
        // First time the entity ID has been seen
        counts[entity_id] = 1;
        starts[entity_id] = batch;
        ends[entity_id] = batch;
    }
    else
    {
        // Entity ID has been seen at least once before
        counts[entity_id] += 1;
        ends[entity_id] = batch;
    }
}

void print_entity_span(EntitySpan e)
{
    printf("Entity ID: %d, Count: %d, Start: %d, End: %d\n",
           e.entity_id,
           e.count,
           e.start_index,
           e.end_index);
}

void print_result_set(ResultSet r)
{
    printf("Number of results: %d\n", r.n);
    for (uint8_t i = 0; i < r.n; i++)
    {
        print_entity_span(r.arr[i]);
    }
}

ResultSet collect(uint8_t *counts,
                  uint8_t *starts,
                  uint8_t *ends,
                  uint32_t max_entity_id,
                  uint8_t min_count)
{
    // Determine how many entity IDs were seen with the minimum required count
    uint32_t total = 0;
    for (uint32_t i = 0; i <= max_entity_id; i++)
    {
        if (counts[i] >= min_count)
        {
            total += 1;
        }
    }

    if (total == 0)
    {
        ResultSet r =
            {
                0,
                NULL};
        return r;
    }

    // Allocate memory for the array of EntitySpans
    ResultSet r;
    r.n = total;
    r.arr = malloc(sizeof(EntitySpan) * total);
    if (r.arr == NULL)
    {
        printf("Unable to allocate space for ResultSet with %d elements\n", total);
        exit(-1);
    }

    // Build the results
    uint32_t elementIdx = 0;
    for (uint32_t i = 0; i <= max_entity_id; i++)
    {
        if (counts[i] >= min_count)
        {
            r.arr[elementIdx].entity_id = i;
            r.arr[elementIdx].count = counts[i];
            r.arr[elementIdx].start_index = starts[i];
            r.arr[elementIdx].end_index = ends[i];
            elementIdx += 1;
        }
    }

    // Return the result set
    return r;
};

ResultSet calc(char *str,
               uint32_t max_entity_id,
               uint8_t min_count)
{
    uint32_t end = 0;
    uint8_t batchIdx = 0;
    char temp[MAXIMUM_ENTITY_ID_WIDTH];
    uint8_t tempIdx = 0;
    uint32_t entity_id;

    // Allocate memory for the counts
    uint8_t *counts = allocate_and_initialise_array(max_entity_id + 1);

    // Allocate memory for the start indices
    uint8_t *starts = allocate_and_initialise_array(max_entity_id + 1);

    // Allocate memory for the end indices
    uint8_t *ends = allocate_and_initialise_array(max_entity_id + 1);

    while ((str[end]) != '\0')
    {
        if (str[end] == ' ' || str[end] == '|')
        {
            if (tempIdx > 0)
            {
                entity_id = atoi(temp);
                update(batchIdx, entity_id, max_entity_id, counts, starts, ends);
            }

            tempIdx = 0;
            temp[0] = '\0';
        }
        else
        {
            temp[tempIdx] = str[end];
            temp[tempIdx + 1] = '\0';
            tempIdx++;
        }

        if (str[end] == '|')
        {
            batchIdx++;
        }

        end++;
    }

    if (tempIdx > 0)
    {
        entity_id = atoi(temp);
        update(batchIdx, entity_id, max_entity_id, counts, starts, ends);
    }

    // Collect the results that have the required minimum number of entries
    ResultSet r;
    r = collect(counts, starts, ends, max_entity_id, min_count);

    // Free memory
    free(counts);
    free(starts);
    free(ends);

    return r;
}