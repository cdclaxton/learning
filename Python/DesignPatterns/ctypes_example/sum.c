#include <stdio.h>
#include <stdlib.h>

int calcSum(int length, int *values)
{
    int total = 0;

    for (int i = 0; i < length; i++)
    {
        total += values[i];
    }

    return total;
}

typedef struct
{
    int length;
    double *values;
} Dataset;

Dataset *makeDataset(int length)
{
    Dataset *dataset = malloc(sizeof(Dataset));
    if (dataset == NULL)
    {
        return NULL;
    }

    dataset->length = length;
    dataset->values = malloc(sizeof(double) * length);

    for (int i = 0; i < length; i++)
    {
        dataset->values[i] = (double)rand() / RAND_MAX;
    }

    return dataset;
}

void freeDataset(Dataset *dataset)
{
    free(dataset->values);
    free(dataset);
}