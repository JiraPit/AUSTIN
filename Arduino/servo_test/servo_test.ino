#include <Servo.h>

Servo myservo1;
int pos = 0; 

void setup() {
  myservo1.attach(D8,500,2400);
  myservo1.write(120);
}

void loop() {
//  myservo1.write(100);
//  
//  delay(3000);
//
//  myservo1.write(150);
//  delay(3000);
}
