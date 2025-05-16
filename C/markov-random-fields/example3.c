#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Number of states for a variable
#define K 4

// Populate a random K x K potential table.
void randomPotentialTable(double table[K][K])
{
    // Set the seed for the rand() function
    srand(time(0));

    // Randomly populate the K x K table
    double total = 0.0;
    for (int i = 0; i < K; i++)
    {
        for (int j = 0; j < K; j++)
        {
            table[i][j] = (double)rand() / RAND_MAX; // value in range [0,1]
            total += table[i][j];
        }
    }

    // Normalise the table so that the elements sum to one
    for (int i = 0; i < K; i++)
    {
        for (int j = 0; j < K; j++)
        {
            table[i][j] = table[i][j] / total;
        }
    }
}

double jointDistribution(double psi01[K][K],     // Potential function psi_{01}
                         double psi12[K][K],     // Potential function psi_{12}
                         double result[K][K][K]) // Joint distribution (K^3 elements)
{
    double total = 0.0;

    for (int x0 = 0; x0 < K; x0++)
    {
        for (int x1 = 0; x1 < K; x1++)
        {
            for (int x2 = 0; x2 < K; x2++)
            {
                result[x0][x1][x2] = psi01[x0][x1] * psi12[x1][x2];
                total += result[x0][x1][x2];
            }
        }
    }

    // Normalise the joint distribution
    for (int x0 = 0; x0 < K; x0++)
    {
        for (int x1 = 0; x1 < K; x1++)
        {
            for (int x2 = 0; x2 < K; x2++)
            {
                result[x0][x1][x2] = result[x0][x1][x2] / total;
            }
        }
    }

    return total;
}

double marginal(double distribution[K][K][K], // Joint distribution
                int variable,                 // Variable x
                int state)                    // State of variable x in range [0, K-1]
{
    double total = 0.0;

    for (int x0 = 0; x0 < K; x0++)
    {
        for (int x1 = 0; x1 < K; x1++)
        {
            for (int x2 = 0; x2 < K; x2++)
            {
                if ((variable == 0 && x0 != state) ||
                    (variable == 1 && x1 != state) ||
                    (variable == 2 && x2 != state))
                {
                    continue;
                }
                total += distribution[x0][x1][x2];
            }
        }
    }

    return total;
}

void naiveMarginal(double psi01[K][K],  // Potential function psi_{01}
                   double psi12[K][K],  // Potential function psi_{12}
                   double result[3][K]) // Marginal distribution (3 x K matrix)
{
    // Calculate the joint distribution
    double distribution[K][K][K];
    double total = jointDistribution(psi01, psi12, distribution);

    // Calculate the marginal by summing
    for (int x = 0; x < 3; x++)
    {
        for (int state = 0; state < K; state++)
        {
            result[x][state] = marginal(distribution, x, state);
        }
    }
}

void printMarginal(double marginal[3][K])
{
    for (int x = 0; x < 3; x++)
    {
        double total = 0.0;

        printf("x = %d: [", x);
        for (int state = 0; state < K; state++)
        {
            total += marginal[x][state];
            if (state < (K - 1))
            {
                printf("%f, ", marginal[x][state]);
            }
            else
            {
                printf("%f] (total = %f)\n", marginal[x][state], total);
            }
        }
    }
}

void calcMuBetaX1(double psi12[K][K],
                  double muBetaX1[K])
{
    for (int x1 = 0; x1 < K; x1++)
    {
        muBetaX1[x1] = 0.0;
        for (int x2 = 0; x2 < K; x2++)
        {
            muBetaX1[x1] += psi12[x1][x2];
        }
    }
}

void calcMuBetaX0(double psi01[K][K],
                  double muBetaX1[K],
                  double muBetaX0[K])
{
    for (int x0 = 0; x0 < K; x0++)
    {
        muBetaX0[x0] = 0.0;
        for (int x1 = 0; x1 < K; x1++)
        {
            muBetaX0[x0] += psi01[x0][x1] * muBetaX1[x1];
        }
    }
}

void calcMuAlphaX1(double psi01[K][K],
                   double muAlphaX1[K])
{
    for (int x1 = 0; x1 < K; x1++)
    {
        muAlphaX1[x1] = 0.0;
        for (int x0 = 0; x0 < K; x0++)
        {
            muAlphaX1[x1] += psi01[x0][x1];
        }
    }
}

void calcMuAlphaX2(double psi12[K][K],
                   double muAlphaX1[K],
                   double muAlphaX2[K])
{
    for (int x2 = 0; x2 < K; x2++)
    {
        muAlphaX2[x2] = 0.0;
        for (int x1 = 0; x1 < K; x1++)
        {
            muAlphaX2[x2] += psi12[x1][x2] * muAlphaX1[x1];
        }
    }
}

void normaliseMarginal(double p[K])
{
    double total = 0.0;
    for (int i = 0; i < K; i++)
    {
        total += p[i];
    }

    for (int i = 0; i < K; i++)
    {
        p[i] = p[i] / total;
    }
}

void messagePassingMarginal(double psi01[K][K],     // Potential function psi_{01}
                            double psi12[K][K],     // Potential function psi_{12}
                            double marginals[3][K]) // Marginal distribution (3 x K matrix)
{
    // Calculate \mu_{\beta}(x_1)
    double muBetaX1[K];
    calcMuBetaX1(psi12, muBetaX1);

    // Calculate \mu_{\beta}(x_0)
    double muBetaX0[K];
    calcMuBetaX0(psi01, muBetaX1, muBetaX0);

    // Calculate \mu_{\alpha}(x_1)
    double muAlphaX1[K];
    calcMuAlphaX1(psi01, muAlphaX1);

    // Calculate \mu_{\alpha}(x_2)
    double muAlphaX2[K];
    calcMuAlphaX2(psi12, muAlphaX1, muAlphaX2);

    // Calculate the unnormalised marginals
    double pX0[K];
    memcpy(pX0, muBetaX0, sizeof(double) * K);

    double pX1[K];
    for (int x1 = 0; x1 < K; x1++)
    {
        pX1[x1] = muAlphaX1[x1] * muBetaX1[x1];
    }

    double pX2[K];
    memcpy(pX2, muAlphaX2, sizeof(double) * K);

    // Normalise the marginals
    normaliseMarginal(pX0);
    normaliseMarginal(pX1);
    normaliseMarginal(pX2);

    // Build a matrix of marginals
    for (int i = 0; i < K; i++)
    {
        marginals[0][i] = pX0[i];
        marginals[1][i] = pX1[i];
        marginals[2][i] = pX2[i];
    }
}

int main(void)
{
    // Make the potential functions in the form of K x K tables
    double psi01[K][K];
    randomPotentialTable(psi01);

    double psi12[K][K];
    randomPotentialTable(psi12);

    // Calculate the marginal distribution of each variable using a naive,
    // brute-force approach
    double marginal1[3][K];
    naiveMarginal(psi01, psi12, marginal1);

    printf("Marginal using the naive approach:\n");
    printMarginal(marginal1);

    // Calculate the marginal distribution using message passing
    double marginal2[3][K];
    messagePassingMarginal(psi01, psi12, marginal2);

    printf("Marginal using the message passing approach:\n");
    printMarginal(marginal2);

    return 0;
}