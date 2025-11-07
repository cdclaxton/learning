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
                     double *g,
                     int numStates,
                     double *logVariableToFactorMessage);

void logSumProductForStates(int numStates,
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
