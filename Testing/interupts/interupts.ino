LED1 = 13;
LED2 = 3;

void setup() {
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  Timer1.initialize(5000);
  Timer1.attachInterrupt(toggleLED);
}

void loop() {
}

void toggleLED() {
  digitalWrite(LED1, !digitalRead(LED1));
}
