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

// Get a single row from the matrix.
void matrixRow(double *matrix,
               int row,
               int nColumns,
               double *result);

// Get a single column from the matrix.
void matrixColumn(double *matrix,
                  int column,
                  int nRows,
                  int nColumns,
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

void setMatrixColumn(double *matrix,
                     int nRows,
                     int nCols,
                     double *vector,
                     int columnIndex);