#include <assert.h>
#include <stdio.h>
#include "factor.h"

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

    printf("Tests pass\n");
}