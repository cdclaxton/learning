#include <stdint.h>

typedef struct
{
    uint32_t entity_id;  // Entity ID
    uint8_t count;       // Number of times entity seen
    uint8_t start_index; // Batch start index
    uint8_t end_index;   // Batch end index
} EntitySpan;

typedef struct
{
    uint32_t n;      // Number of EntitySpan structs
    EntitySpan *arr; // Array of EntitySpan structs
} ResultSet;

// Calculate the EntitySpans in the string `str` where the entity occurs with a
// minimum count of `min_count`. The set of all entities has a maximum entity
// ID of `max_entity_id`.
ResultSet calc(char *str,
               uint32_t max_entity_id,
               uint8_t min_count);

// Allocate and initialise an array of `num_elements` elements where each
// element is of type `uint8_t`.
uint8_t *allocate_and_initialise_array(uint32_t num_elements);

// Update the entity counts, start indices (`starts`) and end indices (`ends`)
// for the entity with ID `entity_id`. The maximum entity ID in the dataset is
// set to `max_entity_id`. The batch (or token index) to which the entity occurs
// is set to `batch`.
void update(uint8_t batch,
            uint32_t entity_id,
            uint32_t max_entity_id,
            uint8_t *counts,
            uint8_t *starts,
            uint8_t *ends);

// Collect the EntitySpans for entities that occur with a minimum count of
// `min_count`.
ResultSet collect(uint8_t *counts,
                  uint8_t *starts,
                  uint8_t *ends,
                  uint32_t max_entity_id,
                  uint8_t min_count);

// Print an EntitySpan to stdout.
void print_entity_span(EntitySpan e);

// Print the ResultSet struct to stdout.
void print_result_set(ResultSet r);

// Print the array `arr` with `num_elements` elements to stdout.
void print_array(uint8_t *arr,
                 uint8_t num_elements);