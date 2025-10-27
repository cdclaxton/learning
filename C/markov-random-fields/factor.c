#include <stdbool.h>
#include <stdio.h>
#include <string.h>

char bitState(int value,
              char bitIndex)
{
    int x = 1 << bitIndex;
    return (value & x) > 0;
}

void setStates(int value,
               char *variables,
               int nVariables)
{
    for (int i = 0; i < nVariables; i++)
    {
        variables[i] = bitState(value, i);
    }
}

bool statesEqual(char *expected,
                 char *actual,
                 int nVariables)
{
    for (int i = 0; i < nVariables; i++)
    {
        if (expected[i] != actual[i])
        {
            return false;
        }
    }

    return true;
}

void cloneStates(char *source,
                 char *destination,
                 int nVariables)
{
    memcpy(destination, source, sizeof(char) * nVariables);
}

void statesString(char *states,
                  int nVariables,
                  char *resultString)
{
    for (int i = 0; i < nVariables; i++)
    {
        char stringForVariable[10];
        if (i < (nVariables - 1))
        {
            sprintf(stringForVariable, "x_%d=%d, ", i + 1, states[i]);
        }
        else
        {
            sprintf(stringForVariable, "x_%d=%d", i + 1, states[i]);
        }

        strcat(resultString, stringForVariable);
    }
}

double oneFactor(bool x1, double pNotX1, double pX1)
{
    if (x1)
    {
        return pX1;
    }

    return pNotX1;
}

double twoFactor(bool x1, bool x2, double notX1notX2, double notX1X2, double x1NotX2, double x1X2)
{
    if (!x1 && !x2)
    {
        return notX1notX2;
    }
    else if (!x1 && x2)
    {
        return notX1X2;
    }
    else if (x1 && !x2)
    {
        return x1NotX2;
    }

    return x1X2;
}