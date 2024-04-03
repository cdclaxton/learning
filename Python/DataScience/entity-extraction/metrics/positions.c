#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "positions.h"

SparsePositionResults positions(char *str,
                                uint32_t max_entity_id,
                                uint8_t min_count)
{
    SparsePositionResults results;
    results.n = 0;

    // Check the parameters
    if (str == NULL)
    {
        strncpy(results.error_message, "Input string is null",
                MAXIMUM_MESSAGE_LENGTH);
        return results;
    }

    if (min_count == 0)
    {
        strncpy(results.error_message, "Minimum counts is zero",
                MAXIMUM_MESSAGE_LENGTH);
        return results;
    }

    // Count the number of times each entity occurs in the string
    uint8_t *counts = count_occurrences(str, max_entity_id);
    if (counts == NULL)
    {
        strncpy(results.error_message, "Failed to count occurrences",
                MAXIMUM_MESSAGE_LENGTH);
        return results;
    }

    // Create the position results for each entity that occurs with the required
    // number of times
    DenseEntityPositions *dense_results = populate_position_results(str,
                                                                    max_entity_id,
                                                                    min_count,
                                                                    counts);

    // Compact the results
    SparsePositionResults compact_results = compact(dense_results,
                                                    max_entity_id);

    // Free the dynamically allocated array of counts
    free(counts);

    // Free the dynamically allocated space for the dense entity positions
    free_dense_entity_positions(dense_results, max_entity_id);

    // Return the position results
    return compact_results;
}

uint8_t *count_occurrences(char *str,
                           uint32_t max_entity_id)
{
    // Dynamically allocate an array to hold the number of times each entity
    // occurs
    uint32_t num_elements = max_entity_id + 1;
    uint8_t *counts = (uint8_t *)calloc(num_elements, sizeof(uint8_t));
    if (counts == NULL)
    {
        printf("Failed to allocate memory with %d elements\n", num_elements);
    }

    // Walk through the string, counting the occurrences of the entities found
    uint32_t current = 0;
    uint8_t substring_index = 0;
    uint32_t entity_id;
    char temp[MAXIMUM_ENTITY_ID_WIDTH];

    while ((str[current]) != '\0')
    {
        if (str[current] == ' ' || str[current] == '|')
        {
            if (substring_index > 0)
            {
                entity_id = atoi(temp);
                if (entity_id > max_entity_id)
                {
                    printf("Entity ID %d > maximum entity ID %d\n",
                           entity_id, max_entity_id);
                    free(counts);
                    return NULL;
                }
                counts[entity_id] += 1;
            }

            substring_index = 0;
            temp[0] = '\0';
        }
        else
        {
            temp[substring_index] = str[current];
            temp[substring_index + 1] = '\0';
            substring_index++;
        }

        current++;
    }

    if (substring_index > 0)
    {
        entity_id = atoi(temp);
        if (entity_id > max_entity_id)
        {
            printf("Entity ID %d > maximum entity ID %d\n",
                   entity_id, max_entity_id);
            free(counts);
            return NULL;
        }
        counts[entity_id] += 1;
    }

    // Return the counts
    return counts;
}

DenseEntityPositions *initialise_position_results(uint8_t *counts,
                                                  uint32_t max_entity_id,
                                                  uint8_t min_count)
{
    DenseEntityPositions *ep = (DenseEntityPositions *)malloc((max_entity_id + 1) *
                                                              sizeof(EntityPositions));
    if (ep == NULL)
    {
        printf("Failed to allocate DenseEntityPositions");
        free(ep);
        return NULL;
    }

    for (uint32_t i = 0; i <= max_entity_id; i++)
    {
        if (counts[i] < min_count)
        {
            ep[i].n = -1;
            continue;
        }

        ep[i].n = 0;
        ep[i].arr = (uint8_t *)malloc(counts[i] * sizeof(uint8_t));
        if (ep[i].arr == NULL)
        {
            free_dense_entity_positions(ep, max_entity_id);
            return NULL;
        }
    }

    return ep;
}

DenseEntityPositions *populate_position_results(char *str,
                                                uint32_t max_entity_id,
                                                uint8_t min_count,
                                                uint8_t *counts)
{
    DenseEntityPositions *positions = initialise_position_results(counts,
                                                                  max_entity_id,
                                                                  min_count);

    // Walk through the string, recording the occurrences of the entities found
    uint8_t batch = 0;
    uint32_t current = 0;
    uint8_t substring_index = 0;
    uint32_t entity_id;
    char temp[MAXIMUM_ENTITY_ID_WIDTH];

    while ((str[current]) != '\0')
    {
        if (str[current] == ' ' || str[current] == '|')
        {
            if (substring_index > 0)
            {
                entity_id = atoi(temp);
                if (positions[entity_id].n >= 0)
                {
                    positions[entity_id].arr[positions[entity_id].n] = batch;
                    positions[entity_id].n++;
                }
            }

            substring_index = 0;
            temp[0] = '\0';
        }
        else
        {
            temp[substring_index] = str[current];
            temp[substring_index + 1] = '\0';
            substring_index++;
        }

        if (str[current] == '|')
        {
            batch++;
        }

        current++;
    }

    if (substring_index > 0)
    {
        entity_id = atoi(temp);
        if (positions[entity_id].n >= 0)
        {
            positions[entity_id].arr[positions[entity_id].n] = batch;
            positions[entity_id].n++;
        }
    }

    return positions;
}

void free_dense_entity_positions(DenseEntityPositions *positions,
                                 uint32_t max_entity_id)
{
    for (uint32_t i = 0; i < (max_entity_id + 1); i++)
    {
        if (positions[i].n > 0)
        {
            free(positions[i].arr);
        }
    }
}

void free_sparse_position_results(SparsePositionResults *sparse_results)
{
    for (uint32_t i = 0; i < sparse_results->n; i++)
    {
        free(sparse_results->results[i].arr);
    }
}

SparsePositionResults compact(DenseEntityPositions *results,
                              uint32_t max_entity_id)
{
    // Count how many of the dense results will be included in the sparse results
    SparsePositionResults sparse_results;
    sparse_results.n = 0;
    for (uint32_t i = 0; i < (max_entity_id + 1); i++)
    {
        if (results[i].n > 0)
        {
            sparse_results.n += 1;
        }
    }

    // Dynamically allocate space for the entity positions
    sparse_results.results = (EntityPositions *)malloc(sparse_results.n *
                                                       sizeof(EntityPositions));
    if (sparse_results.results == NULL)
    {
        strncpy(sparse_results.error_message,
                "Failed to allocate space",
                MAXIMUM_MESSAGE_LENGTH);
        return sparse_results;
    }

    uint32_t current_index = 0;
    for (uint32_t i = 0; i < (max_entity_id + 1); i++)
    {
        if (results[i].n < 1)
        {
            continue;
        }

        sparse_results.results[current_index].entity_id = i;
        sparse_results.results[current_index].n = results[i].n;
        sparse_results.results[current_index].arr = malloc(
            results[i].n * sizeof(uint8_t));
        memcpy(sparse_results.results[current_index].arr,
               results[i].arr,
               results[i].n * sizeof(uint8_t));

        current_index++;
    }

    sparse_results.error_message[0] = '\0';

    return sparse_results;
}