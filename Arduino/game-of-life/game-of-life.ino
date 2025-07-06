#include "Arduino_LED_Matrix.h"

ArduinoLEDMatrix matrix;

// Number of rows in the matrix of LEDs
#define NUM_ROWS 8

// Number of columns in the matrix of LEDs
#define NUM_COLS 12

// Probability that a cell is alive initially
#define P_CELL_ALIVE 0.3

// LED frame
byte frame0[NUM_ROWS][NUM_COLS] = {
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};

byte frame1[NUM_ROWS][NUM_COLS] = {
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};

byte currentFrame = 0;
int numberOfUnchangedFrames = 0;

void setup() {
  Serial.begin(115200);
  matrix.begin();

  initialiseMatrix(P_CELL_ALIVE);
  showFrame();
}

void loop() {

  // Calculate the next frame
  calculateNextFrame();

  // Switch over the current frame
  if (currentFrame == 0) {
    currentFrame = 1;
  } else {
    currentFrame = 0;
  }

  // Show the current frame
  showFrame();
  delay(250);

  if (currentAndPreviousFramesSame()) {
    numberOfUnchangedFrames += 1;
    if (numberOfUnchangedFrames == 5) {
      initialiseMatrix(P_CELL_ALIVE);
      numberOfUnchangedFrames = 0;
    }
  }
}

void initialiseMatrix(float p) {

  // Set the seed of the random number generator
  srand(analogRead(A0));

  // r will hold a random number in the range 0 to 1
  float r;

  // Randomly populate frame 0
  for (int row=0; row<NUM_ROWS; row++) {
    for (int col=0; col<NUM_COLS; col++) {
      r = (float)rand() / (float)RAND_MAX;
      if (r <= p) {
        frame0[row][col] = 1;
      } else {
        frame0[row][col] = 0;
      }
    }
  }

  // Clear frame 1
  clearFrame(1);

  // Set frame 0 as the current frame
  currentFrame = 0;
}

// Clear the frame by setting all LEDs to off.
void clearFrame(byte frame) {
  for (int row=0; row<8; row++) {
    for (int col=0; col<12; col++) {
      if (frame == 0) {
        frame0[row][col] = 0;
      } else {
        frame1[row][col] = 0;
      }
    }
  }
}

void showFrame() {
  if (currentFrame == 0) {
    matrix.renderBitmap(frame0, 8, 12);
  } else {
    matrix.renderBitmap(frame1, 8, 12);
  }
}

void calculateNextFrame() {

  byte cellIsAlive;
  byte numberOfLiveNeighbourCells;

  // Clear the next frame
  if (currentFrame == 0) {
    clearFrame(1);
  } else {
    clearFrame(0);
  }

  for (int i=0; i<NUM_ROWS; i++) {
    for (int j=0; j<NUM_COLS; j++) {

      // Is the (i,j) cell alive in the current frame?
      cellIsAlive = cellIsAliveInCurrentFrame(i, j);
      
      // Calculate the number of live cells surrounding the (i,j) cell
      numberOfLiveNeighbourCells = calcNumberOfLiveNeighbourCells(i, j);

      // Set whether the (i,j) cell is alive or dead in the next frame
      setCellInNextFrame(i, j, cellLivesGivenNeighbours(cellIsAlive, numberOfLiveNeighbourCells));
    }
  }
}

// Does the cell given its current state and the number of neighbouring cells that are alive?
byte cellLivesGivenNeighbours(byte cellIsAlive, byte numberOfLiveNeighbourCells) {

  if (cellIsAlive) {
    if (numberOfLiveNeighbourCells < 2) {
      return 0; // Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    } else if ((numberOfLiveNeighbourCells == 2) || (numberOfLiveNeighbourCells == 3)) {
      return 1; // Any live cell with two or three live neighbours lives on to the next generation.
    } else if (numberOfLiveNeighbourCells > 3) {
      return 0; // Any live cell with more than three live neighbours dies, as if by overpopulation.
    }
  } else if (!cellIsAlive && (numberOfLiveNeighbourCells == 3)) {
    return 1; // Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
  }

  return 0;
}

// Set the cell to be alive or dead in the next frame.
void setCellInNextFrame(byte i, byte j, byte live) {
  if (currentFrame == 0) {
    frame1[i][j] = live;
  } else {
    frame0[i][j] = live;
  }
}

// Is the (i,j) cell alive in the current frame?
byte cellIsAliveInCurrentFrame(byte i, byte j) {
  if (currentFrame == 0) {
    return frame0[i][j];
  }
  return frame1[i][j];
}

// Calculate the number of live neighbour cells to (i,j) in the 8 surrounding cells.
byte calcNumberOfLiveNeighbourCells(byte i, byte j) {

  byte total = 0;

  for (int row=i-1; row<=i+1; row++) {
    if ((row < 0) || (row >= NUM_ROWS)) {
      continue;
    }

    for (int col=j-1; col<=j+1; col++) {
      if ((col < 0) || (col >= NUM_COLS)) {
        continue;
      }

      if ((row == i) && (col == j)) {
        continue;
      }

      total += cellIsAliveInCurrentFrame(row, col);
    }
  }

  return total;
}

bool currentAndPreviousFramesSame() {

  for (byte i=0; i<NUM_ROWS; i++) {
    for (byte j=0; j<NUM_COLS; j++) {
      if (frame0[i][j] != frame1[i][j]) {
        return false;
      }
    }
  }

  return true;
}