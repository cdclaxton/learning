#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void expLogMessage(double *logMessage,
                   int length,
                   double *result)
{
    for (int i = 0; i < length; i++)
    {
        *(result + i) = exp(logMessage[i]);
    }
}

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

void sumThreeLogMessages(double *logMessage1,
                         double *logMessage2,
                         double *logMessage3,
                         int length,
                         double *result)
{
    for (int i = 0; i < length; i++)
    {
        *(result + i) = *(logMessage1 + i) + *(logMessage2 + i) + *(logMessage3 + i);
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

void logSumProductForStates(int numStates,
                            double *g,
                            double *logVariableToFactorMessage,
                            double *result)
{
    for (int i = 0; i < numStates; i++)
    {
        result[i] = logSumProduct(i, g, numStates, logVariableToFactorMessage);
    }
}

void matrixRow(double *matrix,
               int row,
               int nColumns,
               double *result)
{
    for (int i = 0; i < nColumns; i++)
    {
        *(result + i) = matrix[row * nColumns + i];
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
        *(result + i) = matrix[i * nColumns + column];
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

double sumVector(double *vector, int length)
{
    double total = 0.0;

    for (int i = 0; i < length; i++)
    {
        total += vector[i];
    }

    return total;
}

void scaleVector(double *vector,
                 int length,
                 double c,
                 double *result)
{
    for (int i = 0; i < length; i++)
    {
        result[i] = vector[i] / c;
    }
}

void marginalFactors(double *logMessage1,
                     double *logMessage2,
                     double *logMessage3,
                     int length,
                     int nMessages,
                     double *result)
{
    double *lambda_x = (double *)malloc(length * sizeof(double));
    if (lambda_x == NULL)
    {
        perror("Failed to allocate memory for lambda_x");
        exit(1);
    }

    if (nMessages == 2)
    {
        sumLogMessages(logMessage1, logMessage2, length, lambda_x);
    }
    else if (nMessages == 3)
    {
        sumThreeLogMessages(logMessage1, logMessage2, logMessage3, length, lambda_x);
    }
    else
    {
        perror("Invalid number of messages");
        exit(1);
    }

    double *mu_x = (double *)malloc(length * sizeof(double));
    if (mu_x == NULL)
    {
        perror("Failed to allocate memory for mu_x");
        exit(1);
    }

    expLogMessage(lambda_x, length, mu_x);
    double total = sumVector(mu_x, length);

    scaleVector(mu_x, length, total, result);

    free(lambda_x);
    free(mu_x);
}

void setMatrixColumn(double *matrix,
                     int nRows,
                     int nCols,
                     double *vector,
                     int columnIndex)
{
    for (int i = 0; i < nRows; i++)
    {
        matrix[i * nCols + columnIndex] = vector[i];
    }
}