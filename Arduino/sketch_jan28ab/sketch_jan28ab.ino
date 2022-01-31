#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial Bluetooth(10,11);

Servo indexServo;
int pos = 0;

void setup(){
  indexServo.attach(9);
  Bluetooth.begin(9600);
  Serial.begin(38400);
}

void loop() {
  if (Bluetooth.available() > 0) {
    int recieve = Bluetooth.read();
    float value = (int)recieve-48;
    value = (value/9)*180;
    Serial.println(value);
    if(abs(pos-value)>1){
      pos = value;
      indexServo.write(pos);
    }
    
  }
}
