// Assumptions:
// * Entity IDs fit into 32 bits
// * Number of tokens < 255

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "metrics.h"

#define MAXIMUM_ENTITY_ID_WIDTH 21

int main(void)
{
    ResultSet r = calc("1 2 3||||1 2 3|2 3|2 3", 4, 2);
    printResultSet(r);

    return EXIT_SUCCESS;
}

// allocateAndInitaliseArray allocates and initialises an array with zero values.
uint8_t *allocateAndInitaliseArray(uint32_t numElements)
{
    // Allocate memory for the array
    uint8_t *arr = (uint8_t *)calloc(numElements, sizeof(uint32_t));
    if (arr == NULL)
    {
        printf("Failed to allocate memory with %d elements\n", numElements);
        return NULL;
    }

    return arr;
}

void printArray(uint8_t *arr, uint8_t numElements)
{
    printf("[");
    for (uint8_t i = 0; i < numElements; i++)
    {
        if (i < (numElements - 1))
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

void update(uint8_t batch, uint32_t entityId, uint32_t maxEntityId,
            uint8_t *counts, uint8_t *starts, uint8_t *ends)
{
    if (entityId >= maxEntityId)
    {
        printf("Entity ID %d equal to or exceeds max entity ID %d\n", entityId, maxEntityId);
        exit(-1);
    }

    if (counts[entityId] == 0)
    {
        // First time the entity ID has been seen
        counts[entityId] = 1;
        starts[entityId] = batch;
        ends[entityId] = batch;
    }
    else
    {
        // Entity ID has been seen at least once before
        counts[entityId] += 1;
        ends[entityId] = batch;
    }
}

void printResultSet(ResultSet r)
{
    printf("Number of results: %d\n", r.n);
    for (uint8_t i = 0; i < r.n; i++)
    {
        printf("Entity ID: %d, Start: %d, End: %d\n",
               r.arr[i].entityId, r.arr[i].startIndex, r.arr[i].endIndex);
    }
}

ResultSet collect(uint8_t *counts, uint8_t *starts, uint8_t *ends, uint32_t maxEntityId, uint8_t minCount)
{
    // Determine how many entity IDs were seen with the minimum required count
    uint32_t total = 0;
    for (uint32_t i = 0; i < maxEntityId; i++)
    {
        if (counts[i] >= minCount)
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
    for (uint32_t i = 0; i < maxEntityId; i++)
    {
        if (counts[i] >= minCount)
        {
            r.arr[elementIdx].entityId = i;
            r.arr[elementIdx].startIndex = starts[i];
            r.arr[elementIdx].endIndex = ends[i];
            elementIdx += 1;
        }
    }

    // Return the result set
    return r;
};

ResultSet calc(char *str, uint32_t maxEntityId, uint8_t minCount)
{
    uint32_t end = 0;
    uint8_t batchIdx = 0;
    char temp[MAXIMUM_ENTITY_ID_WIDTH];
    uint8_t tempIdx = 0;
    uint32_t entityId;

    // Allocate memory for the counts
    uint8_t *counts = allocateAndInitaliseArray(maxEntityId);

    // Allocate memory for the start indices
    uint8_t *starts = allocateAndInitaliseArray(maxEntityId);

    // Allocate memory for the end indices
    uint8_t *ends = allocateAndInitaliseArray(maxEntityId);

    while ((str[end]) != '\0')
    {
        if (str[end] == ' ' || str[end] == '|')
        {
            if (tempIdx > 0)
            {
                entityId = atoi(temp);
                update(batchIdx, entityId, maxEntityId, counts, starts, ends);
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
        entityId = atoi(temp);
        update(batchIdx, entityId, maxEntityId, counts, starts, ends);
    }

    // Collect the results that have the required minimum number of entries
    ResultSet r;
    r = collect(counts, starts, ends, maxEntityId, minCount);

    // Free memory
    free(counts);
    free(starts);
    free(ends);

    return r;
}