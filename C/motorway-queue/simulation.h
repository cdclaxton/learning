#include <stdbool.h>
#include <stdlib.h>

#define BEFORE_MOTORWAY_START -1
#define AFTER_MOTORWAY_END -2

// Vehicle actions
#define VEHICLE_STOP 1
#define VEHICLE_MOVE_FORWARD 2
#define VEHICLE_LEAVE_MOTORWAY 3
#define VEHICLE_JOIN_MOTORWAY 4

// -----------------------------------------------------------------------------
// Vehicle
// -----------------------------------------------------------------------------

typedef struct
{
    double position;        // Position along journey in metres
    bool onMotorway;        // Is the vehicle on the motorway?
    double speed;           // Speed in m/s
    double lengthOfJourney; // Total length of the journey in metres
} Vehicle;

// Instantiate a new Vehicle struct.
Vehicle *newVehicle(double speed);

// Free the memory allocated for the Vehicle struct.
void freeVehicle(Vehicle *vehicle);

// What would be the vehicle's new position if it moved?
double predicatedPosition(const Vehicle *const vehicle,
                          double timeDelta);

// Is the vehicle's position within tolerance?
bool positionInDelta(const Vehicle *const vehicle,
                     double position,
                     double tolerance);

// Move the vehicle forward given the time delta (in seconds).
void move(Vehicle *const vehicle,
          double timeDelta);

// -----------------------------------------------------------------------------
// Motorway
// -----------------------------------------------------------------------------

typedef struct
{
    double position;  // Position along the motorway (in metres)
    double startTime; // Start time in seconds
    double endTime;   // End time in seconds
} Blockage;

typedef struct
{
    Blockage **blockages;              // Array of blockages
    int numberOfBlockages;             // Number of blockages in the array
    int numberOfBlockagesAllocated;    // Number of blockages allocated in memory
    int numberOfBlockagesInAllocation; // Number of Blockage spaces allocated at a time
    double *sectionLengths;            // Array of lengths of each section (in metres)
    int numberOfSections;              // Number of sections
    double motorwayLength;             // Total length of the sections
} Motorway;

// Instantiate a new Motorway struct.
Motorway *newMotorway(double sectionLengths[],
                      int numberOfSections,
                      int numberOfBlockagesInAllocation);

// Free the memory allocated for the Motorway struct and its fields.
void freeMotorway(Motorway *motorway);

// Add a time-limited blockage to the motorway.
void addBlockage(Motorway *motorway,
                 double position,
                 double startTime,
                 double endTime);

// Clear all blockages from the motorway.
void clearBlockages(Motorway *const motorway);

// Is the path between the start and end locations blocked in the half-open
// interval [startLocation, endLocation) at the current time?
bool isPathBlocked(const Motorway *const motorway,
                   double startLocation,
                   double endLocation,
                   double currentTime);

// Motorway section index given the location (in metres).
int sectionIndex(const Motorway *const motorway,
                 double location);

// Get the start and end locations of the motorway section such that the section
// occupies the half-open interval [start, end).
void sectionStartEnd(const Motorway *const motorway,
                     int section,
                     double *start,
                     double *end);

// Is the section blocked that the location is in at the current time?
bool isSectionBlocked(const Motorway *const motorway,
                      double location,
                      double currentTime);

// Draw a sample from a continuous uniform distribution.
double sampleFromUniform(double minValue,
                         double maxValue);

// Update the motorway where the probability of a new blockage is given by
// pBlockage.
void updateMotorway(Motorway *motorway,
                    double pBlockage,
                    double currentTime,
                    double blockageDuration);

// Is there a motorway junction between [start, end)?
bool junctionInPath(const Motorway *const motorway,
                    double start,
                    double end);

// Get the position of the end of the motorway section.
double endOfMotorwaySection(const Motorway *const motorway,
                            int sectionIndex);

// Is the path from the current position to the next motorway junction clear
// given the current time?
bool isPathToJunctionClear(const Motorway *const motorway,
                           double position,
                           double currentTime);

// Decide the action the vehicle should take given the motorway state.
int decideVehicleAction(const Vehicle *const vehicle,
                        const Motorway *const motorway,
                        double currentTime,
                        double timeDelta);

// Update the position of the vehicle.
void updateVehicle(Vehicle *vehicle,
                   Motorway *motorway,
                   double currentTime,
                   double timeDelta); // Time delta in seconds

// Is the vehicle at its destination?
bool vehicleIsAtDestination(const Vehicle *const vehicle,
                            const Motorway *const motorway);

// -----------------------------------------------------------------------------
// Simulation
// -----------------------------------------------------------------------------

typedef struct
{
    double *speeds;           // Array of vehicle speeds to test in m/s
    int numberOfSpeeds;       // Length of the array of speeds
    int numberOfRunsPerSpeed; // Number of runs per vehicle speed
    double timeDelta;         // Time delta in seconds
    double *journeyTimes;     // 2D array of journey times
    double pBlockage;         // Probability of a blockage
    double blockageDuration;  // Duration of a blockage in seconds
} Simulation;

// Instantiate a new simulation.
Simulation *newSimulation(double *speeds,
                          int numberOfSpeeds,
                          int numberOfRunsPerSpeed,
                          double timeDelta,
                          double pBlockage,
                          double blockageDuration);

// Free the memory allocated for a simulation.
void freeSimulation(Simulation *simulation);

// Index of an element in a 2D array.
int index2D(int row, int col, int nCols);

// Add a result.
void addJourneyResult(Simulation *const simulation,
                      int speedIndex,
                      int testIndex,
                      double time);

// Mean journey times for each of the speeds.
void meanJourneyTimes(const Simulation *const simulation,
                      double *const result);

// Run a single experiment.
double runSingleExperiment(Simulation *const simulation,
                           Motorway *const motorway,
                           double speed);

// Run the simulation.
void runSimulation(Simulation *const simulation,
                   Motorway *const motorway);

// Convert a speed from mph to m/s.
double mphToMs(double mph);

// Convert speeds from mph to m/s.
void convertSpeeds(const double *const speedsInMph,
                   double *const speedsInMs,
                   int numberOfSpeeds);
