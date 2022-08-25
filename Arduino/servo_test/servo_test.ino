#include <Servo.h>

Servo myservo1;
int pos1 = 140;
int pos2 = 0;
int from_pos,to_pos = 0;
void setup() {
  Serial.begin(115200);
  myservo1.attach(D5, 500, 2400);
}

void loop() {
  from_pos = pos1;
  to_pos = pos2;
  if (from_pos < to_pos) {
    for (int pos = from_pos; pos <= to_pos; pos += 1) {
      myservo1.write(pos);
      delay(15);
    }
  } else if (to_pos < from_pos) {
    for (int pos = from_pos; pos >= to_pos; pos -= 1) {
      myservo1.write(pos);
      delay(15);
    }
  }
  Serial.println(pos2);


  from_pos = pos2;
  to_pos = pos1;
  if (from_pos < to_pos) {
    for (int pos = from_pos; pos <= to_pos; pos += 1) {
      myservo1.write(pos);
      delay(25);
    }
  } else if (to_pos < from_pos) {
    for (int pos = from_pos; pos >= to_pos; pos -= 1) {
      myservo1.write(pos);
      delay(25);
    }
  }
  Serial.println(pos1);
}
