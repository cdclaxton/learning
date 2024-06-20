#include <stdio.h>
#include <stdlib.h>

#define NUM_ITEMS 2

typedef struct
{
    int a;
    int b;
} Item;

typedef struct
{
    int n_items;
    Item *items;
} Container;

void display(Container *c)
{
    printf("Container (%d items):\n", c->n_items);
    for (int i = 0; i < c->n_items; i++)
    {
        printf(" Item %d: a=%d, b=%d\n", i, c->items[i].a, c->items[i].b);
    }
}

void set(Container *c)
{
    c->items[0].a = 30;
    c->items[0].b = 100;
    c->items[1].b = 200;
}

int main(void)
{

    Container c;
    c.n_items = NUM_ITEMS;
    c.items = (Item *)malloc(NUM_ITEMS * sizeof(Item));
    if (c.items == NULL)
    {
        printf("Failed to allocate memory\n");
        exit(-1);
    }
    printf("Initialising container\n");
    display(&c);

    printf("Modifying container\n");
    c.items[0].a = 20;
    c.items[1].b = 100;
    display(&c);

    printf("Setting\n");
    set(&c);
    display(&c);

    // Free memory allocated for Items
    free(c.items);
}