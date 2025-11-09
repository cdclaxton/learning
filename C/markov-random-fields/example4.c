#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "matrix.h"
#include "permutations.h"
#include "sum_product_utilities.h"

// Number of time steps
#define N_TIME_STEPS 3
#define N_LANES 3

// Sample from a categorical distribution. Note that probs must sum to 1.
int sampleFromCategoricalDist(double *probs,
                              int nElements)
{
    // Check that the probabilities sum to one
    double totalProbability = 0.0;
    for (int i = 0; i < nElements; i++)
    {
        totalProbability += *(probs + i);
    }
    if (abs(totalProbability - 1) > 1e-6)
    {
        printf("Error: Probabilities don't sum to 1\n");
        exit(1);
    }

    // Value in the range [0,1]
    double value = (double)rand() / RAND_MAX;

    // Return a sample using the CDF
    double total = probs[0];
    for (int i = 0; i < (nElements - 1); i++)
    {
        if (value <= total)
        {
            return i;
        }
        total += probs[i + 1];
    }

    return nElements - 1;
}

void sampleVehiclePosition(double initialLane[N_LANES],
                           double gTheta[N_LANES][N_LANES],
                           int *positions)
{
    // Initial position
    positions[0] = sampleFromCategoricalDist(initialLane, N_LANES);

    // Subsequent positions
    for (int i = 1; i < N_TIME_STEPS; i++)
    {
        int prev = positions[i - 1];
        positions[i] = sampleFromCategoricalDist(gTheta[prev], N_LANES);
    }
}

void printVehiclePosition(int positions[N_TIME_STEPS])
{
    for (int i = 0; i < N_TIME_STEPS; i++)
    {
        printf("%d ", positions[i]);
    }
    printf("\n");
}

// Sample from a continuous uniform distribution.
double sampleFromUniform(double minValue,
                         double maxValue)
{
    if (minValue >= maxValue)
    {
        printf("Error: min value >= max value\n");
        exit(1);
    }

    // Value in the range [0,1]
    double value = (double)rand() / RAND_MAX;

    // Value in the range [minValue, maxValue]
    return ((maxValue - minValue) * value) + minValue;
}

// Populate a lane x timestep matrix.
void generateObservations(int vehiclePositions[N_TIME_STEPS],
                          double pMinVehicleInLane,
                          double pMaxVehicleInLane,
                          double pMinVehicleNotInLane,
                          double pMaxVehicleNotInLane,
                          double observations[N_LANES][N_TIME_STEPS])
{
    if (pMinVehicleInLane >= pMaxVehicleInLane)
    {
        printf("Error: Invalid pMinVehicleInLane and pMaxVehicleInLane\n");
        exit(1);
    }
    if (pMinVehicleNotInLane >= pMaxVehicleNotInLane)
    {
        printf("Error: Invalid pMinVehicleNotInLanena and pMaxVehicleNotInLane\n");
        exit(1);
    }

    for (int t = 0; t < N_TIME_STEPS; t++)
    {
        double total = 0.0;
        for (int lane = 0; lane < N_LANES; lane++)
        {
            if (vehiclePositions[t] == lane)
            {
                observations[lane][t] = sampleFromUniform(pMinVehicleInLane, pMaxVehicleInLane);
            }
            else
            {
                observations[lane][t] = sampleFromUniform(pMinVehicleNotInLane, pMaxVehicleNotInLane);
            }
            total += observations[lane][t];
        }

        // Normalise the values
        for (int lane = 0; lane < N_LANES; lane++)
        {
            observations[lane][t] = observations[lane][t] / total;
        }
    }
}

void printObservations(double observations[N_LANES][N_TIME_STEPS])
{
    for (int lane = 0; lane < N_LANES; lane++)
    {
        printf("Lane %d: ", lane);
        for (int t = 0; t < N_TIME_STEPS; t++)
        {
            printf("%f ", observations[lane][t]);
        }
        printf("\n");
    }
}

int generatePermuations(int **matrix)
{
    // Calculate the number of permutations
    int nPermutations = numberOfPermutations(N_TIME_STEPS, N_LANES);

    // Allocate space all permutations
    *matrix = (int *)malloc(nPermutations * N_TIME_STEPS * sizeof(int));
    if (matrix == NULL)
    {
        perror("Failed to allocate memory for permutations");
        exit(1);
    }

    // Generate the permutations
    permutations(N_TIME_STEPS, N_LANES, *matrix);
    // printMatrix(*matrix, nPermutations, N_TIME_STEPS);

    return nPermutations;
}

void bruteForce(double observations[N_LANES][N_TIME_STEPS],
                double gTheta[N_LANES][N_LANES],
                double result[N_LANES][N_TIME_STEPS])
{
    // Generate all permutations
    int *permutations = NULL;
    int nPermutations = generatePermuations(&permutations);

    // Walk through each time step
    for (int xi = 0; xi < N_TIME_STEPS; xi++)
    {
        double total = 0.0;

        // Walk through each lane
        for (int lane = 0; lane < N_LANES; lane++)
        {
            double p = marginal(observations[0],
                                gTheta[0],
                                xi,
                                lane,
                                permutations,
                                nPermutations,
                                N_LANES,
                                N_TIME_STEPS);
            result[lane][xi] = p;
            total += p;
        }

        // Normalise
        for (int lane = 0; lane < N_LANES; lane++)
        {
            result[lane][xi] = result[lane][xi] / total;
        }
    }

    // Free the generated permutations
    free(permutations);
}

void findMostLikelyStates(double observations[N_LANES][N_TIME_STEPS],
                          double gTheta[N_LANES][N_LANES],
                          int mostLikelyStates[N_LANES])
{
    // Generate all permutations
    int *permutations = NULL;
    int nPermutations = generatePermuations(&permutations);

    double maximumJointProbability = -1;

    for (int i = 0; i < nPermutations; i++)
    {
        double prob = jointProbability(observations[0],
                                       gTheta[0],
                                       permutations + i * N_TIME_STEPS,
                                       N_LANES,
                                       N_TIME_STEPS);
        if (prob > maximumJointProbability)
        {
            memcpy(mostLikelyStates,
                   permutations + i * N_TIME_STEPS,
                   sizeof(int) * N_TIME_STEPS);
            maximumJointProbability = prob;
        }
    }

    // Free the generated permutations
    free(permutations);
}

void sumProduct(double observations[N_LANES][N_TIME_STEPS],
                double gTheta[N_LANES][N_LANES],
                double result[N_LANES][N_TIME_STEPS])
{
    if (N_TIME_STEPS != 3)
    {
        printf("Sum-product algorithm only works for 3 time steps");
        exit(1);
    }

    // Step 1
    // f0 -> x0
    double mu_f0_to_x0[N_LANES];
    double lambda_f0_to_x0[N_LANES];
    matrixColumn(observations[0], 0, N_LANES, N_TIME_STEPS, mu_f0_to_x0);
    calcLogMessage(mu_f0_to_x0, N_LANES, lambda_f0_to_x0);

    // f1 -> x1
    double mu_f1_to_x1[N_LANES];
    double lambda_f1_to_x1[N_LANES];
    matrixColumn(observations[0], 1, N_LANES, N_TIME_STEPS, mu_f1_to_x1);
    calcLogMessage(mu_f1_to_x1, N_LANES, lambda_f1_to_x1);

    // f2 -> x2
    double mu_f2_to_x2[N_LANES];
    double lambda_f2_to_x2[N_LANES];
    matrixColumn(observations[0], 2, N_LANES, N_TIME_STEPS, mu_f2_to_x2);
    calcLogMessage(mu_f2_to_x2, N_LANES, lambda_f2_to_x2);

    // Step 2
    // x0 -> g0
    double lambda_x0_to_g0[N_LANES];
    copyLogMessage(lambda_f0_to_x0, N_LANES, lambda_x0_to_g0);

    // x2 -> g1
    double lambda_x2_to_g1[N_LANES];
    copyLogMessage(lambda_f2_to_x2, N_LANES, lambda_x2_to_g1);

    // Step 3
    // g0 -> x1
    double lambda_g0_to_x1[N_LANES];
    logSumProductForStates(N_LANES, false, gTheta[0], lambda_x0_to_g0, lambda_g0_to_x1);

    // g1 -> x1
    double lambda_g1_to_x1[N_LANES];
    logSumProductForStates(N_LANES, true, gTheta[0], lambda_x2_to_g1, lambda_g1_to_x1);

    // Step 4
    // x1 -> g0
    double lambda_x1_to_g0[N_LANES];
    sumLogMessages(lambda_f1_to_x1, lambda_g1_to_x1, N_LANES, lambda_x1_to_g0);

    // x1 -> g1
    double lambda_x1_to_g1[N_LANES];
    sumLogMessages(lambda_f1_to_x1, lambda_g0_to_x1, N_LANES, lambda_x1_to_g1);

    // Step 5
    // g0 -> x0
    double lambda_g0_to_x0[N_LANES];
    logSumProductForStates(N_LANES, true, gTheta[0], lambda_x1_to_g0, lambda_g0_to_x0);

    // g1 -> x2
    double lambda_g1_to_x2[N_LANES];
    logSumProductForStates(N_LANES, false, gTheta[0], lambda_x1_to_g1, lambda_g1_to_x2);

    // Marginal for x0
    double p_x0[3];
    marginalFactors(lambda_f0_to_x0,
                    lambda_g0_to_x0,
                    NULL,
                    N_LANES,
                    2,
                    p_x0);

    // Marginal for x1
    double p_x1[3];
    marginalFactors(lambda_g0_to_x1,
                    lambda_f1_to_x1,
                    lambda_g1_to_x1,
                    N_LANES,
                    3,
                    p_x1);

    // Marginal for x2
    double p_x2[3];
    marginalFactors(lambda_f2_to_x2,
                    lambda_g1_to_x2,
                    NULL,
                    N_LANES,
                    2,
                    p_x2);

    // Record the result
    setMatrixColumn(result[0], N_LANES, N_TIME_STEPS, p_x0, 0);
    setMatrixColumn(result[0], N_LANES, N_TIME_STEPS, p_x1, 1);
    setMatrixColumn(result[0], N_LANES, N_TIME_STEPS, p_x2, 2);
}

void maxProduct(double observations[N_LANES][N_TIME_STEPS],
                double gTheta[N_LANES][N_LANES],
                int mostLikelyStatesMaxProduct[N_TIME_STEPS])
{
    if (N_TIME_STEPS != 3)
    {
        printf("Sum-product algorithm only works for 3 time steps");
        exit(1);
    }

    // Step 1
    // f0 -> x0
    double mu_f0_to_x0[N_LANES];
    double lambda_f0_to_x0[N_LANES];
    matrixColumn(observations[0], 0, N_LANES, N_TIME_STEPS, mu_f0_to_x0);
    calcLogMessage(mu_f0_to_x0, N_LANES, lambda_f0_to_x0);

    // f1 -> x1
    double mu_f1_to_x1[N_LANES];
    double lambda_f1_to_x1[N_LANES];
    matrixColumn(observations[0], 1, N_LANES, N_TIME_STEPS, mu_f1_to_x1);
    calcLogMessage(mu_f1_to_x1, N_LANES, lambda_f1_to_x1);

    // f2 -> x2
    double mu_f2_to_x2[N_LANES];
    double lambda_f2_to_x2[N_LANES];
    matrixColumn(observations[0], 2, N_LANES, N_TIME_STEPS, mu_f2_to_x2);
    calcLogMessage(mu_f2_to_x2, N_LANES, lambda_f2_to_x2);

    // Step 2
    // x0 -> g0
    double lambda_x0_to_g0[N_LANES];
    copyLogMessage(lambda_f0_to_x0, N_LANES, lambda_x0_to_g0);

    // x2 -> g1
    double lambda_x2_to_g1[N_LANES];
    copyLogMessage(lambda_f2_to_x2, N_LANES, lambda_x2_to_g1);

    // Step 3
    // g0 -> x1
    double lambda_g0_to_x1[N_LANES];
    maxLogPlusLogMessage(N_LANES, false, gTheta[0], lambda_x0_to_g0, lambda_g0_to_x1);

    // g1 -> x1
    double lambda_g1_to_x1[N_LANES];
    maxLogPlusLogMessage(N_LANES, true, gTheta[0], lambda_x2_to_g1, lambda_g1_to_x1);

    // Step 4
    // x1 -> g0
    double lambda_x1_to_g0[N_LANES];
    sumLogMessages(lambda_f1_to_x1, lambda_g1_to_x1, N_LANES, lambda_x1_to_g0);

    // x1 -> g1
    double lambda_x1_to_g1[N_LANES];
    sumLogMessages(lambda_f1_to_x1, lambda_g0_to_x1, N_LANES, lambda_x1_to_g1);

    // Step 5
    // g0 -> x0
    double lambda_g0_to_x0[N_LANES];
    maxLogPlusLogMessage(N_LANES, true, gTheta[0], lambda_x1_to_g0, lambda_g0_to_x0);

    // g1 -> x2
    double lambda_g1_to_x2[N_LANES];
    maxLogPlusLogMessage(N_LANES, false, gTheta[0], lambda_x1_to_g1, lambda_g1_to_x2);

    // MAP solution
    mostLikelyStatesMaxProduct[0] = argMaxSumMessages(lambda_f0_to_x0,
                                                      lambda_g0_to_x0,
                                                      NULL,
                                                      N_LANES,
                                                      2);

    mostLikelyStatesMaxProduct[1] = argMaxSumMessages(lambda_g0_to_x1,
                                                      lambda_f1_to_x1,
                                                      lambda_g1_to_x1,
                                                      N_LANES,
                                                      3);

    mostLikelyStatesMaxProduct[2] = argMaxSumMessages(lambda_f2_to_x2,
                                                      lambda_g1_to_x2,
                                                      NULL,
                                                      N_LANES,
                                                      2);
}

int main(void)
{
    // Setting seed for the rand() function
    srand(time(0));

    // Probability of changing lane
    double gTheta[N_LANES][N_LANES] = {{0.8, 0.2, 0.0},
                                       {0.1, 0.8, 0.1},
                                       {0.0, 0.2, 0.8}};

    // Probability of starting in a given lane
    double initialLane[N_LANES] = {1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0};

    // Create a random ground truth path for the vehicle
    int vehiclePositions[N_LANES];
    sampleVehiclePosition(initialLane, gTheta, vehiclePositions);
    printf("Ground-truth lanes:\n");
    printVehiclePosition(vehiclePositions);
    printf("\n");

    // Generate the observations
    double observations[N_LANES][N_TIME_STEPS];
    double pMinVehicleInLane = 0.8;
    double pMaxVehicleInLane = 1.0;
    double pMinVehicleNotInLane = 0.01;
    double pMaxVehicleNotInLane = 0.1;
    generateObservations(vehiclePositions,
                         pMinVehicleInLane, pMaxVehicleInLane,
                         pMinVehicleNotInLane, pMaxVehicleNotInLane,
                         observations);
    printf("Observations:\n");
    printObservations(observations);
    printf("\n");

    // Find the most likely vehicle path using a brute force approach, trying
    // all permutations of the lanes
    int mostLikelyStates[N_TIME_STEPS];
    findMostLikelyStates(observations, gTheta, mostLikelyStates);
    printf("Most likely states:\n");
    printVehiclePosition(mostLikelyStates);
    printf("\n");

    // Calculate the predicted vehicle path using a brute force approach
    double predictedBruteForce[N_LANES][N_TIME_STEPS];
    bruteForce(observations, gTheta, predictedBruteForce);
    printf("Marginal using brute force:\n");
    printObservations(predictedBruteForce);
    printf("\n");

    // Calculate the predicted vehicle path using sum-product algorithm
    double predictedSumProduct[N_LANES][N_TIME_STEPS];
    sumProduct(observations, gTheta, predictedSumProduct);
    printf("Marginal using the sum-product algorithm:\n");
    printObservations(predictedSumProduct);
    printf("\n");

    // Calculate the most likely state using the max-product algorithm
    int mostLikelyStatesMaxProduct[N_TIME_STEPS];
    printf("Most likely states using the max-product algorithm:\n");
    maxProduct(observations, gTheta, mostLikelyStatesMaxProduct);
    printVehiclePosition(mostLikelyStatesMaxProduct);
    printf("\n");

    return 0;
}