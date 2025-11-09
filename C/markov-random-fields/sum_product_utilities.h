#include <stdbool.h>

// Calculate the log message from a message with a given length.
void calcLogMessage(double *message,
                    int length,
                    double *result);

// Calculate the sum of two log messages.
void sumLogMessages(double *logMessage1,
                    double *logMessage2,
                    int length,
                    double *result);

void sumThreeLogMessages(double *logMessage1,
                         double *logMessage2,
                         double *logMessage3,
                         int length,
                         double *result);

double logSumProduct(int factorState,
                     bool knownFactorIsRow,
                     double *g, // N_LANES x N_LANES matrix
                     int numStates,
                     double *logVariableToFactorMessage);

void logSumProductForStates(int numStates,
                            bool knownFactorIsRow,
                            double *g,
                            double *logVariableToFactorMessage,
                            double *result);

// Copy a log message.
void copyLogMessage(double *logMessage,
                    int length,
                    double *result);

// Print a message.
void printMessage(double *message,
                  int length);

void marginalFactors(double *logMessage1,
                     double *logMessage2,
                     double *logMessage3,
                     int length,
                     int nMessages,
                     double *result);

double jointProbability(double *observations, // nLanes x nTimesteps
                        double *gTheta,       // nLanes x nLanes
                        int *state,           // nLanes
                        int nLanes,
                        int nTimesteps);

double marginal(double *observations, // nLanes x nTimesteps
                double *gTheta,       // nLanes x nLanes
                int xi,
                int lane,
                int *permutations,
                int nPermutations,
                int nLanes,
                int nTimesteps);