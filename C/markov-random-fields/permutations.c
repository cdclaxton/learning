#include <math.h>
#include <stdio.h>
#include "matrix.h"

int numberOfPermutations(int N, int M)
{
    return (int)pow(M, N);
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
