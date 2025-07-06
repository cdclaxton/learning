#include "Arduino_LED_Matrix.h"

ArduinoLEDMatrix matrix;

#define NUM_LEDS 96
byte frame[8][12] = {
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};

void setup() {
  Serial.begin(115200);
  matrix.begin();
  matrix.renderBitmap(frame, 8, 12);
}

void loop() {

  // Put all LEDs to on as the randomisation takes a few seconds
  fullFrame();
  matrix.renderBitmap(frame, 8, 12);

  int sequence[NUM_LEDS];
  for (int i=0; i<NUM_LEDS; i++) {
    sequence[i] = i;
  }

  for (int i=0; i<NUM_LEDS-1; i++) {
    long j = random(NUM_LEDS);
    byte temp = sequence[j];
    sequence[j] = sequence[i];
    sequence[i] = temp;
  }

  // Turn all LEDs off
  clearFrame();
  matrix.renderBitmap(frame, 8, 12);

  // Light up the LEDs one at a time
  for (int i=0; i<NUM_LEDS; i++) {
    int col = sequence[i] % 12;
    int row = (sequence[i] - col) / 12;
    frame[row][col] = 1;
    matrix.renderBitmap(frame, 8, 12);
    delay(100);
  }
}

// Set all LEDs in the matrix to on.
void fullFrame() {
  for (int row=0; row<8; row++) {
    for (int col=0; col<12; col++) {
      frame[row][col] = 1;
    }
  }
}

// Clear the frame by setting all LEDs to off.
void clearFrame() {
  for (int row=0; row<8; row++) {
    for (int col=0; col<12; col++) {
      frame[row][col] = 0;
    }
  }
}
