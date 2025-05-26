#include <stdio.h>
#include "simulation.h"

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        printf("Usage: %s <number of blockages per hour> <blockage duration> <number of runs per speed>\n",
               argv[0]);
        exit(EXIT_FAILURE);
    }

    // Number of blockages per hour, on average
    double numBlockagesPerHour = atof(argv[1]);
    printf("Number of blockages per hour = %f\n", numBlockagesPerHour);

    // Blockage duration in seconds
    double blockageDuration = atof(argv[2]);
    printf("Blockage duration = %f seconds\n", blockageDuration);

    // Number of simulation runs per speed
    int numberOfRunsPerSpeed = atoi(argv[3]);
    printf("Number of runs per speed = %d\n", numberOfRunsPerSpeed);

    // Time between simulation ticks in seconds
    double timeDelta = 1.0;

    // Number of ticks per hour
    double numTicksPerHour = 60 * 60 / timeDelta;

    // Probability of a blockage on a time tick
    double pBlockage = numBlockagesPerHour / numTicksPerHour;
    printf("pBlockage = %f\n", pBlockage);

    // Speeds to test in mph
    double speedsInMph[7] = {50, 55, 60, 65, 70, 75, 80};
    double speedsInMs[7];
    int numberOfSpeeds = 7;
    convertSpeeds(speedsInMph, speedsInMs, numberOfSpeeds);

    // Instantiate the motorway
    double sectionLengths[3] = {16550, 5000, 10750};
    Motorway *motorway = newMotorway(sectionLengths, 3, 5);

    // Instantiate the simulation
    Simulation *simulation = newSimulation(speedsInMs,
                                           numberOfSpeeds,
                                           numberOfRunsPerSpeed,
                                           timeDelta,
                                           pBlockage,
                                           blockageDuration);

    // Run the simulation
    runSimulation(simulation,
                  motorway);

    // Calculate the mean journey times
    double result[7];
    meanJourneyTimes(simulation,
                     result);

    printf("Results:\n");
    for (int i = 0; i < numberOfSpeeds; i++)
    {
        printf("Speed %f mph: Mean journey time = %f seconds\n", speedsInMph[i], result[i]);
    }

    // Free the allocated memory
    freeMotorway(motorway);
    freeSimulation(simulation);

    exit(EXIT_SUCCESS);
}