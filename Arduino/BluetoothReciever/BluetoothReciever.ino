#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial Bluetooth(D7, D8);
const int BufLen = 30;

void setup() {
  Bluetooth.begin(9600);
  Serial.begin(9600);
}

void loop() {
  if (Bluetooth.available() > 0) {
    char Buf[BufLen]; 
    String rec = Bluetooth.readStringUntil('$');
    rec = "#" + rec;
    rec.toCharArray(Buf,BufLen);
    Serial.write(Buf,BufLen);
  }
}
