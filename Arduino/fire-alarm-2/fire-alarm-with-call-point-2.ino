#define TRIGGERED_LED D0
#define NOT_TRIGGERED_LED D1
#define KEY_IN_LED D2
#define SOUNDER_LED D3
#define KEY_SWITCH D4
#define RESET_BUTTON D5
#define ACTIVATE_BUTTON D6
#define CALL_POINT_LED D7
#define CALL_POINT_SWITCH D8
#define AUDIO_BOARD_IO0 D9
#define AUDIO_BOARD_IO1 D10

/*********************************************************************
 * LED -- A non-flashing LED
 *********************************************************************/

struct LED {
  pin_size_t pinNumber;  // Pin to which the LED is attached
  bool state;            // State of the LED
};

// Define a new LED connected to pinNumber with the specified initial state.
struct LED newLED(pin_size_t pinNumber, bool initial_state) {
  struct LED led = {
    pinNumber,
    initial_state
  };
  return led;
}

// Setup the LED (call in the setup() block).
void setupLED(struct LED *led) {
  pinMode(led->pinNumber, OUTPUT);
}

// Change the state of the LED.
void changeLEDState(struct LED *led, bool state) {
  led->state = state;
}

// Update the LED.
void updateLED(struct LED *led) {
  digitalWrite(led->pinNumber, led->state);
}

/*********************************************************************
 * Flashing LED
 *********************************************************************/

struct FlashingLED {
  pin_size_t pinNumber;      // Pin to which the LED is attached
  bool state;                // State of the LED (flashing or off)
  int onTimeMillis;          // On time in milliseconds
  int offTimeMillis;         // Off time in milliseconds

  // Internal
  unsigned long lastChange;  // Last time it went from on to off or off to on
  bool isHigh;               // True if on, otherwise off
};

// Define a new flashing LED connected to pinNumber with a given initial state (HIGH or LOW).
// The LED is on (lit) for onTimeMillis milliseconds and off for offTimeMillis milliseconds.
struct FlashingLED newFlashingLED(pin_size_t pinNumber, bool initial_state, int onTimeMillis, int offTimeMillis) {
  struct FlashingLED led = {
    pinNumber,
    initial_state,
    onTimeMillis,
    offTimeMillis,
    millis(),
    LOW
  };
  return led;
}

// Setup the flashing LED (call in the setup() block).
void setupFlashingLED(struct FlashingLED *led) {
  pinMode(led->pinNumber, OUTPUT);
}

// Change the state of the flashing LED.
void changeFlashingLEDState(struct FlashingLED *led, bool state) {
  if (state == LOW && led->state == HIGH) {
    led->isHigh = LOW;
    led->lastChange = millis();
  }

  led->state = state;
}

// Update the flashing LED.
void updateFlashingLED(struct FlashingLED *led) {
  if (led->state == LOW) {
    digitalWrite(led->pinNumber, LOW);
    return;
  }

  unsigned long currentTime = millis();

  if ((led->isHigh == HIGH) && (currentTime > (led->lastChange + led->onTimeMillis))) {
    led->isHigh = LOW;
    led->lastChange = currentTime;
  } else if ((led->isHigh == LOW) && (currentTime > (led->lastChange + led->offTimeMillis))) {
    led->isHigh = HIGH;
    led->lastChange = currentTime;
  }

  digitalWrite(led->pinNumber, led->isHigh);
}

/*********************************************************************
 * Debounced switch
 *********************************************************************/

struct DebouncedSwitch {
  pin_size_t pinNumber;         // Pin to which the button is attached  
  int debounceDelay;            // Debounce delay in milliseconds
  bool invert;                  // Invert the switch?

  // Internal
  unsigned long lastChangeTime;
  bool lastState;
  bool state;    
};

// Create a new debounced switch.
struct DebouncedSwitch newDebouncedSwitch(pin_size_t pinNumber, int debounceDelay, bool invert) {
  struct DebouncedSwitch debouncedSwitch = {
    pinNumber,
    debounceDelay,
    invert,
    millis(),
    LOW,
    LOW
  };
  return debouncedSwitch;
}

void setupDebouncedSwitch(struct DebouncedSwitch *debouncedSwitch) {
  pinMode(debouncedSwitch->pinNumber, INPUT);  
}

void updateDebouncedSwitch(struct DebouncedSwitch *debouncedSwitch) {

  // Get the current state of the switch
  bool currentReading = digitalRead(debouncedSwitch->pinNumber);

  // Current time in milliseconds
  unsigned long currentTime = millis();

  if ((currentReading == debouncedSwitch->lastState) & (currentTime > (debouncedSwitch->lastChangeTime + debouncedSwitch->debounceDelay))) {
    if (debouncedSwitch->invert) {
      debouncedSwitch->state = !currentReading;
    } else {
      debouncedSwitch->state = currentReading;
    }
    debouncedSwitch->lastChangeTime = currentTime;
  }

  debouncedSwitch->lastState = currentReading;
}

/*********************************************************************
 * Debounced button
 *********************************************************************/

struct DebouncedButton {
  pin_size_t pinNumber;      // Pin to which the button is attached
  bool hasPullUpResistor;    // Does the pin have an internal pull-up resistor?
  int debounceDelay;         // Debounce delay in milliseconds

  // Internal
  bool state;
  unsigned long lastPressTime;
};

// Create a new debounced button. If the pin has an internal pull up resistor then
// set hasPullUpResistor to HIGH.
struct DebouncedButton newDebouncedButton(pin_size_t pinNumber, bool hasPullUpResistor, int debounceDelay) {
  struct DebouncedButton button = {
    pinNumber,
    hasPullUpResistor,
    debounceDelay,
    LOW,
    0
  };
  return button;
}

// Setup the debounced button (call in the setup() block).
void setupDebouncedButton(struct DebouncedButton *button) {
  if (button->hasPullUpResistor == HIGH) {
    pinMode(button->pinNumber, INPUT_PULLUP);
  } else {
    pinMode(button->pinNumber, INPUT);
  }
}

// Has the button been pressed?
bool updateDebouncedButton(struct DebouncedButton *button) {

  // Get the current state of the button
  bool currentReading;
  if (button->hasPullUpResistor) {
    currentReading = !digitalRead(button->pinNumber);
  }  else {
    currentReading = digitalRead(button->pinNumber);
  }

  unsigned long currentTime = millis();

  if ((currentTime <= button->lastPressTime + button->debounceDelay) && (button->state == HIGH)) {
    button->state = LOW;
  } else if ((currentTime > button->lastPressTime + button->debounceDelay) && (currentReading == HIGH)) {
    button->lastPressTime = currentTime;
    button->state = HIGH;
  }

  return button->state;
}

/*********************************************************************
 * Audio module
 *********************************************************************/

struct AudioModule {
  pin_size_t io_pin_1;
  pin_size_t io_pin_2;
  int state;
  long timeForSound2;         // Time in milliseconds
  long sound2TriggeredTime;   // Time in milliseconds at which sound 2 was triggered
};

void alarmTriggered(struct AudioModule *module) {
  module->state = 1;
}

void alarmCancelled(struct AudioModule *module) {
  module->state = 2;
  module->sound2TriggeredTime = millis();
}

void updateAudioModule(struct AudioModule *module) {
  if (module->state == 0) {
    digitalWrite(AUDIO_BOARD_IO0, HIGH);
    digitalWrite(AUDIO_BOARD_IO1, HIGH);   
  } else if (module->state == 1) {
    digitalWrite(AUDIO_BOARD_IO0, LOW);
    digitalWrite(AUDIO_BOARD_IO1, HIGH);
  } else if (module->state == 2) {
    if (millis() > (module->sound2TriggeredTime + module->timeForSound2)) {
      module->state = 0;
    } else {
      digitalWrite(AUDIO_BOARD_IO0, HIGH);
      digitalWrite(AUDIO_BOARD_IO1, LOW);
    }
  } 
}

/*********************************************************************
 * Main code
 *********************************************************************/

struct AudioModule audioModule = {
  AUDIO_BOARD_IO0,
  AUDIO_BOARD_IO1,
  0,
  1200,
  millis()
};

struct FlashingLED triggeredLED = newFlashingLED(TRIGGERED_LED, LOW, 300, 300);
struct LED notTriggeredLED = newLED(NOT_TRIGGERED_LED, LOW);
struct LED keyInLED = newLED(KEY_IN_LED, LOW);
struct FlashingLED sounderLED = newFlashingLED(SOUNDER_LED, LOW, 250, 250);
struct DebouncedSwitch keySwitch = newDebouncedSwitch(KEY_SWITCH, 200, LOW);
struct DebouncedButton resetButton = newDebouncedButton(RESET_BUTTON, LOW, 200);
struct DebouncedButton activateButton = newDebouncedButton(ACTIVATE_BUTTON, LOW, 200);
struct LED callPointLED = newLED(CALL_POINT_LED, LOW);
struct DebouncedSwitch callPointSwitch = newDebouncedSwitch(CALL_POINT_SWITCH, 200, HIGH);

bool alarmIsTriggered = LOW;
bool alarmIsCancelled = LOW;
bool previousAlarmTriggered = LOW;

void setup() {
  setupFlashingLED(&triggeredLED);
  setupLED(&notTriggeredLED);
  setupLED(&keyInLED);
  setupFlashingLED(&sounderLED);
  setupDebouncedSwitch(&keySwitch);
  setupDebouncedButton(&resetButton);
  setupDebouncedButton(&activateButton);
  
  setupLED(&callPointLED);
  setupDebouncedSwitch(&callPointSwitch);

  // Audio module
  pinMode(AUDIO_BOARD_IO0, OUTPUT);
  pinMode(AUDIO_BOARD_IO1, OUTPUT);

  digitalWrite(AUDIO_BOARD_IO0, HIGH);    
}

void loop() {

  // Check each of the buttons
  updateDebouncedSwitch(&keySwitch);
  updateDebouncedButton(&resetButton);
  updateDebouncedButton(&activateButton);
  updateDebouncedSwitch(&callPointSwitch);

  // Show whether the key is turned in the switch
  changeLEDState(&keyInLED, keySwitch.state);
  updateLED(&keyInLED);

  // Allow the activate and reset buttons to work
  if (keySwitch.state == HIGH) {
    if ((activateButton.state == HIGH) && (resetButton.state == LOW)) {
      alarmIsTriggered = HIGH;
    } else if ((activateButton.state == LOW) && (resetButton.state == HIGH)) {
      alarmIsTriggered = LOW;
    }
  }

  if (callPointSwitch.state == HIGH) {
    alarmIsTriggered = HIGH;
  }

  // Update the activate and reset LEDs
  changeLEDState(&notTriggeredLED, !alarmIsTriggered);
  updateLED(&notTriggeredLED);

  changeFlashingLEDState(&triggeredLED, alarmIsTriggered);
  updateFlashingLED(&triggeredLED);

  // Update the sounder LEDs
  changeFlashingLEDState(&sounderLED, alarmIsTriggered);
  updateFlashingLED(&sounderLED);

  // Update the call point LED
  changeLEDState(&callPointLED, callPointSwitch.state);
  updateLED(&callPointLED);  

  // Update the audio module
  if ((alarmIsTriggered == HIGH) && (previousAlarmTriggered == LOW)) {
    alarmTriggered(&audioModule);
  } else if ((alarmIsTriggered == LOW) && (previousAlarmTriggered == HIGH)) {
    alarmCancelled(&audioModule);
  }

  updateAudioModule(&audioModule);

  previousAlarmTriggered = alarmIsTriggered;
}
