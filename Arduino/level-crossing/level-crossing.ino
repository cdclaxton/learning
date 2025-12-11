// Buttons
#define LEFT_BARRIER_UP A0
#define LEFT_BARRIER_DOWN A1
#define RIGHT_BARRIER_UP A2
#define RIGHT_BARRIER_DOWN A3
#define YELLOW_BUTTON A4
#define RED_BUTTON A5
#define BLACK_BUTTON 2

// Buzzer
#define BUZZER 3

// LEDs
#define RED_LED_1 4
#define RED_LED_2 5
#define YELLOW_LED 6

// Motor 1
#define MOTOR1_ENABLE 8
#define MOTOR1_IP1 9
#define MOTOR1_IP2 10

// Motor 2
#define MOTOR2_ENABLE 11
#define MOTOR2_IP1 12
#define MOTOR2_IP2 13

// States of the buttons
bool redLightsFlashing = LOW;
bool redLightsLit = LOW;

bool yellowLightFlashing = LOW;
bool yellowLightLit = LOW;

bool blackState = LOW;

// Minimum time between button presses to debounce
#define debounceButtonTime 1000

// On and off times for the red light
#define RED_ON_CONSTANT_TIME 1000
#define RED_ON_TIME 500
unsigned long lastRedStateChange = millis();
bool redIsOnConstant = LOW;
bool redLeftState = HIGH;
bool redRightState = HIGH;

// Buzzer
#define BUZZER_TIME 500
#define BUZZER_FREQ_1 500
#define BUZZER_FREQ_2 800
unsigned long lastBuzzerStateChange = millis();
bool buzzerState1 = HIGH;

// Last time each button was pressed
unsigned long lastRedPress = millis();
unsigned long lastYellowPress = millis();
unsigned long lastBlackPress = millis();

// Barrier on and off cycles
#define BARRIER_ON_CYCLES 4
#define BARRIER_OFF_CYCLES 15
int numCyclesSinceLastMotor1Move = 0;
int numCyclesSinceLastMotor2Move = 0;

void setup() {
  // Inputs
  pinMode(BLACK_BUTTON, INPUT);
  pinMode(BUZZER, INPUT);

  // Outputs
  pinMode(RED_LED_1, OUTPUT);
  pinMode(RED_LED_2, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);

  pinMode(MOTOR1_ENABLE, OUTPUT);
  pinMode(MOTOR1_IP1, OUTPUT);
  pinMode(MOTOR1_IP2, OUTPUT);

  pinMode(MOTOR2_ENABLE, OUTPUT);
  pinMode(MOTOR2_IP1, OUTPUT);
  pinMode(MOTOR2_IP2, OUTPUT);
}

void raiseBarrier1() {
  digitalWrite(MOTOR1_IP1, HIGH);
  digitalWrite(MOTOR1_IP2, LOW);
}

void lowerBarrier1() {
  digitalWrite(MOTOR1_IP1, LOW);
  digitalWrite(MOTOR1_IP2, HIGH);
}

void holdBarrier1() {
  digitalWrite(MOTOR1_IP1, LOW);
  digitalWrite(MOTOR1_IP2, LOW);  
}

void raiseBarrier2() {
  digitalWrite(MOTOR2_IP1, HIGH);
  digitalWrite(MOTOR2_IP2, LOW);
}

void lowerBarrier2() {
  digitalWrite(MOTOR2_IP1, LOW);
  digitalWrite(MOTOR2_IP2, HIGH);
}

void holdBarrier2() {
  digitalWrite(MOTOR2_IP1, LOW);
  digitalWrite(MOTOR2_IP2, LOW);  
}

void loop() {

  // Current time in milliseconds
  unsigned long currentTime = millis();

  // ----------------------------------------------------------------------------------------------
  // Yellow lights
  // ----------------------------------------------------------------------------------------------

  if ((digitalRead(YELLOW_BUTTON) == HIGH) && (currentTime > (lastYellowPress + debounceButtonTime))) {
    yellowLightLit = !yellowLightLit;
    lastYellowPress = currentTime;

    if (yellowLightLit == HIGH) {
      redLightsFlashing = LOW;
    }
  }  

  // ----------------------------------------------------------------------------------------------
  // Red lights
  // ----------------------------------------------------------------------------------------------

  if ((digitalRead(RED_BUTTON) == HIGH) && (currentTime > (lastRedPress + debounceButtonTime))) {
    redLightsFlashing = !redLightsFlashing;
    lastRedPress = currentTime;

    if (redLightsFlashing == HIGH) {
      yellowLightLit = LOW;
      redIsOnConstant = HIGH;
      redLeftState = HIGH;
      redRightState = HIGH;
      lastRedStateChange = currentTime;
    }
  }

  if ((redIsOnConstant == LOW) && (redLightsFlashing == HIGH) && (currentTime > lastRedStateChange + RED_ON_TIME)) {
    redLeftState  = !redLeftState;
    redRightState = !redRightState;
    lastRedStateChange = currentTime;
  } else if ((redIsOnConstant == HIGH) && (redLightsFlashing == HIGH) && (currentTime > lastRedStateChange + RED_ON_CONSTANT_TIME)) {
    redIsOnConstant = LOW;
    redLeftState = HIGH;
    redRightState = LOW;
    lastRedStateChange = currentTime;
  }

  // ----------------------------------------------------------------------------------------------
  // Buzzer
  // ---------------------------------------------------------------------------------------------- 

  if ((digitalRead(BLACK_BUTTON) == HIGH) && (currentTime > (lastBlackPress + debounceButtonTime))) {
    blackState = !blackState;
    lastBlackPress = currentTime;

    if (blackState == HIGH) {
      buzzerState1 = HIGH;
    }
  }

  if ((blackState == HIGH) && (currentTime > lastBuzzerStateChange + BUZZER_TIME)) {
    buzzerState1 = !buzzerState1;
    lastBuzzerStateChange = currentTime;
    if (buzzerState1 == HIGH) {
      tone(BUZZER, BUZZER_FREQ_1, BUZZER_TIME);
    } else {
      tone(BUZZER, BUZZER_FREQ_2, BUZZER_TIME);
    }
  }

  // ----------------------------------------------------------------------------------------------
  // Set lights
  // ---------------------------------------------------------------------------------------------- 

  digitalWrite(YELLOW_LED, yellowLightLit);
  digitalWrite(RED_LED_1, (redLightsFlashing == HIGH) && (redLeftState == HIGH));
  digitalWrite(RED_LED_2, (redLightsFlashing == HIGH) && (redRightState == HIGH));

  // ----------------------------------------------------------------------------------------------
  // Motor 1 for the left barrier
  // ----------------------------------------------------------------------------------------------   

  if (((digitalRead(LEFT_BARRIER_UP) == HIGH) && (digitalRead(LEFT_BARRIER_DOWN) == LOW)) ||
    ((digitalRead(LEFT_BARRIER_UP) == LOW) && (digitalRead(LEFT_BARRIER_DOWN) == HIGH))) {

      digitalWrite(MOTOR1_ENABLE, HIGH);

      if (numCyclesSinceLastMotor1Move < BARRIER_ON_CYCLES) {
        if (digitalRead(LEFT_BARRIER_UP) == HIGH) {
          raiseBarrier1();
        } else {
          lowerBarrier1();
        }
      } else {
        holdBarrier1();
      }

      if (numCyclesSinceLastMotor1Move == (BARRIER_ON_CYCLES + BARRIER_OFF_CYCLES)) {
        numCyclesSinceLastMotor1Move = 0;
      } else {
        numCyclesSinceLastMotor1Move = numCyclesSinceLastMotor1Move + 1;
      }      
  } else {
    digitalWrite(MOTOR1_ENABLE, LOW);
  }

  // ----------------------------------------------------------------------------------------------
  // Motor 2 for the right barrier
  // ----------------------------------------------------------------------------------------------   

  if (((digitalRead(RIGHT_BARRIER_UP) == HIGH) && (digitalRead(RIGHT_BARRIER_DOWN) == LOW)) ||
    ((digitalRead(RIGHT_BARRIER_UP) == LOW) && (digitalRead(RIGHT_BARRIER_DOWN) == HIGH))) {

      digitalWrite(MOTOR2_ENABLE, HIGH);
      
      if (numCyclesSinceLastMotor2Move < BARRIER_ON_CYCLES) {
        if (digitalRead(RIGHT_BARRIER_UP) == HIGH) {
          raiseBarrier2();
        } else {
          lowerBarrier2();
        }
      } else {
        holdBarrier2();
      }

      if (numCyclesSinceLastMotor2Move == (BARRIER_ON_CYCLES + BARRIER_OFF_CYCLES)) {
        numCyclesSinceLastMotor2Move = 0;
      } else {
        numCyclesSinceLastMotor2Move = numCyclesSinceLastMotor2Move + 1;
      }      
  } else {
    digitalWrite(MOTOR2_ENABLE, LOW);
  }

}
