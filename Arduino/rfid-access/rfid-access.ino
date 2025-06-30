#include <SPI.h>
#include <MFRC522.h>

#define RED_LED_PIN 4
#define GREEN_LED_PIN 2
#define BUZZER_PIN 3

// RC522 module pins
#define RST_PIN 9
#define SS_PIN 10

String PetersTag = "13131C39";
String ReubensTag = "B3F2B438";
String tagID;

// Create instances
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.begin(9600); // Initialize serial communications with the PC
  SPI.begin();        // SPI bus
  mfrc522.PCD_Init(); // MFRC522

  Serial.println("Starting card reader ...");
  showAccess(false);
}

void loop() {
  // digitalWrite(redLedPin, HIGH);
  // tone(buzzer, 1000);

  while(getID()) {
    if ((tagID == PetersTag) || (tagID == ReubensTag)) {
      Serial.println("Access granted");
      showAccess(true);
      delay(1000);
    } else {
      Serial.println("Access denied");
    }    
  }

  showAccess(false);
}

boolean getID() {
  // Getting ready for Reading PICCs
  if (!mfrc522.PICC_IsNewCardPresent()) {  // If a new PICC placed to RFID reader continue
    return false;
  }
  if (!mfrc522.PICC_ReadCardSerial()) {  // Since a PICC placed get Serial and continue
    return false;
  }
  tagID = "";
  for (uint8_t i = 0; i < 4; i++) {  // The MIFARE PICCs that we use have 4 byte UID
    tagID.concat(String(mfrc522.uid.uidByte[i], HEX));  // Adds the 4 bytes in a single String variable
  }
  tagID.toUpperCase();
  Serial.println(tagID);
  mfrc522.PICC_HaltA();  // Stop reading
  return true;
}

void showAccess(bool allowAccess) {
  if (allowAccess) {
    digitalWrite(RED_LED_PIN, LOW);
    digitalWrite(GREEN_LED_PIN, HIGH);
    tone(BUZZER_PIN, 1200, 500);
  } else {
    digitalWrite(RED_LED_PIN, HIGH);
    digitalWrite(GREEN_LED_PIN, LOW);       
  }
}
