#include <LiquidCrystal.h>

const int rs = 2, en = 4, d4 = 5, d5 = 7, d6 = 3, d7 = 8;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  lcd.begin(16,2);
  lcd.clear();
  Serial.begin(9600);
}

void loop() {
  sendCommand("P1Ready");
  delay(2000);
  sendCommand("P2Ready");
  delay(2000);
  sendCommand("useItem");
  delay(2000);
}

void sendCommand(String cmdarg) {
  Serial.println(cmdarg);
  lcd.setCursor(0,0);
  lcd.print("Sent: "+cmdarg);
}
