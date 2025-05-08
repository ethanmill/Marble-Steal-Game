#include <LiquidCrystal.h>

const int rs = 2, en = 4, d4 = 5, d5 = 7, d6 = 3, d7 = 8;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

byte PadLock[] = {
  B01110,B10001,B10001,B11111,B11011,B11011,B11111,B01110
};
byte Arrow[] ={
  B00000,B00100,B01110,B11111,B00100,B00100,B00100,B00100
};

void setup() {
  Serial.begin(9600);
  lcd.clear();
  lcd.begin(16,2);
  lcd.createChar(0,PadLock);
  lcd.setCursor(0,0);
  lcd.print("hello nerd");
  delay(2000);
}

void loop() {
  lcd.setCursor(0, 1);
  lcd.write(byte(0));
  delay(1000);
  lcd.createChar(0,Arrow);
  lcd.setCursor(3, 1);
  lcd.write(byte(0));
}
