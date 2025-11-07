#include <stdio.h>

int matrixIndex(int rowIndex,
                int colIndex,
                int nColumns)
{
    return rowIndex * nColumns + colIndex;
}

void printMatrix(int *matrix,
                 int nRows,
                 int nCols)
{
    for (int i = 0; i < nRows; i++)
    {
        for (int j = 0; j < nCols; j++)
        {
            printf("%d ", matrix[matrixIndex(i, j, nCols)]);
        }
        printf("\n");
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