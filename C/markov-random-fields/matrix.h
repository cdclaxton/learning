// Index in a matrix with nColumns columns.
int matrixIndex(int rowIndex,
                int colIndex,
                int nColumns);

void printMatrix(int *matrix,
                 int nRows,
                 int nCols);

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

void setMatrixColumn(double *matrix,
                     int nRows,
                     int nCols,
                     double *vector,
                     int columnIndex);