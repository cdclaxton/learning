#include <math.h>
#include <stdio.h>

int numberOfPermutations(int N, int M)
{
    return (int)pow(M, N);
}

int matrixIndex(int rowIndex,
                int colIndex,
                int nColumns)
{
    return rowIndex * nColumns + colIndex;
}

void permutations(int N, int M, int *matrix)
{
    int n = numberOfPermutations(N, M);

    // Walk through each permutation
    for (int i = 0; i < n; i++)
    {
        // Make a copy
        int value = i;

        // Walk through each element
        for (int element = 0; element < N; element++)
        {
            //         0    1        N-2 N-1
            // Index [N-1, N-2, ...,  1, 0  ]
            int idx = N - element - 1;

            int positionalValue = (int)pow(M, idx);

            if (value >= positionalValue)
            {
                matrix[matrixIndex(i, element, N)] = value / positionalValue;
                value = value % positionalValue;
            }
            else
            {
                matrix[matrixIndex(i, element, N)] = 0;
            }
        }
    }
}

void printMatrix(int *matrix,
                 int nRows,
                 int nCols)
{
    for (int i = 0; i < nRows; i++)
    {
        for (int j = 0; j < nCols; j++)
        {
            printf("%d ", matrix[matrixIndex(i, j, nCols)]);
        }
        printf("\n");
    }
}