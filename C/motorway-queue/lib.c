#include <stdio.h>
#include "simulation.h"

double *simulate(double speedInMs,        // Vechicle speed in m/s
                 int numberOfRuns,        // Number of runs
                 double timeDelta,        // Simulation tick
                 double pBlockage,        // Probability of a blockage
                 double blockageDuration) // Duration of a blockage in seconds
{
    // Instantiate the motorway
    double sectionLengths[3] = {16550, 5000, 10750};
    Motorway *motorway = newMotorway(sectionLengths, 3, 5);

    double speedsInMs[1] = {speedInMs};
    int numberOfSpeeds = 1;

    // Instantiate the simulation
    Simulation *simulation = newSimulation(speedsInMs,
                                           numberOfSpeeds,
                                           numberOfRuns,
                                           timeDelta,
                                           pBlockage,
                                           blockageDuration);

    // Run the simulation
    runSimulation(simulation, motorway);

    // Copy the journey times into an array to return
    double *journeyTimes = malloc(sizeof(double) * numberOfRuns);
    for (int i = 0; i < numberOfRuns; i++)
    {
        journeyTimes[i] = simulation->journeyTimes[i];
    }

    // Free the memory allocated
    freeSimulation(simulation);

    return journeyTimes;
}

void freeResults(double *results)
{
    free(results);
}