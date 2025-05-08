#include <Servo.h>

Servo servo;

const int servoPin = 12;
int pos = 0;

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);
}

void loop() {
  delay(1000);
  servo.write(255);
  delay(1000);
  servo.write(0);
  delay(1000);
  servo.write(200);
}
