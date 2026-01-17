/*********************************************************************
 * LED
 *********************************************************************/

struct LED {
  pin_size_t pinNumber;  // Pin to which the LED is attached
  bool state;            // State of the LED
};

struct LED newLED(pin_size_t pinNumber, bool initial_state) {
  struct LED led = {
    pinNumber,
    initial_state
  };
  return led;
}

void setupLED(struct LED *led) {
  pinMode(led->pinNumber, OUTPUT);
}

void changeLEDState(struct LED *led, bool state) {
  led->state = state;
}

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

void setupFlashingLED(struct FlashingLED *led) {
  pinMode(led->pinNumber, OUTPUT);
}

void changeFlashingLEDState(struct FlashingLED *led, bool state) {
  if (state == LOW && led->state == HIGH) {
    led->isHigh = LOW;
    led->lastChange = millis();
  }

  led->state = state;
}

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
 * Two-tone buzzer
 *********************************************************************/

struct TwoToneBuzzer {
  pin_size_t pinNumber;   // Pin to which the buzzer is attached  
  int frequency1;         // Frequency 1
  int buzzerFreq1Time;    // Time on frequency 1 in milliseconds
  int frequency2;         // Frequency 2
  int buzzerFreq2Time;    // Time on frequency 2 in milliseconds
  bool state;             // State of the buzzer (on or off)

  // Internal
  unsigned long lastStateChange;
  bool usingFreq1;
  bool buzzerOn;
};

struct TwoToneBuzzer newTwoToneBuzzer(pin_size_t pinNumber, int frequency1, int buzzerFreq1Time,
  int frequency2, int buzzerFreq2Time, bool initial_state) {

    struct TwoToneBuzzer buzzer = {
      pinNumber,
      frequency1,
      buzzerFreq1Time,
      frequency2,
      buzzerFreq2Time,
      initial_state,
      millis(),
      LOW,
      LOW,
    };
    return buzzer;
}

void setupBuzzer(struct TwoToneBuzzer *buzzer) {
  pinMode(buzzer->pinNumber, OUTPUT);
}

void changeBuzzerState(struct TwoToneBuzzer *buzzer, bool state) {
  if ((state == LOW) && (buzzer->state == HIGH)) {
    buzzer->usingFreq1 = LOW;
    buzzer->lastStateChange = millis();
    noTone(buzzer->pinNumber);
  }

  buzzer->state = state;
}

void updateBuzzer(struct TwoToneBuzzer *buzzer) {
  if (buzzer->state == LOW) {
    return;
  }

  unsigned long currentTime = millis();

  if ((buzzer->usingFreq1 == HIGH) && (currentTime > buzzer->lastStateChange + buzzer->buzzerFreq1Time)) {
    buzzer->usingFreq1 = LOW;
    buzzer->lastStateChange = currentTime;
    tone(buzzer->pinNumber, buzzer->frequency2, buzzer->buzzerFreq2Time);
  } else if ((buzzer->usingFreq1 == LOW) && (currentTime > buzzer->lastStateChange + buzzer->buzzerFreq2Time)) {
    buzzer->usingFreq1 = HIGH;
    buzzer->lastStateChange = currentTime;
    tone(buzzer->pinNumber, buzzer->frequency1, buzzer->buzzerFreq1Time);
  }
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

void setupDebouncedButton(struct DebouncedButton *button) {
  if (button->hasPullUpResistor == HIGH) {
    pinMode(button->pinNumber, INPUT_PULLUP);
  } else {
    pinMode(button->pinNumber, INPUT);
  }
}

bool hasBeenPressed(struct DebouncedButton *button) {

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
 * Debounced toggle button
 *********************************************************************/

struct DebouncedToggleButton {
  pin_size_t pinNumber;         // Pin to which the button is attached
  bool hasPullUpResistor;       // Does the pin have an internal pull-up resistor?
  int debounceDelay;            // Debounce delay in milliseconds

  // Internal
  unsigned long lastPressTime;
  bool state;
};

struct DebouncedToggleButton newDebouncedToggleButton(pin_size_t pinNumber, bool hasPullUpResistor, int debounceDelay) {
  struct DebouncedToggleButton button = {
    pinNumber,
    hasPullUpResistor,
    debounceDelay,
    millis(),
    LOW
  };
  return button;
}

void setupDebouncedToggleButton(struct DebouncedToggleButton *button) {
  if (button->hasPullUpResistor == HIGH) {
    pinMode(button->pinNumber, INPUT_PULLUP);
  } else {
    pinMode(button->pinNumber, INPUT);
  }
}

void updateDebouncedToggleButton(struct DebouncedToggleButton *button) {
  
  // Get the current state of the button
  bool currentReading;
  if (button->hasPullUpResistor) {
    currentReading = !digitalRead(button->pinNumber);
  }  else {
    currentReading = digitalRead(button->pinNumber);
  }

  // Current time in milliseconds
  unsigned long currentTime = millis();  

  if ((currentReading == HIGH) && (currentTime > (button->lastPressTime + button->debounceDelay))) {
    button->state = !button->state;
    button->lastPressTime = currentTime;
  }
}

/*********************************************************************
 * Measure debounce time required
 *********************************************************************/

unsigned long firstHighTime = 0;
unsigned long lastHighTime = 1000;
bool measuring = LOW;

void measureDebounceTime() {

  // Measure the switch debounce time required
  unsigned long currentTime = millis();
  if (digitalRead(6) && (measuring == LOW)) {
    measuring = HIGH;
    firstHighTime = currentTime;
    lastHighTime = currentTime;
    Serial.println("Timing started");
  }

  if (digitalRead(6) && (measuring == HIGH)) {
    lastHighTime = currentTime;
  }

  if (!digitalRead(6) && (measuring == HIGH) && (currentTime > lastHighTime + 1000)) {
    measuring = LOW;
    char buffer[100];
    sprintf(buffer, "%lu milliseconds\n", lastHighTime - firstHighTime);
    Serial.write(buffer);
  }
}

/*********************************************************************
 * Define components
 *********************************************************************/

struct LED yellowLED = newLED(2, HIGH);
struct FlashingLED greenLED = newFlashingLED(3, HIGH, 500, 800);
struct TwoToneBuzzer buzzer = newTwoToneBuzzer(5, 500, 500, 800, 500, LOW);
//struct DebouncedButton button1 = newDebouncedButton(6, LOW, 200);
struct DebouncedToggleButton button2 = newDebouncedToggleButton(6, LOW, 200);

void setup() {
  setupLED(&yellowLED);
  setupFlashingLED(&greenLED);
  setupBuzzer(&buzzer);
  //setupDebouncedButton(&button1);
  setupDebouncedToggleButton(&button2);

  Serial.begin(9600);
  Serial.println("Measuring switch debounce time\n");
}

void loop() {

  // measureDebounceTime();

  // If using the button as a simple debounced button
  // bool pressed = hasBeenPressed(&button1);
  // changeLEDState(&yellowLED, pressed);
  // if (pressed) {
  //   Serial.write("Button pressed\n");
  // }

  // If using the button as a debounced toggle button
  updateDebouncedToggleButton(&button2);
  changeFlashingLEDState(&greenLED, button2.state); 
  changeBuzzerState(&buzzer, button2.state);

  // Update the output components
  updateLED(&yellowLED);
  updateFlashingLED(&greenLED);
  updateBuzzer(&buzzer);
}
