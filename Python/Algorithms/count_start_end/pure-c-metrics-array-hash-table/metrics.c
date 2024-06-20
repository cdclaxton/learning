#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "metrics.h"

ArrayHashTable new_array_hash_table(uint32_t n_buckets,
                                    uint32_t initial_capacity)
{
    if (n_buckets < 1)
    {
        printf("new_array_hash_table: Invalid number of buckets: %d\n",
               n_buckets);
        exit(-1);
    }

    if (initial_capacity < 1)
    {
        printf("new_array_hash_table: Invalid initial capacity: %d\n",
               initial_capacity);
        exit(-1);
    }

    ArrayHashTable table;

    // Set the number of buckets in the array hash table
    table.n_buckets = n_buckets;

    // Allocate memory for an array of buckets
    table.buckets = malloc(n_buckets * sizeof(Bucket));
    if (table.buckets == NULL)
    {
        printf("new_array_hash_table: Unable to allocate buckets\n");
        exit(-1);
    }

    // Initialise each bucket
    for (uint32_t i = 0; i < n_buckets; i++)
    {
        // Number of Items in the bucket
        table.buckets[i].n_items = 0;

        // Number of Items that can be stored in the bucket
        table.buckets[i].capacity = initial_capacity;

        // Allocate memory for the items in the bucket
        table.buckets[i].items = malloc(initial_capacity * sizeof(Item));
        if (table.buckets[i].items == NULL)
        {
            printf("new_array_hash_table: Failed to allocate memory for bucket %d\n", i);
            exit(-1);
        }
    }

    return table;
}

void free_array_hash_table(ArrayHashTable *hash_table)
{
    // Check the hash table is not null
    if (hash_table == NULL)
    {
        printf("free_array_hash_table: Hash table is NULL\n");
        exit(-1);
    }

    // Free each of the buckets
    for (uint32_t i = 0; i < hash_table->n_buckets; i++)
    {
        free((hash_table->buckets[i]).items);
    }

    // Free the array hash table buckets
    free(hash_table->buckets);
}

void display_table(ArrayHashTable *hash_table)
{
    // Check the hash table is not null
    if (hash_table == NULL)
    {
        printf("display_table: Hash table is NULL\n");
        exit(-1);
    }

    printf("Array hash table (%d buckets):\n", hash_table->n_buckets);
    for (uint32_t i = 0; i < hash_table->n_buckets; i++)
    {
        printf(" Bucket %d (num items: %d, capacity: %d):\n", i,
               (hash_table->buckets[i]).n_items,
               (hash_table->buckets[i]).capacity);

        if ((hash_table->buckets[i]).n_items == 0)
        {
            printf("  Empty bucket\n");
        }

        for (uint32_t j = 0; j < (hash_table->buckets[i]).n_items; j++)
        {
            printf("  Entity ID: %d, Count: %d, Start: %d, End: %d\n",
                   (hash_table->buckets[i]).items[j].entity_id,
                   (hash_table->buckets[i]).items[j].count,
                   (hash_table->buckets[i]).items[j].start_index,
                   (hash_table->buckets[i]).items[j].end_index);
        }
    }
}

uint32_t bucket_index(uint32_t n_buckets, uint32_t entity_id)
{
    int index = entity_id % n_buckets;
    assert(index >= 0 && index < n_buckets);

    return index;
}

void update_item(ArrayHashTable *hash_table,
                 uint32_t entity_id,
                 uint8_t index)
{
    // Check the hash table is not null
    if (hash_table == NULL)
    {
        printf("update_item: Hash table is NULL\n");
        exit(-1);
    }

    if (entity_id < 0)
    {
        printf("update_item: Entity ID is invalid: %d\n", entity_id);
        exit(-1);
    }

    if (index < 0)
    {
        printf("update_item: Index is invalid: %d\n", index);
        exit(-1);
    }

    // Get the bucket index for the entity ID
    uint32_t idx = bucket_index(hash_table->n_buckets, entity_id);

    // Look for an Item in the Bucket with the required entity ID
    uint32_t item_index = 0;
    uint8_t found = 0;
    for (uint32_t i = 0; i < hash_table->buckets[idx].n_items; i++)
    {
        if (hash_table->buckets[idx].items[i].entity_id == entity_id)
        {
            item_index = i;
            found = 1;
            break;
        }
    }

    // If the Item with the matching entity ID has been found then
    // update the Item
    if (found == 1)
    {
        hash_table->buckets[idx].items[item_index].count += 1;
        hash_table->buckets[idx].items[item_index].end_index = index;
        return;
    }

    // An Item for the entity doesn't yet exist. Check there is space for
    // a new Item
    if (hash_table->buckets[idx].n_items == hash_table->buckets[idx].capacity)
    {
        hash_table->buckets[idx].capacity = hash_table->buckets[idx].capacity * 2;
        hash_table->buckets[idx].items = realloc(hash_table->buckets[idx].items,
                                                 hash_table->buckets[idx].capacity * sizeof(Item));
        if (hash_table->buckets[idx].items == NULL)
        {
            printf("update_item: Failed to allocate space for items in bucket");
            exit(-1);
        };
    }

    // Index of the new Item
    uint32_t new_item_index = hash_table->buckets[idx].n_items;

    hash_table->buckets[idx].items[new_item_index].entity_id = entity_id;
    hash_table->buckets[idx].items[new_item_index].count = 1;
    hash_table->buckets[idx].items[new_item_index].start_index = index;
    hash_table->buckets[idx].items[new_item_index].end_index = index;

    // Increment the number of Items in the Bucket
    hash_table->buckets[idx].n_items += 1;
}

FilteredItems items_meeting_threshold(ArrayHashTable *hash_table,
                                      uint8_t min_count,
                                      uint32_t initial_capacity)
{
    if (hash_table == NULL)
    {
        printf("items_meeting_threshold: Hash table is NULL\n");
        exit(-1);
    }

    if (min_count < 0)
    {
        printf("items_meeting_threshold: Min count is invalid: %d\n",
               min_count);
        exit(-1);
    }

    if (initial_capacity <= 0)
    {
        printf("items_meeting_threshold: Initial capacity is invalid: %d\n",
               initial_capacity);
        exit(-1);
    }

    // Dynamicaly allocate space for the items
    FilteredItems filtered_items;
    filtered_items.n_items = 0;
    filtered_items.items = (Item *)malloc(initial_capacity * sizeof(Item));

    if (filtered_items.items == NULL)
    {
        printf("items_meeting_threshold: Failed to allocate space for items\n");
        exit(-1);
    }

    uint32_t max_items = initial_capacity;

    // Walk through each bucket in the array hash table
    for (uint32_t bucket_idx = 0; bucket_idx < hash_table->n_buckets; bucket_idx++)
    {
        // Walk through each item in the bucket
        for (uint32_t item_idx = 0; item_idx < hash_table->buckets[bucket_idx].n_items; item_idx++)
        {
            // If the Item has a count below the required threshold, then move
            // onto the next item
            if (hash_table->buckets[bucket_idx].items[item_idx].count < min_count)
            {
                continue;
            }

            // Ensure there is sufficient space in the array of Items for the
            // new item to be added
            if (filtered_items.n_items == max_items)
            {
                max_items *= 2;
                filtered_items.items = (Item *)realloc(filtered_items.items, max_items * sizeof(Item));
                if (filtered_items.items == NULL)
                {
                    printf("items_meeting_threshold: Failed to allocate space for filtered items");
                    exit(-1);
                }
            }

            uint32_t idx = filtered_items.n_items;
            filtered_items.items[idx].entity_id = hash_table->buckets[bucket_idx].items[item_idx].entity_id;
            filtered_items.items[idx].count = hash_table->buckets[bucket_idx].items[item_idx].count;
            filtered_items.items[idx].start_index = hash_table->buckets[bucket_idx].items[item_idx].start_index;
            filtered_items.items[idx].end_index = hash_table->buckets[bucket_idx].items[item_idx].end_index;

            filtered_items.n_items += 1;
        }
    }

    return filtered_items;
}

void display_filtered_items(FilteredItems *items)
{
    if (items == NULL)
    {
        printf("display_filtered_items: items is NULL\n");
        exit(-1);
    }

    printf("Filtered items (%d items):\n", items->n_items);
    for (uint32_t i = 0; i < items->n_items; i++)
    {
        printf(" Item %d: Entity ID: %d, Count: %d, Start: %d, End: %d\n",
               i,
               items->items[i].entity_id,
               items->items[i].count,
               items->items[i].start_index,
               items->items[i].end_index);
    }
}

void free_filtered_items(FilteredItems *filtered_items)
{
    free(filtered_items->items);
}

FilteredItems calc(char *str,
                   uint32_t n_buckets,
                   uint32_t initial_capacity,
                   uint8_t min_count,
                   uint32_t filtered_initial_capacity)
{
    uint32_t end = 0;
    uint8_t batch_idx = 0;
    char temp[MAXIMUM_ENTITY_ID_WIDTH];
    uint8_t temp_idx = 0;
    uint32_t entity_id;

    // Make an array hash table
    ArrayHashTable ht = new_array_hash_table(n_buckets,
                                             initial_capacity);

    while ((str[end]) != '\0')
    {
        if (str[end] == ' ' || str[end] == '|')
        {
            if (temp_idx > 0)
            {
                entity_id = atoi(temp);
                update_item(&ht,
                            entity_id,
                            batch_idx);
            }

            temp_idx = 0;
            temp[0] = '\0';
        }
        else
        {
            temp[temp_idx] = str[end];
            temp[temp_idx + 1] = '\0';
            temp_idx++;
        }

        if (str[end] == '|')
        {
            batch_idx++;
        }

        end++;
    }

    if (temp_idx > 0)
    {
        entity_id = atoi(temp);
        update_item(&ht,
                    entity_id,
                    batch_idx);
    }

    // Filter the Items to retain those with a sufficient count
    FilteredItems fi = items_meeting_threshold(&ht,
                                               min_count,
                                               filtered_initial_capacity);

    // Free the dynamically allocated memory for the array hash table
    free_array_hash_table(&ht);

    return fi;
}

int main(void)
{
    // ArrayHashTable ht;
    // ht = new_array_hash_table(2, 1);
    // printf("Initial hash table:\n");
    // display_table(&ht);

    // update_item(&ht, 100, 0);
    // update_item(&ht, 100, 1);
    // update_item(&ht, 200, 0);
    // update_item(&ht, 300, 2);
    // update_item(&ht, 41, 3);

    // display_table(&ht);

    // FilteredItems fi = items_meeting_threshold(&ht, 1, 1);
    // free_array_hash_table(&ht);

    // display_filtered_items(&fi);

    // FilteredItems fi = calc("2 6|6|6 2", 2, 5, 0, 1);
    FilteredItems fi = calc("0 5 11 13 15 18 19 20 21 23 24 26 28 29 30 31 32 34 35 37 39 40 41 42 46 49 50 51 53 54 58 60 61 63 65 67 70 73 74 77 82 84 87 89 91 92 94 97 98 99|0 1 2 3 4 7 8 10 11 12 13 16 17 19 20 21 23 27 28 29 31 36 37 43 44 45 48 50 53 54 55 56 57 66 68 70 71 72 73 76 79 80 81 82 87 88 91 94 96", 10, 5, 0, 1);
    display_filtered_items(&fi);
    free_filtered_items(&fi);
};