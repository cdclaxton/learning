#include <assert.h>
#include <stdio.h>
#include <math.h>
#include "simulation.h"

#define TOLERANCE 1e-6

bool inTolerance(double expected, double actual, double tolerance)
{
    if (fabs(expected - actual) < tolerance)
    {
        return true;
    }
    return false;
}

void testInTolerance()
{
    assert(inTolerance(1.0, 1.0, 1e-6));
    assert(!inTolerance(0.5, 1.0, 1e-6));
}

void testNewVehicle()
{
    Vehicle *vehicle = newVehicle(25.0);
    assert(vehicle->position == 0.0);
    assert(vehicle->onMotorway == true);
    assert(vehicle->speed == 25.0);
    freeVehicle(vehicle);
}

void testPredicatedPosition()
{
    Vehicle *vehicle = newVehicle(25.0);
    double predicted = predicatedPosition(vehicle, 2.0);
    assert(inTolerance(predicted, 50.0, TOLERANCE));
    freeVehicle(vehicle);
}

void testMove()
{
    Vehicle *vehicle = newVehicle(25.0);

    move(vehicle, 1.0);
    assert(positionInDelta(vehicle, 25.0, TOLERANCE));

    move(vehicle, 2.0);
    assert(positionInDelta(vehicle, 75.0, TOLERANCE));

    freeVehicle(vehicle);
}

void testNewMotorway()
{
    // Lengths of each motorway section in metres
    double sectionLengths[3] = {100.0, 200.0, 250.0};

    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    assert(motorway->numberOfBlockages == 0);
    assert(motorway->numberOfBlockagesInAllocation == 2);
    assert(motorway->numberOfSections == 3);
    assert(motorway->motorwayLength == 550.0);

    freeMotorway(motorway);
}

bool blockageAtIndex(Motorway *motorway,
                     int index,
                     double position,
                     double startTime,
                     double endTime)
{
    if (motorway->numberOfBlockages <= index)
    {
        return false;
    }

    if ((motorway->blockages[index]->position == position) &&
        (motorway->blockages[index]->startTime == startTime) &&
        (motorway->blockages[index]->endTime == endTime))
    {
        return true;
    }

    return false;
}

void testAddBlockage()
{
    // Lengths of each motorway section in metres
    double sectionLengths[3] = {100.0, 200.0, 250.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    assert(motorway->numberOfBlockages == 0);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Add the first blockage
    addBlockage(motorway, 100.0, 2.0, 3.0);
    assert(motorway->numberOfBlockages == 1);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);
    assert(blockageAtIndex(motorway, 0, 100.0, 2.0, 3.0));

    // Add the second blockage
    addBlockage(motorway, 200.0, 10.0, 11.0);
    assert(motorway->numberOfBlockages == 2);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);
    assert(blockageAtIndex(motorway, 0, 100.0, 2.0, 3.0));
    assert(blockageAtIndex(motorway, 1, 200.0, 10.0, 11.0));

    // Add the third blockage, which will cause a reallocation
    addBlockage(motorway, 300.0, 100.0, 110.0);
    assert(motorway->numberOfBlockages == 3);
    assert(motorway->numberOfBlockagesAllocated == 4);
    assert(motorway->numberOfBlockagesInAllocation == 2);
    assert(blockageAtIndex(motorway, 0, 100.0, 2.0, 3.0));
    assert(blockageAtIndex(motorway, 1, 200.0, 10.0, 11.0));
    assert(blockageAtIndex(motorway, 2, 300.0, 100.0, 110.0));

    freeMotorway(motorway);
}

void testClearBlockages()
{
    // Instantiate a new motorway
    double sectionLengths[3] = {100.0, 200.0, 250.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    assert(motorway->numberOfBlockages == 0);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Add a blockage
    addBlockage(motorway, 300.0, 100.0, 110.0);
    assert(motorway->numberOfBlockages == 1);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Add another blockage
    addBlockage(motorway, 300.0, 100.0, 110.0);
    assert(motorway->numberOfBlockages == 2);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Clear the blockages
    clearBlockages(motorway);
    assert(motorway->numberOfBlockages == 0);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Add a blockage
    addBlockage(motorway, 300.0, 100.0, 110.0);
    assert(motorway->numberOfBlockages == 1);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Add another blockage
    addBlockage(motorway, 300.0, 100.0, 110.0);
    assert(motorway->numberOfBlockages == 2);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Add another blockage
    addBlockage(motorway, 300.0, 100.0, 110.0);
    assert(motorway->numberOfBlockages == 3);
    assert(motorway->numberOfBlockagesAllocated == 4);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    // Clear the blockages
    clearBlockages(motorway);
    assert(motorway->numberOfBlockages == 0);
    assert(motorway->numberOfBlockagesAllocated == 2);
    assert(motorway->numberOfBlockagesInAllocation == 2);

    freeMotorway(motorway);
}

void testIsPathBlocked()
{
    double sectionLengths[3] = {100.0, 200.0, 250.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    // Check if the path is blocked when there are no blockages
    assert(!isPathBlocked(motorway, 50.0, 75.0, 10.0));

    // Add two blockages
    addBlockage(motorway, 100.0, 2.0, 8.0);
    addBlockage(motorway, 200.0, 10.0, 11.0);

    assert(!isPathBlocked(motorway, 50.0, 75.0, 10.0));

    // Path straddles the first blockage
    assert(!isPathBlocked(motorway, 95.0, 105.0, 1.0)); // before
    assert(isPathBlocked(motorway, 95.0, 105.0, 6.0));  // during
    assert(!isPathBlocked(motorway, 95.0, 105.0, 9.0)); // after

    // Path starts on a blockage
    assert(isPathBlocked(motorway, 100.0, 110.0, 6.0));

    // Path is between blockages
    assert(!isPathBlocked(motorway, 165.0, 175.0, 10.0));

    // Path straddles the second blockage
    assert(isPathBlocked(motorway, 180.0, 220.0, 10.5));
    assert(!isPathBlocked(motorway, 180.0, 220.0, 11.0));

    // Path is after the second blockage
    assert(!isPathBlocked(motorway, 201.0, 220.0, 10.5));

    freeMotorway(motorway);
}

void testSectionIndex()
{
    // 0         100.0                300.0 350.0  <-- distance from start
    // |----------|--------------------|-----|
    // |          |                    |     |
    // |----------|--------------------|-----|
    //      0                1            2        <-- section index

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    assert(sectionIndex(motorway, -1.0) == BEFORE_MOTORWAY_START);
    assert(sectionIndex(motorway, 0.0) == 0);
    assert(sectionIndex(motorway, 99.0) == 0);
    assert(sectionIndex(motorway, 100.0) == 1);
    assert(sectionIndex(motorway, 300.0) == 2);
    assert(sectionIndex(motorway, 349.0) == 2);
    assert(sectionIndex(motorway, 350.0) == AFTER_MOTORWAY_END);

    freeMotorway(motorway);
}

void testSectionStartEnd()
{
    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    double start, end;

    // Section 0
    sectionStartEnd(motorway, 0, &start, &end);
    assert(start == 0.0);
    assert(end == 100.0);

    // Section 1
    sectionStartEnd(motorway, 1, &start, &end);
    assert(start == 100.0);
    assert(end == 300.0);

    // Section 2
    sectionStartEnd(motorway, 2, &start, &end);
    assert(start == 300.0);
    assert(end == 350.0);

    freeMotorway(motorway);
}

void testIsSectionBlocked()
{
    // 0         100.0                300.0 350.0  <-- distance from start
    // |----------|--------------------|-----|
    // |          |                    |     |     <-- blockage positions
    // |----------|--------------------|-----|
    //      0                1            2        <-- section index

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    // No blockages
    assert(!isSectionBlocked(motorway, 0.0, 10.0)); // start
    assert(!isSectionBlocked(motorway, 50.0, 10.0));
    assert(!isSectionBlocked(motorway, 100.0, 10.0)); // on boundary
    assert(!isSectionBlocked(motorway, 400.0, 10.0)); // after the end

    // Add a blockage in section 0 during the interval [20s, 30s)
    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |    *     |                    |     |
    // |----------|--------------------|-----|
    //      0                1            2

    addBlockage(motorway, 50.0, 20.0, 30.0);

    assert(!isSectionBlocked(motorway, 0.0, 10.0)); // before blockage occurs
    assert(isSectionBlocked(motorway, 0.0, 25.0));  // during blockage
    assert(!isSectionBlocked(motorway, 0.0, 30.0)); // after blockage

    assert(isSectionBlocked(motorway, 75.0, 25.0));
    assert(!isSectionBlocked(motorway, 100.0, 25.0));
    assert(!isSectionBlocked(motorway, 300.0, 25.0));
    assert(!isSectionBlocked(motorway, 325.0, 25.0));

    // Add a blockage in section 1 during the interval [15s, 25s)
    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |    *     |           *        |     |
    // |----------|--------------------|-----|
    //      0                1            2

    addBlockage(motorway, 150.0, 15.0, 25.0);

    assert(!isSectionBlocked(motorway, 0.0, 10.0)); // before blockage occurs
    assert(isSectionBlocked(motorway, 0.0, 25.0));  // during blockage
    assert(!isSectionBlocked(motorway, 0.0, 30.0)); // after blockage

    assert(isSectionBlocked(motorway, 75.0, 25.0));
    assert(isSectionBlocked(motorway, 100.0, 20.0));
    assert(!isSectionBlocked(motorway, 300.0, 20.0));
    assert(!isSectionBlocked(motorway, 325.0, 20.0));

    freeMotorway(motorway);
}

void testSampleFromUniform()
{
    double sample;
    for (int i = 0; i < 100; i++)
    {
        sample = sampleFromUniform(2.0, 5.0);
        assert(2.0 <= sample && sample <= 5.0);
    }
}

void testUpdateMotorway()
{
    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);
    assert(motorway->numberOfBlockages == 0);

    // pBlockage = 0.0
    updateMotorway(motorway, 0.0, 25.0, 5.0);
    assert(motorway->numberOfBlockages == 0);

    // pBlockage = 1.0
    updateMotorway(motorway, 1.0, 30.0, 5.0);
    assert(motorway->numberOfBlockages == 1);
    assert(motorway->blockages[0]->startTime == 30.0);
    assert(motorway->blockages[0]->endTime == 35.0);
    assert(0.0 <= motorway->blockages[0]->position &&
           motorway->blockages[0]->position <= 350.0);

    freeMotorway(motorway);
}

void testJunctionInPath()
{
    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |          |                    |     |
    // |----------|--------------------|-----|
    // *          *                    *     *  <-- junctions

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    assert(!junctionInPath(motorway, 50.0, 60.0));
    assert(!junctionInPath(motorway, 95.0, 100.0));
    assert(junctionInPath(motorway, 95.0, 105.0));
    assert(junctionInPath(motorway, 295.0, 305.0));
    assert(junctionInPath(motorway, 345.0, 355.0));

    freeMotorway(motorway);
}

void testDecideVehicleAction()
{
    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |          |          #         |     |  <-- blockages
    // |----------|--------------------|-----|
    // *          *                    *     *  <-- junctions

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);
    addBlockage(motorway, 200.0, 20.0, 80.0);

    // Vehicle is at the start of motorway
    Vehicle *vehicle = newVehicle(10.0);
    assert(decideVehicleAction(vehicle, motorway, 0.0, 1.0) == VEHICLE_MOVE_FORWARD);

    // Vehicle is in a clear section
    vehicle->position = 50.0;
    assert(decideVehicleAction(vehicle, motorway, 20.0, 1.0) == VEHICLE_MOVE_FORWARD);

    // Vehicle is about to pass the junction, but the next section has a
    // blockage
    vehicle->position = 99.0;
    assert(decideVehicleAction(vehicle, motorway, 60.0, 1.0) == VEHICLE_LEAVE_MOTORWAY);

    // Vehicle is about to pass the junction and the next section had a
    // blockage (which has now cleared)
    vehicle->position = 99.0;
    assert(decideVehicleAction(vehicle, motorway, 90.0, 1.0) == VEHICLE_MOVE_FORWARD);

    // Vehicle has passed the junction, but there is a blockage far ahead
    vehicle->position = 101.0;
    assert(decideVehicleAction(vehicle, motorway, 60.0, 1.0) == VEHICLE_MOVE_FORWARD);

    // Vehicle is just before the blockage
    vehicle->position = 199.99;
    assert(decideVehicleAction(vehicle, motorway, 60.0, 1.0) == VEHICLE_STOP);

    // Vehicle is just before a blockage that has cleared
    vehicle->position = 199.99;
    assert(decideVehicleAction(vehicle, motorway, 90.0, 1.0) == VEHICLE_MOVE_FORWARD);

    // Vehicle is just before the blockage, but is not on the motorway
    vehicle->onMotorway = false;
    vehicle->position = 97.0;
    assert(decideVehicleAction(vehicle, motorway, 60.0, 1.0) == VEHICLE_MOVE_FORWARD);

    // Vehicle is off the motorway, but can rejoin
    vehicle->onMotorway = false;
    vehicle->position = 299.0;
    assert(decideVehicleAction(vehicle, motorway, 100.0, 1.0) == VEHICLE_JOIN_MOTORWAY);

    freeMotorway(motorway);

    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |        # |                    |     |  <-- blockages
    // |----------|--------------------|-----|
    // *          *                    *     *  <-- junctions

    motorway = newMotorway(sectionLengths, 3, 2);
    addBlockage(motorway, 98.0, 20.0, 80.0);

    // Vehicle is just before the blockage
    vehicle->onMotorway = true;
    vehicle->position = 97.0;
    assert(decideVehicleAction(vehicle, motorway, 60.0, 1.0) == VEHICLE_STOP);

    // Vehicle is off the motorway
    vehicle->onMotorway = false;
    vehicle->position = 97.0;
    assert(decideVehicleAction(vehicle, motorway, 60.0, 1.0) == VEHICLE_JOIN_MOTORWAY);

    freeMotorway(motorway);
    freeVehicle(vehicle);
}

void testUpdateVehicle()
{
    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |          |          #         |     |  <-- blockages
    // |----------|--------------------|-----|
    // *          *                    *     *  <-- junctions

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);
    addBlockage(motorway, 200.0, 20.0, 80.0);

    // Vehicle moving at 10 m/s at the start of the motorway
    Vehicle *vehicle = newVehicle(10.0);

    updateVehicle(vehicle, motorway, 10.0, 1.0);
    assert(inTolerance(10.0, vehicle->position, 1e-6));
    assert(vehicle->onMotorway);

    // Vehicle is just prior to the junction, where the next section is blocked
    vehicle->position = 99.0;
    updateVehicle(vehicle, motorway, 60.0, 1.0);
    assert(inTolerance(109.0, vehicle->position, 1e-6));
    assert(!vehicle->onMotorway);

    // Vehicle is just prior to the blockage
    vehicle->position = 199.0;
    vehicle->onMotorway = true;
    updateVehicle(vehicle, motorway, 60.0, 1.0);
    assert(inTolerance(199.0, vehicle->position, 1e-6));
    assert(vehicle->onMotorway);

    // Vehicle is on the parallel road from the motorway, just prior to the
    // blockage
    vehicle->position = 199.0;
    vehicle->onMotorway = false;
    updateVehicle(vehicle, motorway, 60.0, 1.0);
    assert(inTolerance(209.0, vehicle->position, 1e-6));
    assert(!vehicle->onMotorway);

    // Vehicle is on the parallel road, but can rejoin
    vehicle->position = 299.0;
    vehicle->onMotorway = false;
    updateVehicle(vehicle, motorway, 60.0, 1.0);
    assert(inTolerance(309.0, vehicle->position, 1e-6));
    assert(vehicle->onMotorway);

    freeMotorway(motorway);
    freeVehicle(vehicle);
}

void testVehicleIsAtDestination()
{
    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    Vehicle *vehicle = newVehicle(25.0);

    vehicle->position = 10.0;
    assert(!vehicleIsAtDestination(vehicle, motorway));

    vehicle->position = 345.0;
    assert(!vehicleIsAtDestination(vehicle, motorway));

    vehicle->position = 350.0;
    assert(vehicleIsAtDestination(vehicle, motorway));

    vehicle->position = 400.0;
    assert(vehicleIsAtDestination(vehicle, motorway));

    freeMotorway(motorway);
    freeVehicle(vehicle);
}

void testEndOfMotorwaySection()
{
    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |     0    |          1         |  2  |
    // |----------|--------------------|-----|

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    assert(endOfMotorwaySection(motorway, 0) == 100.0);
    assert(endOfMotorwaySection(motorway, 1) == 300.0);
    assert(endOfMotorwaySection(motorway, 2) == 350.0);

    freeMotorway(motorway);
}

void testIsPathToJunctionClear()
{
    // 0         100.0                300.0 350.0
    // |----------|--------------------|-----|
    // |        # |                    |     |  <-- blockages
    // |----------|--------------------|-----|
    // *          *                    *     *  <-- junctions

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);
    addBlockage(motorway, 98.0, 20.0, 80.0);

    // Blockage present
    assert(!isPathToJunctionClear(motorway, 97.0, 60.0));

    // Blockage that has cleared
    assert(isPathToJunctionClear(motorway, 97.0, 81.0));

    // Position is after the blockage
    assert(isPathToJunctionClear(motorway, 98.1, 60.0));

    // Section 1
    assert(isPathToJunctionClear(motorway, 290.0, 60.0));

    // Section 2
    assert(isPathToJunctionClear(motorway, 340.0, 60.0));

    freeMotorway(motorway);
}

void testNewSimulation()
{
    double speeds[] = {55, 60, 65};
    int numberOfSpeeds = 3;
    int numberOfRunsPerSpeed = 10;
    double timeDelta = 1.0;
    double pBlockage = 0.01;
    double blockageDuration = 60.0;

    Simulation *simulation = newSimulation(speeds,
                                           numberOfSpeeds,
                                           numberOfRunsPerSpeed,
                                           timeDelta,
                                           pBlockage,
                                           blockageDuration);

    assert(simulation->speeds[0] == 55);
    assert(simulation->speeds[1] == 60);
    assert(simulation->speeds[2] == 65);
    assert(simulation->numberOfSpeeds == numberOfSpeeds);
    assert(simulation->numberOfRunsPerSpeed == numberOfRunsPerSpeed);
    assert(simulation->timeDelta == timeDelta);
    assert(simulation->pBlockage == pBlockage);
    assert(simulation->blockageDuration == blockageDuration);

    freeSimulation(simulation);
}

void testIndex2D()
{
    // [0]
    // [1]
    // [2]
    assert(index2D(0, 0, 1) == 0);
    assert(index2D(1, 0, 1) == 1);
    assert(index2D(2, 0, 1) == 2);

    // [0, 1]
    // [2, 3]
    // [4, 5]
    assert(index2D(0, 0, 2) == 0);
    assert(index2D(0, 1, 2) == 1);
    assert(index2D(1, 0, 2) == 2);
    assert(index2D(1, 1, 2) == 3);
    assert(index2D(2, 0, 2) == 4);
    assert(index2D(2, 1, 2) == 5);

    // [0, 1, 2]
    // [3, 4, 5]
    assert(index2D(0, 0, 3) == 0);
    assert(index2D(0, 1, 3) == 1);
    assert(index2D(0, 2, 3) == 2);
    assert(index2D(1, 0, 3) == 3);
    assert(index2D(1, 1, 3) == 4);
    assert(index2D(1, 2, 3) == 5);
}

void testMeanJourneyTimes()
{
    double speeds[] = {55, 60};
    int numberOfSpeeds = 2;
    Simulation *simulation = newSimulation(speeds,
                                           numberOfSpeeds,
                                           3,
                                           1.0,
                                           0.01,
                                           60.0);

    // Build a set of results:
    //
    // Speed 0  [ 67.0, 71.0, 69.0 ]  --> mean = 69.0
    // Speed 1  [ 45.0, 34.0, 41.0 ]  --> mean = 40.0
    addJourneyResult(simulation, 0, 0, 67.0);
    addJourneyResult(simulation, 0, 1, 71.0);
    addJourneyResult(simulation, 0, 2, 69.0);
    addJourneyResult(simulation, 1, 0, 45.0);
    addJourneyResult(simulation, 1, 1, 34.0);
    addJourneyResult(simulation, 1, 2, 41.0);

    // Calculate the mean journey times
    double result[2] = {-1, -1};
    meanJourneyTimes(simulation, result);

    assert(inTolerance(69.0, result[0], 1e-6));
    assert(inTolerance(40.0, result[1], 1e-6));

    freeSimulation(simulation);
}

void testRunSingleExperiment()
{
    // Run a simulation where there can be no blockages
    double speeds[] = {2};
    int numberOfSpeeds = 2;
    Simulation *simulation = newSimulation(speeds,
                                           numberOfSpeeds,
                                           3,
                                           1.0,
                                           0.00,
                                           60.0);

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    double time = runSingleExperiment(simulation,
                                      motorway,
                                      2.0);
    assert(inTolerance(175.0, time, 1e-6));

    freeSimulation(simulation);
    freeMotorway(motorway);
}

void testRunSimulation()
{
    // Run a simulation where there can be no blockages
    double speeds[] = {2, 3};
    int numberOfSpeeds = 2;
    Simulation *simulation = newSimulation(speeds,
                                           numberOfSpeeds,
                                           3,
                                           1.0,
                                           0.00,
                                           60.0);

    double sectionLengths[3] = {100.0, 200.0, 50.0};
    Motorway *motorway = newMotorway(sectionLengths, 3, 2);

    runSimulation(simulation, motorway);

    freeSimulation(simulation);
    freeMotorway(motorway);
}

void testMphToMs()
{
    double ms = mphToMs(1.0);
    assert(inTolerance(0.447040, ms, 1e-6));
}

void testConvertSpeeds()
{
    double speedsInMph[] = {1, 2};
    double speedsInMs[] = {-1, -1};

    convertSpeeds(speedsInMph, speedsInMs, 2);

    assert(inTolerance(0.447040, speedsInMs[0], 1e-6));
    assert(inTolerance(0.447040 * 2, speedsInMs[1], 1e-6));
}

int main(void)
{
    testInTolerance();
    testNewVehicle();
    testPredicatedPosition();
    testMove();
    testNewMotorway();
    testAddBlockage();
    testClearBlockages();
    testIsPathBlocked();
    testSectionIndex();
    testSectionStartEnd();
    testIsSectionBlocked();
    testSampleFromUniform();
    testUpdateMotorway();
    testJunctionInPath();
    testVehicleIsAtDestination();
    testEndOfMotorwaySection();
    testIsPathToJunctionClear();
    testDecideVehicleAction();
    testUpdateVehicle();
    testNewSimulation();
    testIndex2D();
    testMeanJourneyTimes();
    testRunSingleExperiment();
    testRunSimulation();
    testMphToMs();
    testConvertSpeeds();
}