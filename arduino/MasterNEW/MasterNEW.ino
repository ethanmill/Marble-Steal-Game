#include <LiquidCrystal.h>
#include <Wire.h>
// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to

LiquidCrystal lcd(7,8,9,10,11,12);

// All the pixel art
byte MagGlass[] = {
  B01110,B10101,B10011,B10001,B01110,B00100,B01110,B01110
};
byte Double[] = {
  B00000,B00110,B01001,B00001,B10010,B00100,B01000,B01111
};
byte PadLock[] = {
  B01110,B10001,B10001,B11111,B11011,B11011,B11111,B01110
};
byte Arrow[] ={
  B00000,B00100,B01110,B11111,B00100,B00100,B00100,B00100
};
byte Selector[] ={
  	B00000,B00000,B01110,B01110,B01110,B00000,B00000,B00000
};
byte Back[] = {
  B10001,B01010,B00100,B01010,B10001,B00000,B00000,B00000
};
byte Skip[] = {
  B00000,B00000,B01110,B11001,B10101,B10011,B01110,B00000
};
byte Gamble[] = {
  B00000,B01110,B10001,B11001,B11101,B11111,B01110,B00000
};
byte Spy[] = {
  B00000,B01101,B10010,B10101,B10001,B01110,B01000,B11100
};
byte Recycle[] = {
  B01110,B10010,B10111,B00010,B01000,B11101,B01001,B00110
};

const int P1_L = 5;
const int P1_M = 4;
const int P1_R = 3;
int P1_Buttons[] = {0,0,0};

const int P2_L = 14;
const int P2_M = 15;
const int P2_R = 16;
int P2_Buttons[] = {0,0,0};

bool P1latch = false;
bool P2latch = false;
bool swap = true;

int cursorPos = 0;
int P2cursorPos = 0;
int maxCursorPos = 15;

int P1Items[] = {0,0,0,0,0,0,0,0};
int P2Items[] = {0,0,0,0,0,0,0,0};

int whosTurn = 1; //0 is P1 1 is P2

int P1prevmenu = 100;
int P1menu = 2;
int P2prevmenu = 100;
int P2menu = 0;
// 0 - Waiting
// 1 - Ready menu 
// 2 - Main menu 
// 3 - Give menu
// 4 - Item menu

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.clear();
  lcd.createChar(1,MagGlass);
  lcd.createChar(2,PadLock);
  lcd.createChar(3,Spy);
  lcd.createChar(4,Skip);
  lcd.createChar(5,Gamble);
  lcd.createChar(6,Selector);            
  lcd.createChar(7,Arrow);
  lcd.createChar(8,Back);
  pinMode(P1_R,INPUT);
  pinMode(P1_M,INPUT);
  pinMode(P1_L,INPUT);
  pinMode(P2_R,INPUT);
  pinMode(P2_M,INPUT);
  pinMode(P2_L,INPUT);
  Wire.begin();
  dispInitMenu();
}

void loop() {
  delay(70);
  readButtons();
  receiveSerial();
  //printButtons();
  if (swap) {
    if (whosTurn == 0) {
      whosTurn = 1;
      P2menu = 2;
      P1menu = 0;
    }
    else {
      whosTurn = 0;
      P2menu = 0;
      P1menu = 2;
    }
    swap = false;
  }

  if (P1prevmenu != P1menu) {
    P1updateMenu();
    P1prevmenu = P1menu;
  }
  if (P2prevmenu != P2menu) {
    P2updateMenu();
    P2prevmenu = P2menu;
  }

  if (whosTurn == 0 || P1menu == 1) {// Is it P1s turn?
    if (P1latch == false) {
      if (P1_Buttons[0] == 1) {//P1 Left button
        cursorPos -= 1;
        updateCursor();
        P1latch = true;
      }
      if (P1_Buttons[1] == 1) {//P1 Middle button
        select();
        P1latch = true;
      }
      if (P1_Buttons[2] == 1) {//P1 Right button
        cursorPos += 1;
        updateCursor();
        P1latch = true;
      }
    }
    else {
      if (P1_Buttons[0] == 0 && P1_Buttons[1] == 0 && P1_Buttons[2] == 0) {
        P1latch = false;
      }
    }
  }
  if (whosTurn == 1 || P2menu == 1) { //Begin P2 turn
    if (P2latch == false) {
      if (P2_Buttons[0] == 1) {//P2 Left button
        cursorPos -= 1;
        updateCursor();
        P2latch = true;
      }
      if (P2_Buttons[1] == 1) {//P2 Middle button
        select();
        P2latch = true;
      }
      if (P2_Buttons[2] == 1) {//P2 Right button
        cursorPos += 1;
        updateCursor();
        P2latch = true;
      }
    }
    else {
      if (P2_Buttons[0] == 0 && P2_Buttons[1] == 0 && P2_Buttons[2] == 0) {
        P2latch = false;
      }
    }
  }
}

void wireSend(int send) {
  delay(20);
  Wire.beginTransmission(4);
  Wire.write(send);
  Wire.endTransmission();
}

void select() {
  int menu;
  if (whosTurn == 0) {
    menu = P1menu;
  }
  else {
    menu = P2menu;
  }
  if (menu == 1) {
    if (P1_Buttons[1] == 1) {
      Serial.println("P2Ready");
    }
    else if (P2_Buttons[1] == 1) {
      Serial.println("P1Ready");
    }
  }

  if (menu == 2) {
    if (cursorPos == 0) {
      menu = 3; //Goto give menu
    }
    else if (cursorPos == 1) {
      Serial.println("updateItemsArd");
      menu = 4; //Goto items menu
    }
  }
  else if (menu == 3) {
    if (cursorPos == 0) {
      if (whosTurn == 0) {
        Serial.println("dispense P1");
      }
      else {
        Serial.println("dispense P2");
      }
    }
    else if (cursorPos == 1) {
      Serial.println("dispense B");
    }
    else if (cursorPos == 2) {
      if (whosTurn == 0) {
        Serial.println("dispense P2");
      }
      else {
        Serial.println("dispense P1");
      }
    }
    menu = 2;
  }
  else if (menu == 4) {
    if (whosTurn == 0) {
      if (cursorPos < P1countItems()) {
        Serial.println("useItem P1 "+String(cursorPos));
      }
    }
    else {
      if (cursorPos < P2countItems()) {
        Serial.println("useItem P2 "+String(cursorPos));
      }
    }
    Serial.println("hoverExit");
    menu = 2;
  }
  cursorPos = 0;

  if (whosTurn == 0) {
    P1menu = menu; 
  }
  else {
    P2menu = menu;
  }
}

void updateCursor() {
  if (cursorPos < 0) {
    cursorPos = maxCursorPos;
  }
  else if (cursorPos > maxCursorPos) {
    cursorPos = 0;
  }
  //Serial.print("Updating Cursor: ");
  //Serial.print(cursorPos);
  //Serial.print(", Max Pos: ");
  //Serial.print(cursorPos);
  //Serial.print(", For player: ");
  //Serial.println(whosTurn+1);

  if (whosTurn == 0) { // P1s Turn
    if (P1menu == 1 || P1menu == 0) { // ready menu or waiting
      return; //Do nothing
    }
    if (P1menu == 2) { // main menu
      dispMainMenu();
      if (cursorPos == 0) { // Set cursor under give action
        lcd.setCursor(1,1);
      }
      else if (cursorPos == 1) { // Set cursor under item action
        lcd.setCursor(9,1);
      }
    }
    else if (P1menu == 3) { //Give menu
      dispGiveMenu();
      if (cursorPos == 0) {
        lcd.setCursor(0,1);
      }
      else if (cursorPos == 1) {
        lcd.setCursor(5,1);
      }
      else if (cursorPos == 2) {
        lcd.setCursor(11,1);
      }
      else if (cursorPos == 3) {
        lcd.setCursor(15,1);
      }
    }
    else if (P1menu == 4) { //Item menu
      dispItemMenu();
      if (cursorPos < P1countItems()) {
        Serial.println("hoverItem P1 "+String(cursorPos));
        lcd.setCursor(cursorPos,1);
      }
      else {
        Serial.println("hoverExit");
        lcd.setCursor(15,1);
      }
    }
    lcd.write(byte(7));
  }
  else if (whosTurn == 1) { //Begin P2
    if (P2menu == 1 || P2menu == 0) { // ready menu or waiting
      return; //Do nothing
    }
    wireSend(10+cursorPos);
    if (P2menu == 4) {
      if(cursorPos < P2countItems()) {
        Serial.println("hoverItem P2 "+String(cursorPos));
      }
    }
    else {
        Serial.println("hoverExit");
    }
  }
}

void P2updateItems() {
  for (int i=0; i<8; i++) {
    if (P2Items[i] > 0 && P2Items[i] < 10) {
      wireSend(100+i*10+P2Items[i]);
    }
  }
  if (P2menu == 4) {
    maxCursorPos = P2countItems();
  }
}

void P2updateMenu() {
  P2updateItems();
  if (P2menu == 0) {
    maxCursorPos = 0;
  }
  else if (P2menu == 1) {
    maxCursorPos = 0;
  }
  else if (P2menu == 2) {
    maxCursorPos = 1;
  }
  else if (P2menu == 3) {
    maxCursorPos = 3;
  }
  else if (P2menu == 4) {
    maxCursorPos = P2countItems();
  }
  else if (P2menu == 5) {
    maxCursorPos = 0;
  }
  wireSend(P2menu);
  updateCursor();
}

void P1updateMenu() {
  if (P1menu == 0) {
    dispWaitMenu();
  }
  else if (P1menu == 1) {
    dispReadyMenu();
  }
  else if (P1menu == 2) {
    dispMainMenu();
  }
  else if (P1menu == 3) {
    dispGiveMenu();
  }
  else if (P1menu == 4) {
    dispItemMenu();
  }
  updateCursor();
}

int P1countItems() {
  int i = 0;
  while (P1Items[i] != 0) {
    i++;
  }
  return i;
}

int P2countItems() {
  int i = 0;
  while (P2Items[i] != 0) {
    i++;
  }
  return i;
}

void printP1Items() {
  Serial.print("P1Items: ");
  for (int i=0; i<P1countItems(); i++) {
    Serial.print(P1Items[i]);
  }
  Serial.println();
}

void printP2Items() {
  Serial.print("P2Items: ");
  for (int i=0; i<P2countItems(); i++) {
    Serial.print(P2Items[i]);
  }
  Serial.println();
}

void printButtons() {
  Serial.print("P1_Buttons: [");
  for (int i=0; i<3; i++) {
    Serial.print(P1_Buttons[i]);
  }
  Serial.print("] P2_Buttons: [");
  for (int i=0; i<3; i++) {
    Serial.print(P2_Buttons[i]);
  }
  Serial.println("]");
}

void readButtons() {
  P1_Buttons[0] = digitalRead(P1_L);
  P1_Buttons[1] = digitalRead(P1_M);
  P1_Buttons[2] = digitalRead(P1_R);
  P2_Buttons[0] = digitalRead(P2_L);
  P2_Buttons[1] = digitalRead(P2_M);
  P2_Buttons[2] = digitalRead(P2_R);
}

void receiveSerial() {
  int player = 0;
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    Serial.print("Arduino: ");
    Serial.println(cmd);
    // ----- Command Examples ----- 
    // updateItems P1 12341234
    // updateMenu P2 wait
    if (cmd.startsWith("updateItems")) {
      cmd.remove(0,12);
      if (cmd.startsWith("P1")) {
        player = 0;
      }
      else {
        player = 1;
      }
      cmd.remove(0,3);
      for (int i=0; i<8; i++) {
        int item = int(cmd[i])-48;//Why can't this cast normally wtf
        if (player == 0) {
          for (int j=0; j<8; j++) {
            P1Items[i] = 0;
          }
          if (item > 0 && item < 10) {
            P1Items[i] = item;
          }
        }
        if (player == 1) {
          for (int j=0; j<8; j++) {
            P2Items[i] = 0;
          }
          if (item > 0 && item < 10) {
            P2Items[i] = item;
          }
        }
      }
      P2updateItems();
      printP1Items();
      printP2Items();
    }
    else if (cmd.startsWith("updateMenu")) {
      cmd.remove(0,11);
      if (cmd.startsWith("P1")) {
        cmd.remove(0,3);
        if (cmd.startsWith("wait")) {
          P1menu = 0;
        }
        else if (cmd.startsWith("ready")) {
          P1menu = 1;
          P2menu = 1;
        }
        else if (cmd.startsWith("main")) {
          P1menu = 2;
        }
        P1updateMenu();
      }
      else {
        cmd.remove(0,3);
        if (cmd.startsWith("wait")) {
          P2menu = 0;
        }
        else if (cmd.startsWith("ready")) {
          P1menu = 1;
          P2menu = 1;
        }
        else if (cmd.startsWith("main")) {
          P2menu = 2;
        }
        P2updateMenu();
      }
    }
    else if (cmd.startsWith("updateTurn")) {
      cmd.remove(0,11);
      if (cmd.startsWith("P1")) {
        whosTurn = 0;
        P1menu = 2;
        P2menu = 0;
      }
      else if (cmd.startsWith("P2")) {
        whosTurn = 1;
        P1menu = 0;
        P2menu = 2;
      }
      P1updateMenu();
      P2updateMenu();
    }
    else if (cmd.startsWith("showMarble")) { //showMarble P1 2 1
      cmd.remove(0,11);
      if (cmd.startsWith("P1")) {
        cmd.remove(0,3);
        int marblePos = int(cmd[0]);
        int marbleColor = int(cmd[2])-48;
        dispMarbleInfo(marblePos, marbleColor);
      }
      else if (cmd.startsWith("P2")) {
        lcd.clear();
        cmd.remove(0,3);
        int marblePos = int(cmd[0])-48;
        int marbleColor = int(cmd[2])-48;
        int marbleSend = marblePos*5+marbleColor;
        wireSend(30+marbleSend);
        delay(4000);
        wireSend(30);
      }
    }
    else if (cmd.startsWith("swapTurns")) {
      swap = true;
    }
  }
}

// --------- Menu Displays --------

void dispInitMenu() {
  maxCursorPos = 0;
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Initializing...");
  lcd.setCursor(0,1);
  lcd.print("Waiting for pi");
}

void dispWaitMenu() {
  maxCursorPos = 0;
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Waiting for foe");
}

void dispReadyMenu() {
  maxCursorPos = 0;
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Ready?");
}

void dispMainMenu() {
  maxCursorPos = 1; // Give, Item
  lcd.clear();
  lcd.setCursor(2,0);
  lcd.print("Give");
  lcd.setCursor(10,0);
  lcd.print("Items");
  lcd.setCursor(9,0);
  lcd.write(byte(6)); 
  lcd.setCursor(1,0);
  lcd.write(byte(6));
}

void dispGiveMenu() {
  maxCursorPos = 3;
  lcd.clear();
  lcd.setCursor(15,0);
  lcd.write(byte(8));
  lcd.setCursor(0,0);
  lcd.write(byte(6));
  lcd.setCursor(1,0);
  lcd.print("Self");
  lcd.setCursor(5,0);
  lcd.write(byte(6));
  lcd.setCursor(6,0);
  lcd.print("Bank");
  lcd.setCursor(11,0);
  lcd.write(byte(6));
  lcd.setCursor(12,0);
  lcd.print("Foe");
}

void dispItemMenu() {
  maxCursorPos = P1countItems();
  lcd.clear();
  lcd.setCursor(15,0);
  lcd.write(byte(8));
  for (int i=0; i<P1countItems(); i++) {
    if (P1Items[i] == 0) {
      break;
    }
    else {
      lcd.setCursor(i,0);
      if (P1Items[i] < 3) {
        lcd.write(byte(P1Items[i]));
      }
      else if(P1Items[i] == 3) {
        lcd.write("2");
      }
      else if (P1Items[i] < 6) {
        lcd.write(byte(P1Items[i]));
      }
      else if (P1Items[i] == 6) {
        lcd.write(byte(3));
      }
      else if (P1Items[i] == 7) {
        lcd.write("R");
      }
    }
  }
}

void dispMarbleInfo(int marblePos, int marbleColor) { //0-white, 1-red, 2-blue
  maxCursorPos = 0;
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.write("Marble #");
  lcd.setCursor(8,0);
  lcd.write(marblePos);
  lcd.setCursor(0,1);
  lcd.write("is");
  lcd.setCursor(3,1);
  if (marbleColor == 0) {
    lcd.write("white");
  }
  else if (marbleColor == 1) {
    lcd.write("red");
  }
  else if (marbleColor == 2) {
    lcd.write("blue");
  }
  else {
    lcd.write(marbleColor);
  }
  delay(4000);
  P1menu = 2;
  P1updateMenu();
}
