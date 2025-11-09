#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"

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

// Note that it is assumed that matrix g is symmetric.
double logSumProduct(int factorState,
                     bool knownFactorIsRow,
                     double *g, // N_LANES x N_LANES matrix
                     int numStates,
                     double *logVariableToFactorMessage)
{
    double total = 0.0;

    for (int i = 0; i < numStates; i++)
    {
        int idx;
        if (knownFactorIsRow == true)
        {
            idx = matrixIndex(factorState, i, numStates);
        }
        else
        {
            idx = matrixIndex(i, factorState, numStates);
        }

        total += g[idx] * exp(logVariableToFactorMessage[i]);
    }

    return log(total);
}

void logSumProductForStates(int numStates,
                            bool knownFactorIsRow,
                            double *g, // N_LANES x N_LANES matrix
                            double *logVariableToFactorMessage,
                            double *result)
{
    for (int i = 0; i < numStates; i++)
    {
        result[i] = logSumProduct(i,
                                  knownFactorIsRow,
                                  g,
                                  numStates,
                                  logVariableToFactorMessage);
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

// Returns the unnormalised joint probability.
// p(x) = (1/Z) \prod_{i=0}^{N-1} f_i(x_i) \prod_{i=0}^{N-2} g_i(x_i, x_{i+1})
double jointProbability(double *observations, // nLanes x nTimesteps
                        double *gTheta,       // nLanes x nLanes
                        int *state,           // nLanes
                        int nLanes,
                        int nTimesteps)
{
    double total = 0.0;

    for (int xi = 0; xi < nTimesteps; xi++)
    {
        // Lane at the i(th) timestep
        int lane = state[xi];

        int idx = matrixIndex(lane, xi, nTimesteps);
        total += log(observations[idx]);
    }

    // Pairs
    for (int xi = 0; xi < nTimesteps - 1; xi++)
    {
        // Lane transition between timesteps
        int lane1 = state[xi];
        int lane2 = state[xi + 1];
        int idx = matrixIndex(lane1, lane2, nLanes);
        total += log(gTheta[idx]);
    }

    return exp(total);
}

void printIntVector(int *vector,
                    int nElements)
{

    printf("[ ");
    for (int i = 0; i < nElements; i++)
    {
        printf("%d ", vector[i]);
    }
    printf("]\n");
}

double marginal(double *observations, // nLanes x nTimesteps
                double *gTheta,       // nLanes x nLanes
                int xi,
                int lane,
                int *permutations,
                int nPermutations,
                int nLanes,
                int nTimesteps)
{
    double total = 0.0;

    // Walk through each permutation
    for (int i = 0; i < nPermutations; i++)
    {
        if (permutations[matrixIndex(i, xi, nTimesteps)] == lane)
        {
            total += jointProbability(observations,
                                      gTheta,
                                      permutations + i * nTimesteps,
                                      nLanes,
                                      nTimesteps);
        }
    }
    return total;
}