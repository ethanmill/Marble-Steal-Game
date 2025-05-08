#include <LiquidCrystal.h>

bool stable = false;

const int out = 12, s3 = 11;
const int rs = 2, en = 4, d4 = 5, d5 = 7, d6 = 3, d7 = 8;
const int scanTime = 5;
const int confirmThreshold = 100/scanTime;

String displayText;
String detectedColor;

int redFreq = 0;
int blueFreq = 0;

int redColor= 0;
int blueColor = 0;

int confirms = 0;

const int maxBlue = 1350;
const int minBlue = 1250;

const int maxRed = 1530;
const int minRed = 1400;

LiquidCrystal lcd(rs,en,d4,d5,d6,d7);

void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.clear();
  lcd.print("hello");
  delay(2000);

  pinMode(out, INPUT);
  pinMode(s3, OUTPUT);

}

//!!! -------------------------------------------------- !!!
//
//To ground: gnd, s1, s2, 
//
//To 5v: Vcc, 
//
//Scale S0 S1
//0%    0  0
//2%    0  1
//20%   1  0
//100%  1  1
//
//!!! -------------------------------------------------- !!!

void loop() {
  digitalWrite(s3,LOW); //read red

  Serial.println(digitalRead(out));
  redFreq = pulseIn(out, LOW);
  delay(scanTime);
  redColor = map(redFreq, minRed, maxRed, 100, 0);

  digitalWrite(s3,HIGH); //read blue

  blueFreq = pulseIn(out, LOW);
  delay(scanTime);
  blueColor = map(blueFreq, minBlue, maxBlue, 100, 0);

  if (redColor > 100 && blueColor > 100) {
    if (detectedColor == "white") {
      confirms += 1;
    }
    else {
      confirms = 0;
    }
    detectedColor = "white";
  }
  else if (redColor > 90) {
    if (detectedColor == "red") {
      confirms += 1;
    }
    else {
      confirms = 0;
    }
    detectedColor = "red";
  }
  else if (blueColor > 90) {
    if (detectedColor == "blue") {
      confirms += 1;
    }
    else {
      confirms = 0;
    }
    detectedColor = "blue";
  }
  else {
    detectedColor = "none";
    confirms = 0;
  }

  if (confirms>=confirmThreshold) {
    stable = true;
    confirms = confirmThreshold;
  }
  else {
    stable = false;
  }

  //displayText = "Red: "+String(redColor)+", blue: "+String(blueColor)+", Color is "+detectedColor;
  displayText = "Red: "+String(redFreq)+", blue: "+String(blueFreq);
  Serial.println(displayText);
  //Serial.println(detectedColor+", "+String(stable));
  lcd.clear();
  lcd.print(detectedColor+", "+String(stable));
}
