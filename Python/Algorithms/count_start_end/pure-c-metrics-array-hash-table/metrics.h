#include <stdint.h>

// Maximum number of characters in an entity ID
#define MAXIMUM_ENTITY_ID_WIDTH 21

typedef struct
{
    uint32_t entity_id;  // Entity ID
    uint8_t count;       // Number of times entity found
    uint8_t start_index; // Start token index of entity
    uint8_t end_index;   // End token index of entity
} Item;

typedef struct
{
    uint32_t n_items;  // Number of Items in bucket
    uint32_t capacity; // Capacity of the array of Items
    Item *items;       // Array of Items
} Bucket;

typedef struct
{
    uint32_t n_buckets; // Number of buckets
    Bucket *buckets;    // Array of buckets
} ArrayHashTable;

typedef struct
{
    uint32_t n_items; // Number of items
    Item *items;      // Array of items
} FilteredItems;

// Returns an initialised array hash table with `n_buckets` buckets. Each
// bucket has allocated space for `initial_capacity` Items.
ArrayHashTable new_array_hash_table(uint32_t n_buckets,
                                    uint32_t initial_capacity);

// Free dynamically allocated memory in an array hash table.
void free_array_hash_table(ArrayHashTable *hash_table);

// Update an item in the array hash table for an entity with id `entity_id` that
// matches token `index`.
void update_item(ArrayHashTable *hash_table,
                 uint32_t entity_id,
                 uint8_t index);

// Returns an array of Items where the `count` of the occurrences of the entity
// is equal to or above the threshold `min_count`.
FilteredItems items_meeting_threshold(ArrayHashTable *hash_table,
                                      uint8_t min_count,
                                      uint32_t initial_capacity);

// Free the dynamically allocated memory for the filtered items.
void free_filtered_items(FilteredItems *filtered_items);

// Prints the array hash table to the stdout.
void display_table(ArrayHashTable *hash_table);

// Returns the bucket index for an entity with ID `entity_id` given that there
// are `n_buckets` buckets in the array hash table.
uint32_t bucket_index(uint32_t n_buckets, uint32_t entity_id);

// Prints the filtered items to stdout.
void display_filtered_items(FilteredItems *items);

// Returns a filtered set of Items given an input string `str` of entity IDs
// and a minimum number of occurrences of an entity `min_count`. The function
// uses an array hash table with `n_buckets` buckets where each bucket has an
// initial capacity for `initial_capacity` Items. The Items with the required
// minimum number of occurrences are placed in an array and the initial capacity
// of the array is set to `filtered_initial_capacity`.
FilteredItems calc(char *str,
                   uint32_t n_buckets,
                   uint32_t initial_capacity,
                   uint8_t min_count,
                   uint32_t filtered_initial_capacity);
