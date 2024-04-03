#include <stdint.h>

#define MAXIMUM_ENTITY_ID_WIDTH 21
#define MAXIMUM_MESSAGE_LENGTH 120

typedef struct
{
    int16_t n;    // Number of tokens that match the entity ID or -1 if not used
    uint8_t *arr; // Array of matching positions
} DenseEntityPositions;

typedef struct
{
    uint32_t entity_id; // Entity ID
    uint8_t n;          // Number of tokens that match the entity ID
    uint8_t *arr;       // Array of matching positions
} EntityPositions;

typedef struct
{
    uint32_t n;                                     // Number of entity matches;
    EntityPositions *results;                       // Results for each entity
    char error_message[MAXIMUM_MESSAGE_LENGTH + 1]; // Error message
} SparsePositionResults;

// Returns the token positions in which the entity matches where the entity
// occurs at least `min_count` times. The maximum entity ID is `max_entity_id`.
SparsePositionResults positions(char *str,
                                uint32_t max_entity_id,
                                uint8_t min_count);

// Counts the occurrences of each entity in the string.
uint8_t *count_occurrences(char *str,
                           uint32_t max_entity_id);

// Initialise the dense entity positions results given the `counts` of each
// entity ID. An entity is only processed if it occurs at least `min_count`
// times.
DenseEntityPositions *initialise_position_results(uint8_t *counts,
                                                  uint32_t max_entity_id,
                                                  uint8_t min_count);

// Walk through the string `str` and record the positions of the entities
// that occur with a minimum count of `min_count`.
DenseEntityPositions *populate_position_results(char *str,
                                                uint32_t max_entity_id,
                                                uint8_t min_count,
                                                uint8_t *counts);

// Convert the dense entity positions to a sparse representation, thus removing
// entities that have an insufficient count.
SparsePositionResults compact(DenseEntityPositions *results,
                              uint32_t max_entity_id);

// Free the dynamically allocated memory for a DenseEntityPositions struct with
// a maximum entity ID of `max_entity_id`.
void free_dense_entity_positions(DenseEntityPositions *positions,
                                 uint32_t max_entity_id);

// Free the dynamically allocated memory for a SparsePositionResults struct.
void free_sparse_position_results(SparsePositionResults *sparse_results);