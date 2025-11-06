#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "factor.h"
#include "permutations.h"
#include "sum_product_utilities.h"

void testBitState()
{
    // 2-bits for the value
    // Index: 0 1
    //        0 0 = 0
    //        0 1 = 1
    //        1 0 = 2
    //        1 1 = 3
    assert(bitState(0, 0) == 0);
    assert(bitState(0, 1) == 0);
    assert(bitState(1, 0) == 1);
    assert(bitState(1, 1) == 0);
    assert(bitState(2, 0) == 0);
    assert(bitState(2, 1) == 1);
    assert(bitState(3, 0) == 1);
    assert(bitState(3, 1) == 1);

    // 3-bits for the value
    assert(bitState(6, 0) == 0);
    assert(bitState(6, 1) == 1);
    assert(bitState(6, 2) == 1);
}

void testSetStates()
{
    char actual1[1];
    setStates(1, actual1, 1);
    char expected1[] = {1};
    assert(statesEqual(expected1, actual1, 1) == true);

    char actual2[3];
    setStates(5, actual2, 3);
    char expected2[] = {1, 0, 1};
    assert(statesEqual(expected2, actual2, 3) == true);

    // Note how the states are in reverse order
    setStates(6, actual2, 3);
    char expected3[] = {0, 1, 1};
    assert(statesEqual(expected3, actual2, 3) == true);
}

void testCloneStates()
{
    char states[] = {1, 1, 0};
    char copy[3];
    cloneStates(states, copy, 3);
    assert(statesEqual(states, copy, 3));

    // Mutate the source state and check the destination state is unaffected
    states[0] = 0;
    char expected[] = {1, 1, 0};
    assert(statesEqual(copy, expected, 3));
}

void testOneFactor()
{
    assert(oneFactor(false, 0.2, 0.5) == 0.2);
    assert(oneFactor(true, 0.2, 0.5) == 0.5);
}

void testTwoFactor()
{
    double notX1notX2 = 0.2;
    double notX1X2 = 0.3;
    double x1NotX2 = 0.4;
    double x1X2 = 0.5;

    assert(twoFactor(false, false,
                     notX1notX2,
                     notX1X2,
                     x1NotX2,
                     x1X2) == notX1notX2);

    assert(twoFactor(false, true,
                     notX1notX2,
                     notX1X2,
                     x1NotX2,
                     x1X2) == notX1X2);

    assert(twoFactor(true, false,
                     notX1notX2,
                     notX1X2,
                     x1NotX2,
                     x1X2) == x1NotX2);

    assert(twoFactor(true, true,
                     notX1notX2,
                     notX1X2,
                     x1NotX2,
                     x1X2) == x1X2);
}

void testNumberOfPermutations()
{
    assert(numberOfPermutations(1, 2) == 2);
    assert(numberOfPermutations(2, 2) == 4);
    assert(numberOfPermutations(3, 2) == 8);
    assert(numberOfPermutations(1, 3) == 3);
    assert(numberOfPermutations(2, 3) == 9);
}

void testIndex()
{
    // 1x2 matrix
    // [0 1]
    assert(matrixIndex(0, 0, 2) == 0);
    assert(matrixIndex(0, 1, 1) == 1);

    // 2x1 matrix
    // [0]
    // [1]
    assert(matrixIndex(0, 0, 1) == 0);
    assert(matrixIndex(1, 0, 1) == 1);

    // 2x2 matrix
    // [0, 1]
    // [2, 3]
    assert(matrixIndex(0, 0, 2) == 0);
    assert(matrixIndex(0, 1, 2) == 1);
    assert(matrixIndex(1, 0, 2) == 2);
    assert(matrixIndex(1, 1, 2) == 3);
}

bool matricesEqual(int *matrix1,
                   int *matrix2,
                   int nRows,
                   int nCols)
{
    for (int i = 0; i < nRows; i++)
    {
        for (int j = 0; j < nCols; j++)
        {
            if (matrix1[matrixIndex(i, j, nCols)] != matrix2[matrixIndex(i, j, nCols)])
            {
                printf("Matrix 1:\n");
                printMatrix(matrix1, nRows, nCols);
                printf("\n");
                printf("Matrix 2:\n");
                printMatrix(matrix2, nRows, nCols);
                printf("\n");

                return false;
            }
        }
    }
    return true;
}

void testSinglePermutation(int nElements,
                           int nStates,
                           int *expected)
{
    int nPermutations = numberOfPermutations(nElements, nStates);

    // Allocate memory for the actual permutations
    int *actual = (int *)malloc(nPermutations * nElements * sizeof(int));
    assert(actual != NULL);

    // Calculate permutations
    permutations(nElements, nStates, actual);

    // Check the result
    assert(matricesEqual(expected, actual, nPermutations, nElements) == true);

    // Free the allocated space
    free(actual);
}

void testPermutations()
{
    // 1 element, 2 states
    int expected1[1][2] = {0, 1};
    testSinglePermutation(1, 2, &expected1[0][0]);

    // 2 elements, 2 states
    int expected2[4][2] = {{0, 0},
                           {0, 1},
                           {1, 0},
                           {1, 1}};
    testSinglePermutation(2, 2, &expected2[0][0]);

    // 3 elements, 2 states
    int expected3[8][3] = {{0, 0, 0},
                           {0, 0, 1},
                           {0, 1, 0},
                           {0, 1, 1},
                           {1, 0, 0},
                           {1, 0, 1},
                           {1, 1, 0},
                           {1, 1, 1}};
    testSinglePermutation(3, 2, &expected3[0][0]);

    // 1 element, 3 states
    int expected4[1][3] = {0, 1, 2};
    testSinglePermutation(1, 3, &expected4[0][0]);

    // 2 elements, 3 states
    int expected5[9][2] = {{0, 0},
                           {0, 1},
                           {0, 2},
                           {1, 0},
                           {1, 1},
                           {1, 2},
                           {2, 0},
                           {2, 1},
                           {2, 2}};
    testSinglePermutation(2, 3, &expected5[0][0]);
}

bool messagesEqual(double *message1,
                   double *message2,
                   int length)
{
    for (int i = 0; i < length; i++)
    {
        double delta = fabs(message1[i] - message2[i]);
        if (delta > 1e-6)
        {
            return false;
        }
    }
    return true;
}

void testMessagesEqual()
{
    double message1[3] = {1.0, 2.0, 3.0};
    double message2[3] = {1.0, 2.0, 3.1};

    assert(messagesEqual(message1, message1, 3) == true);
    assert(messagesEqual(message1, message2, 3) == false);
}

void testCalcLogMessage()
{
    double message[3] = {0.2, 0.5, 0.3};
    double actual[3];
    double expected[3] = {log(0.2), log(0.5), log(0.3)};

    calcLogMessage(message, 3, actual);
    assert(messagesEqual(expected, actual, 3) == true);
}

void testSumLogMessages()
{
    double message1[3] = {log(0.2), log(0.5), log(0.3)};
    double message2[3] = {log(0.1), log(0.2), log(0.7)};
    double expected[3] = {
        log(0.2) + log(0.1),
        log(0.5) + log(0.2),
        log(0.3) + log(0.7)};
    double actual[3];
    sumLogMessages(message1, message2, 3, actual);
    assert(messagesEqual(expected, actual, 3) == true);
}

void testCopyMessage()
{
    double message1[3] = {log(0.2), log(0.5), log(0.3)};
    double actual[3];
    copyLogMessage(message1, 3, actual);
    assert(messagesEqual(message1, actual, 3) == true);
}

void testMatrixRow()
{
    double matrix[3][4] = {{0.6, 0.2, 0.0, 0.2},
                           {0.2, 0.6, 0.1, 0.1},
                           {0, 0.1, 0.6, 0.3}};

    // Row 1
    double expected1[4] = {0.6, 0.2, 0.0, 0.2};
    double actual1[4];
    matrixRow(matrix[0], 0, 4, actual1);
    assert(messagesEqual(expected1, actual1, 4) == true);

    // Row 2
    double expected2[4] = {0.2, 0.6, 0.1, 0.1};
    double actual2[4];
    matrixRow(matrix[0], 1, 4, actual2);
    assert(messagesEqual(expected2, actual2, 4) == true);

    // Row 3
    double expected3[4] = {0, 0.1, 0.6, 0.3};
    double actual3[4];
    matrixRow(matrix[0], 2, 4, actual3);
    assert(messagesEqual(expected3, actual3, 4) == true);
}

void testMatrixColumn()
{
    double matrix[3][4] = {{0.6, 0.2, 0.0, 0.2},
                           {0.2, 0.6, 0.1, 0.1},
                           {0, 0.1, 0.6, 0.3}};

    // Column 1
    double expected1[3] = {0.6, 0.2, 0.0};
    double actual1[3] = {0, 0, 0};
    matrixColumn(matrix[0], 0, 3, 4, actual1);
    assert(messagesEqual(expected1, actual1, 3) == true);

    // Column 2
    double expected2[3] = {0.2, 0.6, 0.1};
    double actual2[3] = {0, 0, 0};
    matrixColumn(matrix[0], 1, 3, 4, actual2);
    assert(messagesEqual(expected2, actual2, 3) == true);
}

int main(void)
{
    printf("Running tests ...\n");

    // Utilities
    testBitState();
    testSetStates();
    testCloneStates();

    // Factor tests
    testOneFactor();
    testTwoFactor();

    // Permutations
    testNumberOfPermutations();
    testIndex();
    testPermutations();

    // Sum-product utilities
    testMessagesEqual();
    testCalcLogMessage();
    testSumLogMessages();
    testCopyMessage();
    testMatrixRow();
    testMatrixColumn();

    printf("Tests pass\n");
}