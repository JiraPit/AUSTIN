#include <Servo.h>
#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(D5, D6);

const char side = 'r'
const int init_pos = 9;
Servo x_elbowS;
int x_elbow_position = init_pos;
int x_elbow_angles[9] = {110, 120, 130, 140, 150, 160, 170, 180, 180};

void setup() {
  //-Communication
  Bluetooth.begin(9600);
  Serial.begin(74880);
  
  //-Init Servos
  x_elbowS.attach(D8,500,2400);
  
  //-Init position
  x_elbowS.write(x_elbow_angles[x_elbow_position-1]);

void loop() {
  if (Bluetooth.available() > 0) {
    String rec = Bluetooth.readStringUntil('$');
    if (rec[0] == side) {
      x_elbow_position = translate(x_elbowS, rec[1], x_elbow_position, x_elbow_angles);
      Serial.println("-----------------------------");
    }

  }
}

int translate(
  Servo& servo,
  char _rec,
  int _position,
  int _angles[9])
{
  if (abs(_position - (_rec - '0')) > 0) {
    _position = (_rec - '0');
//    servo.write(_angles[_position - 1]);
    Serial.println(_position);
  }
  return _position;
}
