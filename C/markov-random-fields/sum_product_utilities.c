#include <math.h>
#include <stdio.h>

void calcLogMessage(double *message,
                    int length,
                    double *result)
{
    for (int i = 0; i < length; i++)
    {
        *(result + i) = log(*(message + i));
    }
}

void sumLogMessages(double *logMessage1,
                    double *logMessage2,
                    int length,
                    double *result)
{
    for (int i = 0; i < length; i++)
    {
        *(result + i) = *(logMessage1 + i) + *(logMessage2 + i);
    }
}

void copyLogMessage(double *logMessage,
                    int length,
                    double *result)
{
    for (int i = 0; i < length; i++)
    {
        *(result + i) = *(logMessage + i);
    }
}

double logSumProduct(int factorState,
                     double *g,
                     int numStates,
                     double *logVariableToFactorMessage)
{
    double total = 0.0;

    for (int i = 0; i < numStates; i++)
    {
        total += g[i] * exp(logVariableToFactorMessage[i]);
    }

    return log(total);
}

void matrixRow(double *matrix,
               int row,
               int nColumns,
               double *result)
{
    for (int i = 0; i < nColumns; i++)
    {
        *(result + i) = *(matrix + (row * nColumns + i));
    }
}

void matrixColumn(double *matrix,
                  int column,
                  int nRows,
                  int nColumns,
                  double *result)
{
    for (int i = 0; i < nRows; i++)
    {
        *(result + i) = *(matrix + i * nColumns + column);
    }
}

void printMessage(double *message,
                  int length)
{
    for (int i = 0; i < length; i++)
    {
        printf("%f ", *(message + i));
    }
}