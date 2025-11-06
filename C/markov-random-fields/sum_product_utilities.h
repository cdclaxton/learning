// Calculate the log message from a message with a given length.
void calcLogMessage(double *message,
                    int length,
                    double *result);

// Calculate the sum of two log messages.
void sumLogMessages(double *logMessage1,
                    double *logMessage2,
                    int length,
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