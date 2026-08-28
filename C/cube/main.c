#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>

#define PI 3.1415926536

#define SCREEN_WIDTH 40
#define SCREEN_HEIGHT 30

// Get the index into the buffer for the position (x,y)
#define index(x, y) (y * SCREEN_WIDTH + x)

// Get the index into a matrix with nCols columns
#define matrixIndex(row, col, nCols) (row * nCols + col)

// Convert an angle from degrees to radians
#define toRadians(degrees) (degrees * PI / 180)

void clearBuffer(char *buffer)
{
    for (int y = SCREEN_HEIGHT - 1; y >= 0; y--)
    {
        for (int x = 0; x < SCREEN_WIDTH; x++)
        {
            buffer[index(x, y)] = ' ';
        }
    }
}

char getPixel(char *buffer, int x, int y)
{
    return buffer[index(x, y)];
}

char setPixel(char *buffer, int x, int y, char value)
{
    if ((0 <= y) && (y < SCREEN_HEIGHT) &&
        (0 <= x) && (x < SCREEN_WIDTH))
    {
        buffer[index(x, y)] = value;
    }
}

void display(char *buffer)
{
    for (int y = SCREEN_HEIGHT - 1; y >= 0; y--)
    {
        for (int x = 0; x < SCREEN_WIDTH; x++)
        {
            printf("%c", getPixel(buffer, x, y));
        }
        printf("\n");
    }
}

// Clear a 4x4 transformation matrix.
void clearMatrix(float *matrix)
{
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            matrix[matrixIndex(i, j, 4)] = 0.0;
        }
    }
}

// Display a matrix to the screen.
void displayMatrix(float *matrix, int nRows, int nCols)
{
    for (int row = 0; row < nRows; row++)
    {
        for (int col = 0; col < nCols; col++)
        {
            if (col == nCols - 1)
            {
                printf(" %.2f", matrix[matrixIndex(row, col, nCols)]);
            }
            else
            {
                printf(" %.2f,", matrix[matrixIndex(row, col, nCols)]);
            }
        }
        printf("\n");
    }
}

void buildProjectionMatrix(float *matrix, float k_x, float k_y, float k_z)
{
    clearMatrix(matrix);
    matrix[matrixIndex(0, 0, 4)] = k_x;
    matrix[matrixIndex(1, 1, 4)] = k_y;
    matrix[matrixIndex(2, 2, 4)] = k_z;
    matrix[matrixIndex(3, 3, 4)] = 1.0;
}

void buildTranslationMatrix(float *matrix, float x, float y, float z)
{
    clearMatrix(matrix);
    matrix[matrixIndex(0, 0, 4)] = 1;
    matrix[matrixIndex(0, 3, 4)] = x;
    matrix[matrixIndex(1, 1, 4)] = 1;
    matrix[matrixIndex(1, 3, 4)] = y;
    matrix[matrixIndex(2, 2, 4)] = 1;
    matrix[matrixIndex(2, 3, 4)] = z;
    matrix[matrixIndex(3, 3, 4)] = 1;
}

void buildScalingMatrix(float *matrix, float x, float y, float z)
{
    clearMatrix(matrix);
    matrix[matrixIndex(0, 0, 4)] = x;
    matrix[matrixIndex(1, 1, 4)] = y;
    matrix[matrixIndex(2, 2, 4)] = z;
    matrix[matrixIndex(3, 3, 4)] = 1.0;
}

void buildXRotationMatrix(float *matrix, float thetaDegrees)
{
    clearMatrix(matrix);

    // Convert theta to radians
    float theta = toRadians(thetaDegrees);

    matrix[matrixIndex(0, 0, 4)] = 1.0;
    matrix[matrixIndex(1, 1, 4)] = (float)cos(theta);
    matrix[matrixIndex(1, 2, 4)] = -(float)sin(theta);
    matrix[matrixIndex(2, 1, 4)] = (float)sin(theta);
    matrix[matrixIndex(2, 2, 4)] = (float)cos(theta);
    matrix[matrixIndex(3, 3, 4)] = 1;
}

void buildYRotationMatrix(float *matrix, float thetaDegrees)
{
    clearMatrix(matrix);

    // Convert theta to radians
    float theta = toRadians(thetaDegrees);

    matrix[matrixIndex(0, 0, 4)] = (float)cos(theta);
    matrix[matrixIndex(0, 2, 4)] = (float)sin(theta);
    matrix[matrixIndex(1, 1, 4)] = 1.0;
    matrix[matrixIndex(2, 0, 4)] = -(float)sin(theta);
    matrix[matrixIndex(2, 2, 4)] = (float)cos(theta);
    matrix[matrixIndex(3, 3, 4)] = 1;
}

void buildZRotationMatrix(float *matrix, float thetaDegrees)
{
    clearMatrix(matrix);

    // Convert theta to radians
    float theta = toRadians(thetaDegrees);

    matrix[matrixIndex(0, 0, 4)] = 1.0;
    matrix[matrixIndex(0, 0, 4)] = (float)cos(theta);
    matrix[matrixIndex(0, 1, 4)] = -(float)sin(theta);
    matrix[matrixIndex(1, 0, 4)] = (float)sin(theta);
    matrix[matrixIndex(1, 1, 4)] = (float)cos(theta);
    matrix[matrixIndex(2, 2, 4)] = 1;
    matrix[matrixIndex(3, 3, 4)] = 1;
}

// Perform matrix multiplication result = A x B.
void mul(float *matrixA, int nRowsA, int nColsA,
         float *matrixB, int nRowsB, int nColsB,
         float *result)
{
    // Check that the matrices are compatible
    assert(nColsA == nRowsB);

    for (int i = 0; i < nRowsA; i++)
    {
        for (int j = 0; j < nColsB; j++)
        {
            result[matrixIndex(i, j, nColsB)] = 0;

            for (int c = 0; c < nColsA; c++)
            {
                result[matrixIndex(i, j, nColsB)] +=
                    matrixA[matrixIndex(i, c, nColsA)] * matrixB[matrixIndex(c, j, nColsB)];
            }
        }
    }
}

void convertToPixels(char *buffer, float *points, int nPoints)
{
    for (int p = 0; p < nPoints; p++)
    {
        int x = (int)round(points[matrixIndex(0, p, nPoints)]);
        int y = (int)round(points[matrixIndex(1, p, nPoints)]);
        setPixel(buffer, x, y, '*');
    }
}

void plotLine(char *buffer, int x0, int y0, int x1, int y1)
{
    int dx = abs(x1 - x0);
    int sx = x0 < x1 ? 1 : -1;

    int dy = -abs(y1 - y0);
    int sy = y0 < y1 ? 1 : -1;

    int error = dx + dy;

    while (1)
    {
        setPixel(buffer, x0, y0, '.');
        int e2 = 2 * error;
        if (e2 >= dy)
        {
            if (x0 == x1)
            {
                break;
            }
            error = error + dy;
            x0 = x0 + sx;
        }
        if (e2 <= dx)
        {
            if (y0 == y1)
            {
                break;
            }
            error = error + dx;
            y0 = y0 + sy;
        }
    }
}

char getch_linux(void)
{
    struct termios oldt, newt;
    char ch;

    // Save current terminal settings
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;

    // Disable canonical mode (line buffering) and text echo
    newt.c_lflag &= ~(ICANON | ECHO);

    // Apply new settings
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    // Read a single character
    ch = getchar();

    // Restore the original terminal settings
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);

    return ch;
}

void drawLinesFromCoords(char *buffer, float *projectedCube)
{
    int linePairs[12][2] = {
        {0, 1},
        {0, 2},
        {2, 3},
        {1, 3},
        {0, 4},
        {1, 5},
        {2, 6},
        {3, 7},
        {4, 5},
        {4, 6},
        {6, 7},
        {5, 7},
    };

    for (int i = 0; i < 12; i++)
    {
        int p0 = linePairs[i][0];
        int p1 = linePairs[i][1];
        int x0 = (int)round(projectedCube[matrixIndex(0, p0, 8)]);
        int y0 = (int)round(projectedCube[matrixIndex(1, p0, 8)]);
        int x1 = (int)round(projectedCube[matrixIndex(0, p1, 8)]);
        int y1 = (int)round(projectedCube[matrixIndex(1, p1, 8)]);
        plotLine(buffer, x0, y0, x1, y1);
    }
}

int main()
{
    // Buffer to hold the screen pixels
    char buffer[SCREEN_HEIGHT * SCREEN_WIDTH];

    // Coordinates of the vertices of the unit cube in homogeneous coordinates
    float cube[4][8] = {
        {-0.5, 0.5, -0.5, 0.5, -0.5, 0.5, -0.5, 0.5},
        {-0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5},
        {-0.5, -0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5},
        {1, 1, 1, 1, 1, 1, 1, 1},
    };

    float scaling = 1;
    float rotateXDegrees = 20;
    float rotateYDegrees = 20;
    float rotateZDegrees = 0;

    int first = 1;

    while (1)
    {
        if (first == 0)
        {
            // Get a character from the keyboard
            char ch = getch_linux();

            switch (ch)
            {
            case 'q':
                return 0;
            case 'o':
                rotateXDegrees -= 10;
                break;
            case 'p':
                rotateXDegrees += 10;
                break;
            case 'k':
                rotateYDegrees -= 10;
                break;
            case 'l':
                rotateYDegrees += 10;
                break;
            case 'n':
                rotateZDegrees -= 10;
                break;
            case 'm':
                rotateZDegrees += 10;
                break;
            case 'z':
                scaling -= 0.1;
                break;
            case 'x':
                scaling += 0.1;
                break;
            }
        }

        first = 0;

        // Scale the cube
        float scalingMatrix[16];
        float scaledCube[4 * 8];
        buildScalingMatrix(scalingMatrix, scaling * 20, scaling * 20, scaling * 20);
        mul(scalingMatrix, 4, 4, &cube[0][0], 4, 8, scaledCube);
        // displayMatrix(scalingMatrix, 4, 4);
        // displayMatrix(scaledCube, 4, 8);

        // Rotate the cube about the x-axis
        float rotationMatrixX[16];
        float rotatedCubeX[4 * 8];
        buildXRotationMatrix(rotationMatrixX, rotateXDegrees);
        mul(rotationMatrixX, 4, 4, scaledCube, 4, 8, rotatedCubeX);
        // displayMatrix(rotationMatrixX, 4, 4);
        // displayMatrix(rotatedCubeX, 4, 8);

        // Rotate the cube about the y-axis
        float rotationMatrixY[16];
        float rotatedCubeY[4 * 8];
        buildYRotationMatrix(rotationMatrixY, rotateYDegrees);
        mul(rotationMatrixY, 4, 4, rotatedCubeX, 4, 8, rotatedCubeY);
        // displayMatrix(rotationMatrixY, 4, 4);

        // Rotate the cube about the z-axis
        float rotationMatrixZ[16];
        float rotatedCubeZ[4 * 8];
        buildZRotationMatrix(rotationMatrixZ, rotateZDegrees);
        mul(rotationMatrixZ, 4, 4, rotatedCubeY, 4, 8, rotatedCubeZ);
        // displayMatrix(rotationMatrixZ, 4, 4);

        // Translate the cube
        float translationMatrix[16];
        float translatedCube[4 * 8];
        buildTranslationMatrix(translationMatrix, 20, 15, 0);
        mul(translationMatrix, 4, 4, rotatedCubeZ, 4, 8, translatedCube);
        // displayMatrix(translationMatrix, 4, 4);
        // displayMatrix(translatedCube, 4, 8);

        // Project the cube onto the xy-plane
        float projectionMatrix[16];
        float projectedCube[4 * 8];
        buildProjectionMatrix(projectionMatrix, 1.0, 1.0, 0.0);
        mul(projectionMatrix, 4, 4, translatedCube, 4, 8, projectedCube);
        // displayMatrix(projectedCube, 4, 8);

        // Clear the pixel buffer
        clearBuffer(buffer);

        // Draw the lines of the cube
        drawLinesFromCoords(buffer, projectedCube);

        // Draw the points of the cube
        convertToPixels(buffer, projectedCube, 8);

        // Display
        display(buffer);
        printf("Scaling: %f\n", scaling);
        printf("Rotation: x=%f, y=%f, z=%f\n", rotateXDegrees, rotateYDegrees, rotateZDegrees);
    }

    return 0;
}