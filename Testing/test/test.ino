/*
 *MECH307: Mechtronics 
 *Use a shift register to interface with a seven segment display
 *Note that you will nee to modify the code based on your own hardware connections
 * 
 */

// define the LED digit patterns, from 0 - 9
// 1 = LED on, 0 = LED off, in this order:
//                74HC595 pin     Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7 
//                Mapping to      a,b,c,d,e,f,g of Seven-Segment LED
byte seven_seg_digits[10] = { B11111100,  // = 0
                              B01100000,  // = 1
                              B11011010,  // = 2
                              B11110010,  // = 3
                              B01100110,  // = 4
                              B10110110,  // = 5
                              B10111110,  // = 6
                              B11100000,  // = 7
                              B11111110,  // = 8
                              B11100110   // = 9
                             };
 
// connect to the ST_CP of 74HC595 (pin 5,latch pin)
int latchPin = 10;
// connect to the SH_CP of 74HC595 (pin 7, clock pin)
int clockPin = 12;
// connect to the DS of 74HC595 (pin 9)
int dataPin = 9;
const int buttonPin = 13;
int buffer = 0;
int digit = 0;
 
void setup() {
  // Set latchPin, clockPin, dataPin as output
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  Serial.begin(115200);
}
 
// display a number on the digital segment display
void sevenSegWrite(byte digit) {
  // set the latchPin to low potential, before sending data
  digitalWrite(latchPin, LOW);
     
  // the original data (bit pattern)
  // you can learn the syntax for "shiftOut" in the following link
  //https://www.arduino.cc/reference/en/language/functions/advanced-io/shiftout/
  shiftOut(dataPin, clockPin, LSBFIRST, seven_seg_digits[digit]);  
 
  // set the latchPin to high potential, after sending data
  digitalWrite(latchPin, HIGH);
}
 
void loop() {       
  if (digitalRead(buttonPin) == 1) {
	if (buffer == 0) {
		digit += 1;
	}
	buffer = 1;
  }
  else {
	buffer = 0;
  }
  if (digit > 10) {
	digit = 1;
  }
  Serial.print(digit);
  Serial.print(", ");
  Serial.println(digitalRead(buttonPin));
  sevenSegWrite(digit - 1); 
  delay(100);
}
