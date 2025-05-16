#include <stdbool.h>

// Get whether the i(th) bit is on or off
char bitState(int value,
              char bitIndex); // Bit index (starting at 0)

// Set the variable states
void setStates(int value,
               char *variables,
               int nVariables);

// Are the actual and expected states equal?
bool statesEqual(char *expected,
                 char *actual,
                 int nVariables);

// Clone the source values into the destination
void cloneStates(char *source,
                 char *destination,
                 int nVariables);

// Build a string with the states
// To use:
// char resultString[100] = {'\0'};
// statesString(states, 3, resultString);
void statesString(char *states,
                  int nVariables,
                  char *resultString);

// Factor of one discrete (binary) variable
//
//   |   x1  | Potential  |
//   |-------|------------|
//   | false | pNotX1     |
//   | true  | pX1        |
double oneFactor(bool x1,
                 double pNotX1,
                 double pX1);

// Factor of two discrete (binary) variables
//
//   |   x1  |   x2  | Potential  |
//   |-------|-------|------------|
//   | false | false | notX1notX2 |
//   | false | true  | notX1X2    |
//   | true  | false | x1NotX2    |
//   | true  | true  | x1X2       |
double twoFactor(bool x1,
                 bool x2,
                 double notX1notX2,
                 double notX1X2,
                 double x1NotX2,
                 double x1X2);