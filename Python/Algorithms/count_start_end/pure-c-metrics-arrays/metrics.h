#include <stdint.h>

typedef struct
{
    uint32_t entityId;  // Entity ID
    uint8_t startIndex; // Batch start index
    uint8_t endIndex;   // Batch end index
} EntitySpan;

typedef struct
{
    uint8_t n;       // Number of EntitySpan structs
    EntitySpan *arr; // Array of EntitySpan structs
} ResultSet;

ResultSet calc(char *str, uint32_t maxEntityId, uint8_t minCount);

uint8_t *allocateAndInitaliseArray(uint32_t numElements);

void update(uint8_t batch, uint32_t entityId, uint32_t maxEntityId,
            uint8_t *counts, uint8_t *starts, uint8_t *ends);

ResultSet collect(uint8_t *counts, uint8_t *starts, uint8_t *ends, uint32_t maxEntityId, uint8_t minCount);

void printResultSet(ResultSet r);

void printArray(uint8_t *arr, uint8_t numElements);