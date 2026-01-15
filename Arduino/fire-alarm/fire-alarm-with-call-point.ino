#define CALL_POINT_LED D1
#define CALL_POINT_SWITCH D2
#define LED_NORMAL D8
#define LED_TRIGGERED D7
#define LED_KEY_IN D6
#define SWITCH_ACTIVATE D4
#define SWITCH_RESET D3
#define SWITCH_KEY D0
#define BUZZER D5

struct DebouncedButton {
  unsigned long lastDebounceTime = millis();
  bool previousState;
  bool currentState;
  unsigned long debounceDelay;
};

void debounceSwitch(unsigned long currentTime, bool currentReading, struct DebouncedButton *button) {
  if (currentReading != button->previousState) {
    button->lastDebounceTime = currentTime;
  }
  if ((currentTime > button->lastDebounceTime + button->debounceDelay) && 
    (currentReading != button->currentState)) {
    button->currentState = currentReading;
  }
  button->previousState = currentReading;
}

struct DebouncedButton manualActivation;     // Manual activation switch
struct DebouncedButton callPointActivation;  // Call point switch
struct DebouncedButton manualReset;          // Manual reset
struct DebouncedButton keyPresent;           // Override key present

bool alarmTriggered = LOW;

struct TwoToneBuzzer {
  int time;
  int frequency1;
  int frequency2;
  unsigned long lastStateChange = millis();
  bool state = LOW;
  bool buzzerOn = LOW;
};

struct TwoToneBuzzer buzzer = {
  500,
  500,
  800,
  millis(),
  LOW,
  LOW
};

void setup() {
  pinMode(CALL_POINT_LED, OUTPUT);
  pinMode(CALL_POINT_SWITCH, INPUT);
  pinMode(LED_NORMAL, OUTPUT);
  pinMode(LED_TRIGGERED, OUTPUT);
  pinMode(LED_KEY_IN, OUTPUT);
  pinMode(SWITCH_ACTIVATE, INPUT_PULLUP);
  pinMode(SWITCH_RESET, INPUT_PULLUP);
  pinMode(SWITCH_KEY, INPUT);
  pinMode(BUZZER, OUTPUT);
}

// The call point switch and activation state are as follows:
//
//   Call point switch | Call point state | Activation state
//   ------------------|------------------|------------------
//   Unpressed         | LOW              | On
//   Pressed           | HIGH             | Off
void checkCallPointActivation(unsigned long currentTime) {
  debounceSwitch(currentTime, !digitalRead(CALL_POINT_SWITCH), &callPointActivation);
}

// Has the alarm been manually activated?
void checkManualActivation(unsigned long currentTime) {
  debounceSwitch(currentTime, !digitalRead(SWITCH_ACTIVATE), &manualActivation);
}

// Has the alarm been manually reset?
void checkManualReset(unsigned long currentTime) {
  debounceSwitch(currentTime, !digitalRead(SWITCH_RESET), &manualReset);
}

void checkKeyPresent(unsigned long currentTime) {
  debounceSwitch(currentTime, digitalRead(SWITCH_KEY), &keyPresent);
}

void updateBuzzer(unsigned long currentTime, struct TwoToneBuzzer *buzzer) {
  if (buzzer->buzzerOn == LOW) {
    return;
  }

  if (currentTime > buzzer->lastStateChange + buzzer->time) {
    buzzer->state = !buzzer->state;
    buzzer->lastStateChange = currentTime;
    if (buzzer->state == HIGH) {
      tone(BUZZER, buzzer->frequency1, buzzer->time);
    } else {
      tone(BUZZER, buzzer->frequency2, buzzer->time);
    }
  }
}

void loop() {

  // Current time in milliseconds
  unsigned long currentTime = millis();

  checkCallPointActivation(currentTime);
  checkManualActivation(currentTime);
  checkManualReset(currentTime);
  checkKeyPresent(currentTime);

  // Light up the LED in the call point if required
  digitalWrite(CALL_POINT_LED, callPointActivation.currentState);

  digitalWrite(LED_KEY_IN, keyPresent.currentState);

  if (keyPresent.currentState == HIGH) {
    if ((manualActivation.currentState == HIGH) && (manualReset.currentState == LOW)) {
      alarmTriggered = HIGH;
    } else if ((manualActivation.currentState == LOW) && (manualReset.currentState == HIGH)) {
      alarmTriggered = LOW;
    }
  }

  if (callPointActivation.currentState == HIGH) {
    alarmTriggered = HIGH;
  }

  if (alarmTriggered == HIGH) {
    buzzer.buzzerOn = HIGH;
  } else {
    buzzer.buzzerOn = LOW;
    buzzer.state = LOW;
  }

  digitalWrite(LED_TRIGGERED, alarmTriggered);
  digitalWrite(LED_NORMAL, !alarmTriggered);

  updateBuzzer(currentTime, &buzzer);
}
