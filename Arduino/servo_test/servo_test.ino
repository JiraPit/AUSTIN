#include <Servo.h>

Servo myservo;

int pos = 0; 

void setup() {
  myservo.attach(7);
}

void loop() {
  for (pos = 0; pos <= 90; pos += 1) {
    // in steps of 1 degree
    myservo.write(pos);
//    myservo2.write(pos);
    delay(1);                    
  }
  delay(1000);
  for (pos = 90; pos >= 0; pos -= 1) {
    myservo.write(pos);   
//    myservo2.write(pos);
    delay(1);            
  }
  delay(1000);
}
