void setup() {
  Serial.begin(115200);
  pinMode(3, OUTPUT); analogWrite (3, 255);
  pinMode(5, OUTPUT); digitalWrite(5, 0);
  pinMode(6, OUTPUT); digitalWrite(6, 0);
  pinMode(7, OUTPUT); digitalWrite(7, 0);
  pinMode(8, OUTPUT); digitalWrite(8, 0);
  pinMode(9, OUTPUT); analogWrite (9, 255);
}


int spd=0; 
int Ldir=0;
int Rdir=0;
void loop() {
  if (Serial.available()) {
    if (Serial.read() == 101) {
      spd = Serial.read();
      Ldir = Serial.read();
      Rdir = Serial.read();
      set_L(spd, Ldir);
      set_R(spd, Rdir);
    }
  }
  delay(10);
}







void set_L (int spd, int dir) {
  if (dir == 2) { //LS
    analogWrite(3,255);
    digitalWrite(5,0);
    digitalWrite(6,0);
  }
  if (dir == 1) { //LF
    analogWrite(3,spd);
    digitalWrite(5,1);
    digitalWrite(6,0);
  }
  if (dir == 0) { //LB
    analogWrite(3,spd);
    digitalWrite(5,0);
    digitalWrite(6,1);
  }
}

void set_R (int spd, int dir) {
  if (dir == 2) { //RS
    digitalWrite(7,0);
    digitalWrite(8,0);
    analogWrite (9,255);
  }
  if (dir == 1) { //RF
    digitalWrite(7,0);
    digitalWrite(8,1);
    analogWrite (9,spd);
  }
  if (dir == 0) { //RB
    digitalWrite(7,1);
    digitalWrite(8,0);
    analogWrite (9,spd);
  }
}

void test_drive() {
  
  for(int i=0; i<255; i++)
  { // L F
    analogWrite(3,i);
    digitalWrite(5,1);
    digitalWrite(6,0);
    digitalWrite(7,0);
    digitalWrite(8,0);
    analogWrite (9,i);
    delay(5);
  } 
  for(int i=0; i<255; i++)
  { // L B
    analogWrite(3,i);
    digitalWrite(5,0);
    digitalWrite(6,1);
    digitalWrite(7,0);
    digitalWrite(8,0);
    analogWrite (9,i);
    delay(5);
  }
  for(int i=0; i<255; i++)
  { // R F
    analogWrite(3,i);
    digitalWrite(5,0);
    digitalWrite(6,0);
    digitalWrite(7,0);
    digitalWrite(8,1);
    analogWrite (9,i);
    delay(5);
  }
  for(int i=0; i<255; i++)
  { // R B
    analogWrite(3,i);
    digitalWrite(5,0);
    digitalWrite(6,0);
    digitalWrite(7,1);
    digitalWrite(8,0);
    analogWrite (9,i);
    delay(5);
  }
}
