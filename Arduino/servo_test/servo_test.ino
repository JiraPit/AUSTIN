#include <Servo.h>

Servo myservo1;

void setup() {
  myservo1.attach(D5,500,2400);
  myservo1.write(10);
}

void loop() {
  myservo1.write(60);
  
  delay(1000);

  myservo1.write(120);
  delay(1000);
}
