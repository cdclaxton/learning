#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ROWS 10 // Number of rows in the image
#define COLS 10 // Number of columns in the image

// Display the image to stdout.
void displayImage(char image[ROWS][COLS])
{
    printf("|==========|\n");

    for (int i = 0; i < ROWS; i++)
    {
        printf("|");
        for (int j = 0; j < COLS; j++)
        {
            if (image[i][j] == 0)
            {
                printf(".");
            }
            else
            {
                printf("#");
            }
        }
        printf("|\n");
    }

    printf("|==========|\n");
}

// Add noise to the original image to yield a noisy image. The probability that
// a pixel is switched is given by pMutation, which must be in the range [0,1].
void addNoise(char original[ROWS][COLS],
              char noisy[ROWS][COLS],
              double pMutation)
{
    // Setting seed for the rand() function
    srand(time(0));

    for (int i = 0; i < ROWS; i++)
    {
        for (int j = 0; j < COLS; j++)
        {
            double value = (double)rand() / RAND_MAX; // value in range [0,1]
            if (value < pMutation)
            {
                noisy[i][j] = 1 - original[i][j];
            }
            else
            {
                noisy[i][j] = original[i][j];
            }
        }
    }
}

// Calculate the error between image1 and image2, which is defined as the sum of
// difference in the pixel values.
int error(char image1[ROWS][COLS],
          char image2[ROWS][COLS])
{
    int total = 0;

    for (int i = 0; i < ROWS; i++)
    {
        for (int j = 0; j < COLS; j++)
        {
            if (image1[i][j] != image2[i][j])
            {
                total += 1;
            }
        }
    }

    return total;
}

// Copy image original into output.
void copyImage(char original[ROWS][COLS],
               char output[ROWS][COLS])
{
    for (int i = 0; i < ROWS; i++)
    {
        for (int j = 0; j < COLS; j++)
        {
            output[i][j] = original[i][j];
        }
    }
}

double bias(char image[ROWS][COLS])
{
    int total = 0.0;

    for (int i = 0; i < ROWS; i++)
    {
        for (int j = 0; j < COLS; j++)
        {
            total += (2 * image[i][j]) - 1;
        }
    }

    return (double)total;
}

double neighboursTerm(char pixel1, char pixel2)
{
    return pixel1 == pixel2 ? 0.0 : 1.0;
}

double neighbours(char image[ROWS][COLS])
{
    double total = 0.0;

    for (int i = 0; i < ROWS - 1; i++)
    {
        for (int j = 0; j < COLS - 1; j++)
        {
            total += neighboursTerm(image[i][j], image[i][j + 1]) + // horizontal
                     neighboursTerm(image[i][j], image[i + 1][j]);  // vertical
        }
    }

    // Right-hand edge
    for (int i = 0; i < ROWS - 1; i++)
    {
        total += neighboursTerm(image[i][COLS - 1], image[i + 1][COLS - 1]);
    }

    // Bottom
    for (int j = 0; j < COLS - 1; j++)
    {
        total += neighboursTerm(image[ROWS - 1][j], image[ROWS - 1][j + 1]);
    }

    return total;
}

double change(char original[ROWS][COLS], // original (noisy) image
              char image[ROWS][COLS])    // current denoised image
{
    double total = 0.0;

    for (int i = 0; i < ROWS - 1; i++)
    {
        for (int j = 0; j < COLS - 1; j++)
        {
            total += neighboursTerm(original[i][j], image[i][j]);
        }
    }

    return total;
}

double imageEnergy(char original[ROWS][COLS], // original (noisy) image
                   char image[ROWS][COLS],    // current denoised image
                   double h,
                   double beta,
                   double eta)
{
    return h * bias(image) + beta * neighbours(image) + eta * change(image, original);
}

// Perform a single denoise pass of the image using a Markov Random Field (MRF)
// with Iterated Conditional Modes (ICM).
int singleDenoisePass(char original[ROWS][COLS], // original (noisy) image
                      char image[ROWS][COLS],    // current denoised image
                      double h,
                      double beta,
                      double eta)
{
    int numChanges = 0;

    for (int i = 0; i < ROWS; i++)
    {
        for (int j = 0; j < COLS; j++)
        {
            // Pixel [i,j] is to be checked
            double energyCurrent = imageEnergy(original, image, h, beta, eta);

            // Flip the [i,j] pixel
            image[i][j] = 1 - image[i][j];
            double energyNew = imageEnergy(original, image, h, beta, eta);

            if (energyNew < energyCurrent)
            {
                // Retain the [i,j] pixel flip
                numChanges += 1;
            }
            else
            {
                // Revert the [i,j] pixel flip
                image[i][j] = 1 - image[i][j];
            }
        }
    }

    return numChanges;
}

// Denoise the image using an MRF with a maximum of maxCompletePasses complete
// passes.
void denoiseImage(char original[ROWS][COLS],
                  char output[ROWS][COLS],
                  int maxCompletePasses,
                  double h,
                  double beta,
                  double eta)
{
    // Make a copy of the original into the output image
    copyImage(original, output);

    for (int pass = 0; pass < maxCompletePasses; pass++)
    {
        int numChanges = singleDenoisePass(original, output, h, beta, eta);
        if (numChanges == 0)
        {
            printf("Denoising stopped at pass %d\n", pass);
            break;
        }
    }
}

int main(int argc, char *argv[])
{
    // Parse the command line arguments
    if (argc != 4)
    {
        printf("Usage: %s <h> <beta> <eta>\n", argv[0]);
        return -1;
    }

    double h = atof(argv[1]);
    double beta = atof(argv[2]);
    double eta = atof(argv[3]);
    printf("Parameters:\n");
    printf("h = %f, beta = %f, eta = %f\n", h, beta, eta);

    // Build a simple binary image
    char image[10][10] = {
        {1, 1, 0, 0, 0, 0, 0, 0, 0, 0},
        {1, 1, 0, 0, 0, 0, 0, 0, 0, 0},
        {1, 1, 1, 1, 1, 1, 1, 0, 0, 0},
        {1, 1, 1, 1, 1, 1, 1, 0, 0, 0},
        {0, 0, 0, 0, 0, 1, 1, 0, 0, 0},
        {0, 0, 0, 0, 0, 1, 1, 0, 0, 0},
        {0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
        {0, 0, 0, 1, 1, 1, 1, 1, 1, 1},
        {0, 0, 0, 1, 1, 0, 0, 0, 1, 1},
        {0, 0, 0, 1, 1, 0, 0, 0, 1, 1}};

    printf("Original image:\n");
    displayImage(image);

    // Make a noisy version of the original image
    char noisy[10][10];
    addNoise(image, noisy, 0.05);
    printf("Noisy image (error=%d):\n", error(image, noisy));
    displayImage(noisy);

    // Use a Markov Random Field (MRF) with Iterated Conditional Modes (ICM) to
    // denoise the image
    char denoised[10][10];

    denoiseImage(noisy, denoised, 10, h, beta, eta);
    printf("Denoised image (error=%d):\n", error(image, denoised));
    displayImage(denoised);
}