const int en = 10;
const int mc1 = 20;
const int mc2 = 21;

void setup() {
  Serial.begin(9600);
  pinMode(en, OUTPUT);
  pinMode(mc1, OUTPUT);
  pinMode(mc2, OUTPUT);
}

void forward(int rate) {
  digitalWrite(en, 0);
  digitalWrite(mc1, 1);
  digitalWrite(mc2, 0);
  analogWrite(en, rate);
}

void backward(int rate) {
  digitalWrite(en, 0);
  digitalWrite(mc1, 0);
  digitalWrite(mc2, 1);
  analogWrite(en, rate);
}

void stop() {
  digitalWrite(en, 0);
  digitalWrite(mc1, 0);
  digitalWrite(mc2, 0);
  digitalWrite(en, 1);
}

void loop() {
  forward(255);
  delay(1000);
  backward(255);
  delay(1000);
}
