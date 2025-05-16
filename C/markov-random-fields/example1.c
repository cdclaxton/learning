#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "factor.h"

// Calculate the p(x) = f1(x1, x2) f2(x1, x2) f3(x2, x3) f4(x3)
double prob(bool x1, bool x2, bool x3)
{
    double p1 = log(twoFactor(x1, x2, 0.8, 0.2, 0.7, 0.1));
    double p2 = log(twoFactor(x1, x2, 0.9, 0.3, 0.2, 0.4));
    double p3 = log(twoFactor(x2, x3, 0.4, 0.1, 0.6, 0.7));
    double p4 = log(oneFactor(x3, 0.6, 0.1));

    return exp(p1 + p2 + p3 + p4);
}

double calcZ()
{
    char x[3] = {0, 0, 0};
    double total = 0.0;

    for (int i = 0; i < (int)pow(2, 3); i++)
    {
        setStates(i, x, 3);
        total += prob(x[0], x[1], x[2]);
    }

    return total;
}

int main(void)
{
    // Calculate the normalising constant Z
    double z = calcZ();
    printf("z = %lf\n", z);

    // Variables x[0], x[1], x[2]
    char x[3] = {0, 0, 0};

    // State with the maximum probability
    double maxProb = 0.0;
    char xStar[3] = {0, 0, 0};

    for (int i = 0; i < (int)pow(2, 3); i++)
    {
        setStates(i, x, 3);
        double p = prob(x[0], x[1], x[2]) / z;

        char resultString[100] = {'\0'};
        statesString(x, 3, resultString);
        printf("p(%s) = %f\n", resultString, p);

        if (p > maxProb)
        {
            maxProb = p;
            cloneStates(x, xStar, 3);
        }
    }

    char resultString[100] = {'\0'};
    statesString(x, 3, resultString);
    printf("Most probable state: p(%s) = %f\n", resultString, maxProb);
}