#include <stdio.h>
#include <string.h>
#include <time.h>
#include "simulation.h"

// -----------------------------------------------------------------------------
// Vehicle
// -----------------------------------------------------------------------------

Vehicle *newVehicle(double speed)
{
    Vehicle *vehicle = malloc(sizeof(Vehicle));
    vehicle->position = 0.0;
    vehicle->onMotorway = true;
    vehicle->speed = speed;
    return vehicle;
}

void freeVehicle(Vehicle *vehicle)
{
    free(vehicle);
}

double predicatedPosition(const Vehicle *const vehicle,
                          double timeDelta)
{
    return vehicle->position + (vehicle->speed * timeDelta);
}

bool positionInDelta(const Vehicle *const vehicle,
                     double position,
                     double tolerance)
{
    if (abs(vehicle->position - position) < tolerance)
    {
        return true;
    }
    return false;
}

void move(Vehicle *const vehicle,
          double timeDelta)
{
    vehicle->position = predicatedPosition(vehicle, timeDelta);
}

int decideVehicleAction(const Vehicle *const vehicle,
                        const Motorway *const motorway,
                        double currentTime,
                        double timeDelta)
{
    // Is there a junction in the path from the vehicle's current position to
    // where it could move to in the time? In this situation, it doesn't matter
    // if the vehicle is on or off the motorway
    double predicated = predicatedPosition(vehicle, timeDelta);
    if (!junctionInPath(motorway, vehicle->position, predicated))
    {
        // There is not a junction on the path, so see if the vehicle will be
        // blocked by an obstacle
        if (isPathBlocked(motorway, vehicle->position, predicated, currentTime) &&
            vehicle->onMotorway)
        {
            return VEHICLE_STOP;
        }

        return VEHICLE_MOVE_FORWARD;
    }

    // There is a junction in the path. If the vehicle is off the motorway and
    // the next section is clear, then the vehicle can rejoin the motorway.
    // If the next motorway section is blocked, then it continues forward off
    // the motorway
    if (!vehicle->onMotorway)
    {
        if (isSectionBlocked(motorway, predicated, currentTime))
        {
            return VEHICLE_MOVE_FORWARD;
        }
        return VEHICLE_JOIN_MOTORWAY;
    }

    // There is a junction in the path and the vehicle is on the motorway. If
    // the next section is clear and the path is unobstructed, then the vehicle
    // can move forward
    bool nextSectionClear = !isSectionBlocked(motorway, predicated, currentTime);
    bool pathToJunctionClear = isPathToJunctionClear(motorway, vehicle->position, currentTime);

    if (pathToJunctionClear)
    {
        if (nextSectionClear)
        {
            return VEHICLE_MOVE_FORWARD;
        }
        else
        {
            return VEHICLE_LEAVE_MOTORWAY;
        }
    }

    return VEHICLE_STOP;
}

void updateVehicle(Vehicle *vehicle,
                   Motorway *motorway,
                   double currentTime,
                   double timeDelta)
{
    // Decide what action to take
    int action = decideVehicleAction(vehicle, motorway, currentTime, timeDelta);

    // Change the state of the vehicle based on the decided action
    switch (action)
    {
    case VEHICLE_STOP:
        break;
    case VEHICLE_MOVE_FORWARD:
        move(vehicle, timeDelta);
        break;
    case VEHICLE_LEAVE_MOTORWAY:
        move(vehicle, timeDelta);
        vehicle->onMotorway = false;
        break;
    case VEHICLE_JOIN_MOTORWAY:
        move(vehicle, timeDelta);
        vehicle->onMotorway = true;
        break;
    default:
        printf("Unknown action %d\n", action);
        exit(EXIT_FAILURE);
    }
}

// -----------------------------------------------------------------------------
// Motorway
// -----------------------------------------------------------------------------

Motorway *newMotorway(double sectionLengths[],
                      int numberOfSections,
                      int numberOfBlockagesInAllocation)
{
    if (numberOfBlockagesInAllocation < 0)
    {
        printf("Number of blockage allocations is invalid: %d\n", numberOfBlockagesInAllocation);
        exit(EXIT_FAILURE);
    }

    if (numberOfSections <= 0)
    {
        printf("Number of sections is invalid: %d\n", numberOfSections);
        exit(EXIT_FAILURE);
    }

    Motorway *motorway = malloc(sizeof(Motorway));

    // Initialise the blockages
    motorway->numberOfBlockagesInAllocation = numberOfBlockagesInAllocation;
    motorway->blockages = malloc(sizeof(Blockage) * numberOfBlockagesInAllocation);
    motorway->numberOfBlockages = 0;
    motorway->numberOfBlockagesAllocated = numberOfBlockagesInAllocation;

    // Copy the section lengths
    motorway->numberOfSections = numberOfSections;
    motorway->sectionLengths = malloc(sizeof(double) * numberOfSections);
    memcpy(motorway->sectionLengths, sectionLengths, sizeof(double) * numberOfSections);

    // Calculate the total motorway length
    motorway->motorwayLength = 0.0;
    for (int i = 0; i < motorway->numberOfSections; i++)
    {
        motorway->motorwayLength += motorway->sectionLengths[i];
    }

    return motorway;
}

void freeMotorway(Motorway *motorway)
{
    // Free each of the blockages
    for (int i = 0; i < motorway->numberOfBlockages; i++)
    {
        free(motorway->blockages[i]);
    }

    free(motorway->blockages);
    free(motorway->sectionLengths);
    free(motorway);
}

void addBlockage(Motorway *const motorway,
                 double position,
                 double startTime,
                 double endTime)
{
    if (motorway == NULL)
    {
        printf("Motorway is NULL\n");
        exit(EXIT_FAILURE);
    }

    if (motorway->numberOfBlockagesAllocated == motorway->numberOfBlockages)
    {
        // The blockages have reached capacity, so the memory needs extending
        motorway->numberOfBlockagesAllocated += motorway->numberOfBlockagesInAllocation;
        motorway->blockages = realloc(motorway->blockages,
                                      sizeof(Blockage *) * motorway->numberOfBlockagesAllocated);
    }

    // Index of the new blockage to add
    int idx = motorway->numberOfBlockages;
    motorway->blockages[idx] = malloc(sizeof(Blockage));

    // Store the blockage
    motorway->blockages[idx]->position = position;
    motorway->blockages[idx]->startTime = startTime;
    motorway->blockages[idx]->endTime = endTime;
    motorway->numberOfBlockages += 1;
}

void clearBlockages(Motorway *const motorway)
{
    // Free each of the blockages
    for (int i = 0; i < motorway->numberOfBlockages; i++)
    {
        free(motorway->blockages[i]);
    }

    motorway->numberOfBlockagesAllocated = motorway->numberOfBlockagesInAllocation;
    motorway->blockages = realloc(motorway->blockages,
                                  sizeof(Blockage *) * motorway->numberOfBlockagesAllocated);
    motorway->numberOfBlockages = 0;
}

bool isPathBlocked(const Motorway *const motorway,
                   double startLocation,
                   double endLocation,
                   double currentTime)
{
    if (startLocation > endLocation)
    {
        printf("Invalid start and end location: %f and %f\n", startLocation, endLocation);
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < motorway->numberOfBlockages; i++)
    {
        if ((startLocation <= motorway->blockages[i]->position) &&
            (motorway->blockages[i]->position <= endLocation) &&
            (motorway->blockages[i]->startTime <= currentTime) &&
            (motorway->blockages[i]->endTime > currentTime))
        {
            return true;
        }
    }

    return false;
}

int sectionIndex(const Motorway *const motorway,
                 double location)
{
    if (location < 0.0)
    {
        return BEFORE_MOTORWAY_START;
    }

    double endLocation = 0.0;
    for (int i = 0; i < motorway->numberOfSections; i++)
    {
        endLocation += motorway->sectionLengths[i];
        if (location < endLocation)
        {
            return i;
        }
    }

    return AFTER_MOTORWAY_END;
}

void sectionStartEnd(const Motorway *const motorway,
                     int section,
                     double *start,
                     double *end)
{
    if ((section < 0) || (section >= motorway->numberOfSections))
    {
        printf("Invalid section %d\n", section);
        exit(EXIT_FAILURE);
    }

    *start = 0.0;
    int i = 0;
    while (i < section)
    {
        *start += motorway->sectionLengths[i];
        i++;
    }

    *end = *start + motorway->sectionLengths[i];
}

bool isSectionBlocked(const Motorway *const motorway,
                      double location,
                      double currentTime)
{
    // Get the index of the section that the location is in
    int idx = sectionIndex(motorway, location);

    // If the section index is before the start of the motorway or after the
    // end of the motorway then it is not blocked by definition
    if ((idx == BEFORE_MOTORWAY_START) || (idx == AFTER_MOTORWAY_END))
    {
        return false;
    }

    // Get the start and end locations of the section
    double start, end;
    sectionStartEnd(motorway, idx, &start, &end);

    // Check each blockage to see if it is within [start, end]
    return isPathBlocked(motorway, start, end, currentTime);
}

double sampleFromUniform(double minValue,
                         double maxValue)
{
    double value = (double)rand() / RAND_MAX; // value in range [0,1]
    return minValue + value * (maxValue - minValue);
}

void updateMotorway(Motorway *motorway,
                    double pBlockage,
                    double currentTime,
                    double blockageDuration)
{
    // Draw a sample from a uniform distribution in the range [0,1] to determine
    // if there should be a new blockage
    double sample = sampleFromUniform(0.0, 1.0);
    if (sample > pBlockage)
    {
        return;
    }

    // Determine where the blockage occurs along the motorway
    double position = sampleFromUniform(0.0, motorway->motorwayLength);

    // Add the blockage to the motorway
    addBlockage(motorway, position, currentTime, currentTime + blockageDuration);
}

bool junctionInPath(const Motorway *const motorway,
                    double start,
                    double end)
{
    // First junction is at a distance of zero
    if (start < 0 && end > 0)
    {
        return true;
    }

    double total = 0.0;
    for (int i = 0; i < motorway->numberOfSections; i++)
    {
        total += motorway->sectionLengths[i];
        if (start <= total && end > total)
        {
            return true;
        }
    }

    return false;
}

double endOfMotorwaySection(const Motorway *const motorway,
                            int sectionIndex)
{
    if ((sectionIndex < 0) || (sectionIndex >= motorway->numberOfSections))
    {
        printf("Invalid motorway section index: %d\n", sectionIndex);
        exit(EXIT_FAILURE);
    }

    double distance = 0.0;
    for (int i = 0; i <= sectionIndex; i++)
    {
        distance += motorway->sectionLengths[i];
    }

    return distance;
}

bool isPathToJunctionClear(const Motorway *const motorway,
                           double position,
                           double currentTime)
{
    // Get the section index for the motorway section the position is in
    int index = sectionIndex(motorway, position);

    // Get the location of the next motorway junction
    double junction = endOfMotorwaySection(motorway, index);

    // Return whether the path from the current position to the junction is
    // clear
    return !isPathBlocked(motorway, position, junction, currentTime);
}

bool vehicleIsAtDestination(const Vehicle *const vehicle,
                            const Motorway *const motorway)
{
    if (vehicle->position >= motorway->motorwayLength)
    {
        return true;
    }
    return false;
}

// -----------------------------------------------------------------------------
// Simulation
// -----------------------------------------------------------------------------

Simulation *newSimulation(double *speeds,
                          int numberOfSpeeds,
                          int numberOfRunsPerSpeed,
                          double timeDelta,
                          double pBlockage,
                          double blockageDuration)
{
    if (numberOfSpeeds < 0)
    {
        printf("Invalid number of speeds: %f\n", numberOfSpeeds);
        exit(EXIT_FAILURE);
    }

    if (numberOfRunsPerSpeed < 0)
    {
        printf("Invalid number of runs per speed: %f\n", numberOfRunsPerSpeed);
        exit(EXIT_FAILURE);
    }

    if (timeDelta < 0)
    {
        printf("Invalid timeDelta: %f\n", timeDelta);
        exit(EXIT_FAILURE);
    }

    if ((pBlockage < 0) || (pBlockage > 1.0))
    {
        printf("Invalid pBlockage: %f\n", pBlockage);
        exit(EXIT_FAILURE);
    }

    if (blockageDuration < 0)
    {
        printf("Invalid blockage duration: %f\n", blockageDuration);
        exit(EXIT_FAILURE);
    }

    // Seed the random number generator
    srand(time(NULL));

    Simulation *simulation = malloc(sizeof(Simulation));

    simulation->speeds = speeds;
    simulation->numberOfSpeeds = numberOfSpeeds;
    simulation->numberOfRunsPerSpeed = numberOfRunsPerSpeed;
    simulation->timeDelta = timeDelta;

    // Allocate a 2D array of journey times
    //
    //           0   1     numberOfRunsPerSpeed-1
    // speed 0 [ x , x , ... x ]
    // speed 1 [ x , x , ... x ]
    simulation->journeyTimes = malloc(sizeof(double) * numberOfSpeeds * numberOfRunsPerSpeed);

    // Store the blockage parameters
    simulation->pBlockage = pBlockage;
    simulation->blockageDuration = blockageDuration;

    return simulation;
}

void freeSimulation(Simulation *simulation)
{
    free(simulation->journeyTimes);
    free(simulation);
}

int index2D(int row, int col, int nCols)
{
    return row * nCols + col;
}

void addJourneyResult(Simulation *const simulation,
                      int speedIndex,
                      int testIndex,
                      double time)
{
    int idx = index2D(speedIndex, testIndex, simulation->numberOfRunsPerSpeed);
    simulation->journeyTimes[idx] = time;
}

void meanJourneyTimes(const Simulation *const simulation,
                      double *const result)
{
    for (int i = 0; i < simulation->numberOfSpeeds; i++)
    {
        result[i] = 0.0;
        for (int j = 0; j < simulation->numberOfRunsPerSpeed; j++)
        {
            int idx = index2D(i, j, simulation->numberOfRunsPerSpeed);
            result[i] += simulation->journeyTimes[idx];
        }
        result[i] = result[i] / simulation->numberOfRunsPerSpeed;
    }
}

double runSingleExperiment(Simulation *const simulation,
                           Motorway *const motorway,
                           double speed)
{
    // Setup the motorway
    clearBlockages(motorway);

    // Instantiate the vehicle
    Vehicle *vehicle = newVehicle(speed);

    // Initialise the journey time (in seconds)
    double currentTime = 0.0;

    while (!vehicleIsAtDestination(vehicle, motorway))
    {
        // Update the motorway, which may introduce a blockage
        updateMotorway(motorway,
                       simulation->pBlockage,
                       currentTime,
                       simulation->blockageDuration);

        // Update the vehicle, which may move the vehicle
        updateVehicle(vehicle,
                      motorway,
                      currentTime,
                      simulation->timeDelta);

        currentTime += simulation->timeDelta;
    }

    freeVehicle(vehicle);

    return currentTime;
}

void runSimulation(Simulation *const simulation,
                   Motorway *const motorway)
{
    for (int i = 0; i < simulation->numberOfSpeeds; i++)
    {
        for (int j = 0; j < simulation->numberOfRunsPerSpeed; j++)
        {
            double currentTime = runSingleExperiment(simulation,
                                                     motorway,
                                                     simulation->speeds[i]);

            // Store the time taken for the vehicle to complete the journey
            addJourneyResult(simulation, i, j, currentTime);
        }
    }
}

double mphToMs(double mph)
{
    return (mph * 1609.344) / (60 * 60);
}

void convertSpeeds(const double *const speedsInMph,
                   double *const speedsInMs,
                   int numberOfSpeeds)
{
    for (int i = 0; i < numberOfSpeeds; i++)
    {
        speedsInMs[i] = mphToMs(speedsInMph[i]);
    }
}