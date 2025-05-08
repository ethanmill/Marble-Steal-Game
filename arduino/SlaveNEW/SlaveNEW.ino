#include <Wire.h>
#include <LiquidCrystal.h>
// Characters 
LiquidCrystal lcd(7,8,9,10,11,12);
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

int P2Items[] = {0,0,0,0,0,0,0,0};
int P2ItemsDisp[] = {0,0,0,0,0,0,0,0};
int P2prevmenu = 100;
int P2menu = 0;

int cursorPos = 0;

void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.clear();
  lcd.createChar(1,MagGlass);
  lcd.createChar(2,PadLock);
  lcd.createChar(3,Spy);
  lcd.createChar(4,Skip);
  lcd.createChar(5,Gamble);
  lcd.createChar(6,Selector);            
  lcd.createChar(7,Arrow);
  lcd.createChar(8,Back);
  Wire.begin(4);
  Wire.onReceive(commandIngest);
  dispItemMenu();
}

bool matchArray(int a1[], int a2[]) {
  bool match = true;
  for(int i=0; i<8; i++) {
    if (a1[i] != a2[i]) {
      match == false;
      break;
    }
  }
  return match;
}

void loop() {
  delay(100);
  if (P2prevmenu != P2menu) {
    if (P2menu == -1) {
      delay(4000);
    }
    P2updateMenu();
    P2prevmenu = P2menu;
  }
}

void printP2Items() {
  Serial.print("P2Items: ");
  for (int i=0; i<P2countItems(); i++) {
    Serial.print(P2Items[i]);
    Serial.print(",");
  }
  Serial.println();
}

void P2updateMenu() {
  if (P2menu == 0) {
    dispWaitMenu();
  }
  else if (P2menu == 1) {
    dispReadyMenu();
  }
  else if (P2menu == 2) {
    dispMainMenu();
  }
  else if (P2menu == 3) {
    dispGiveMenu();
  }
  else if (P2menu == 4) {
    dispItemMenu();
  }
  updateCursor();
}

void updateCursor() {
  if (P2menu == 2) {
    dispMainMenu();
    if (cursorPos == 0) {
      lcd.setCursor(1,1);
    }
    else if (cursorPos == 1) {
      lcd.setCursor(9,1);
    }
  }
  else if (P2menu == 3) {
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
  else if (P2menu == 4) {
    dispItemMenu();
    if (cursorPos < P2countItems()) {
      lcd.setCursor(cursorPos,1);
    }
    else {
      lcd.setCursor(15,1);
    }
  }
  if (P2menu > 1) {
    lcd.write(byte(7));
  }
}

void commandIngest() {
  // 0-10 -> Set menu (04 sets to menu 4)
  // 10-30 -> Set cursor (23 will set cursorPos to 13)
  // 30-100 -> Set show marble secret (% 5, 37 means marble 2 is blue) 0 - white, 1 - red, 2 - blue
  // 100-200 -> Update items (115 will set item position 1 to item ID 5)
  int rec = 0;
  while (Wire.available()) {
    rec = Wire.read();
    Serial.println(rec);
  }

  if (rec < 10) { //Set menu
    P2menu = rec;
    P2updateMenu();
  }
  else if (rec < 30) { //Set cursor pos
    cursorPos = rec - 10;
    updateCursor();
  }
  else if (rec < 100) { //Show marble in queue
    int marbleShow = rec - 30;
    int marbleColor = marbleShow % 5;
    int marblePos = ((marbleShow - marbleColor) / 5);
    if (rec != 30) {
      if (marbleColor <= 2) { //Filter out garbage
        P2menu = -1;
        dispMarbleInfo(marblePos, marbleColor);
      }
    }
    else {
      P2menu = 2;
      P2updateMenu();
    }
  }
  else if (rec < 200) { //Update items
    int cmd = rec % 100;
    int itemID = cmd % 10;
    int itemPos = (cmd - itemID)/10;
    for (int i=itemPos; i<8; i++) {
      P2Items[i] = 0;
    }
    if (itemID > 0 && itemID < 10) {
      P2Items[itemPos] = itemID;
    }
  }
}

int P2countItems() {
  int i = 0;
  while (P2Items[i] != 0) {
    i++;
  }
  return i;
}

// --------- Menu Displays --------

void dispInitMenu() {
  Serial.println("Init menu");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Initializing...");
  lcd.setCursor(0,1);
  lcd.print("Waiting for pi");
}

void dispWaitMenu() {
  Serial.println("Wait menu");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Waiting for foe");
}

void dispReadyMenu() {
  Serial.println("Ready menu");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Ready?");
}

void dispMainMenu() {
  Serial.println("Main menu");
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
  Serial.println("Give menu");
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
  printP2Items();
  lcd.clear();
  lcd.setCursor(15,0);
  lcd.write(byte(8));
  for (int i=0; i<P2countItems(); i++) {
    if (P2Items[i] == 0) {
      break;
    }
    else {
      lcd.setCursor(i,0);
      if (P2Items[i] < 3) {
        lcd.write(byte(P2Items[i]));
      }
      else if(P2Items[i] == 3) {
        lcd.write("2");
      }
      else if (P2Items[i] < 6) {
        lcd.write(byte(P2Items[i]));
      }
      else if (P2Items[i] == 6) {
        lcd.write(byte(3));
      }
      else if (P2Items[i] == 7) {
        lcd.write("R");
      }
    }
  }
}

void dispMarbleInfo(int marblePos, int marbleColor) { //0-white, 1-red, 2-blue
  Serial.println("marble menu");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.write("Marble #");
  lcd.setCursor(8,0);
  lcd.write(char(marblePos+48));
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
  P2menu = 2;
}
