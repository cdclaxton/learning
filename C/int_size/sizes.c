#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define n 5
#define m 100

int main(void)
{
    int *ptr;

    printf("Size of int: %d bytes\n", sizeof(int));
    printf("Size of char: %d bytes\n", sizeof(char));

    // Allocate memory for an array of char
    ptr = (int *)malloc(n * sizeof(char));
    for (int i = 0; i < n; i++)
    {
        ptr[i] = 0;
    }

    // Set the seed of the random number generator
    srand(time(NULL));

    // Randomly allocate values to the array
    int idx;
    for (int i = 0; i < m; i++)
    {
        idx = rand() % n;
        ptr[idx] += 1;
    }

    // Display the array
    int total = 0;
    for (int i = 0; i < n; i++)
    {
        printf("Element %d: %d\n", i, ptr[i]);
        total += ptr[i];
    }

    printf("Total: %d\n", total);

    // Free the allocated memory
    free(ptr);

    return EXIT_SUCCESS;
}