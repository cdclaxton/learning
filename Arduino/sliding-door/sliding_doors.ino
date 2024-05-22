// Motor
int enable=D2;  // Motor enable
int one_a=D3; // Motor 1A
int one_b=D4; // Motor 1B

int switch_close=D8;  // Red switch
int switch_open=D7; // Green switch

int red_light=D10;  // Red status LED
int green_light=D9; // Green status LED

int end_stop_1=D0; // Door open detector switch
int end_stop_2=D1; // Door closed detector switch

int state = 0;

void setup() {
  pinMode(enable, OUTPUT);
  pinMode(one_a, OUTPUT);
  pinMode(one_b, OUTPUT);

  // LEDs
  pinMode(red_light, OUTPUT);
  pinMode(green_light, OUTPUT);

  pinMode(switch_close, INPUT);
  pinMode(switch_open, INPUT);
  pinMode(end_stop_1, INPUT);
  pinMode(end_stop_2, INPUT);
}

void test() {
  int test_case = 6;

  bool is_closed = digitalRead(end_stop_2) == HIGH;
  bool is_open = digitalRead(end_stop_1) == HIGH;
  bool open_request = digitalRead(switch_open) == HIGH;
  bool close_request = digitalRead(switch_close) == HIGH;
  
  switch (test_case) {
    case 0:
      // Turn on the red LED
      digitalWrite(red_light, HIGH);
      digitalWrite(green_light, LOW);
      break;
    case 1:
      // Turn on the green LED
      digitalWrite(red_light, LOW);
      digitalWrite(green_light, HIGH);        
      break;
    case 2:
      // Fully closed end switch
      digitalWrite(red_light, is_closed);
      digitalWrite(green_light, !is_closed);
      break;
    case 3:
      // Fully open end switch
      digitalWrite(red_light, is_open);
      digitalWrite(green_light, !is_open);
      break;    
    case 4:
      // Open door switch
      digitalWrite(red_light, open_request);
      digitalWrite(green_light, !open_request);
      break;
    case 5:
      // Close door switch
      digitalWrite(red_light, close_request);
      digitalWrite(green_light, !close_request);
      break;
    case 6:
      // Turn motor
      if (close_request) {
        digitalWrite(enable, HIGH);
        digitalWrite(one_a, HIGH);
        digitalWrite(one_b, LOW);
        digitalWrite(red_light, HIGH);
        digitalWrite(green_light, LOW);        
      } else if (open_request) {
        digitalWrite(enable, HIGH);
        digitalWrite(one_a, LOW);
        digitalWrite(one_b, HIGH);    
        digitalWrite(red_light, LOW);
        digitalWrite(green_light, HIGH);              
      } else {
        digitalWrite(enable, LOW);        
        digitalWrite(one_a, LOW);
        digitalWrite(one_b, LOW);
        digitalWrite(red_light, LOW); 
        digitalWrite(green_light, LOW);         
      }
  }

}

void door_closing_or_closed(bool state) {
  digitalWrite(red_light, state);
}

void door_opening_or_open(bool state) {
  digitalWrite(green_light, state);
}

void open_door() {
  digitalWrite(enable, HIGH);
  digitalWrite(one_a, HIGH);
  digitalWrite(one_b, LOW);  
}

void close_door() {
  digitalWrite(enable, HIGH);
  digitalWrite(one_a, LOW);
  digitalWrite(one_b, HIGH);
}

void stop_door() {
  digitalWrite(enable, LOW);
  digitalWrite(one_a, LOW);
  digitalWrite(one_b, LOW);
}

void loop() {

  //test();

  bool is_closed = digitalRead(end_stop_2) == HIGH;
  bool is_open = digitalRead(end_stop_1) == HIGH;

  bool open_request = digitalRead(switch_open) == HIGH;
  bool close_request = digitalRead(switch_close) == HIGH;

  if (!open_request && !close_request) {
    stop_door();
    door_opening_or_open(is_open);
    door_closing_or_closed(is_closed);
  } else if (open_request) {
    door_opening_or_open(true);
    door_closing_or_closed(false);    
    if (is_open) {
      stop_door();
    } else {
      open_door();
    }
  } else if (close_request) {
    door_opening_or_open(false);
    door_closing_or_closed(true);
    if (is_closed) {
      stop_door();
    } else {
      close_door();
    }
  }

}
