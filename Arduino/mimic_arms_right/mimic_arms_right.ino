#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial Bluetooth(D6, D7);
SoftwareSerial Hand(D4, D5);
char Buf[30];

int translate(
  Servo& servo,
  char _rec,
  int _position,
  int _angles[9],
  int*_charge)
{
  if (*_charge == (_rec - '0')) {
    _position = (_rec - '0');
    servo.write(_angles[_position]);
    Serial.print("Move To ");
    Serial.println(_position);
  } else {
    *_charge = (_rec - '0');
    Serial.print(" Charge to");
    Serial.println(*_charge);
  }
  return _position;
}

const char part = 'a';
const char handPart = 'h';
const int init_pos = 10;

Servo a_elbowS;
int a_elbow_position = init_pos;
int a_elbow_charge = 69;
int a_elbow_angles[10] = {30, 50, 60, 80, 100, 120, 140, 160, 170, 180};

//Servo z_shoulderS;
//int z_shoulder_position = init_pos;
//int z_shoulder_charge = 69;
//int z_shoulder_angles[10] = {110, 120, 130, 140, 150, 160, 170, 180, 180, 180};

Servo y_shoulderS;
int y_shoulder_position = init_pos;
int y_shoulder_charge = 69;
int y_shoulder_angles[10] = {160, 150 , 140, 130, 120, 110, 100, 90, 80, 70};
  
void setup() {
  //-Communication
  Bluetooth.begin(9600);
  Hand.begin(9600);
  Serial.begin(19200);

  //-Init Servos
  a_elbowS.attach(D2, 500, 2400);
  //  z_shoulderS.attach(D3,500,2400);
  y_shoulderS.attach(D1, 500, 2400);

  //-Init position
  a_elbowS.write(a_elbow_angles[a_elbow_position - 1]);
  //  z_shoulderS.write(z_shoulder_angles[z_shoulder_position-1]);
  y_shoulderS.write(y_shoulder_angles[y_shoulder_position - 1]);
}

void loop() {
  if (Bluetooth.available() > 0) {
    String rec = Bluetooth.readStringUntil('$');
    //    Serial.println(rec);
    if (rec[0] == part) {
      a_elbow_position = translate(a_elbowS, rec[1], a_elbow_position, a_elbow_angles, &a_elbow_charge);
      //      z_shoulder_position = translate(z_shoulderS, rec[1], z_shoulder_position, z_shoulder_angles, &z_shoulder_charge);
      y_shoulder_position = translate(y_shoulderS, rec[3], y_shoulder_position, y_shoulder_angles, &y_shoulder_charge);
    } else if (rec[0] == handPart) {
      rec.toCharArray(Buf,30);                                                                                                                                                                                                                                                                                                                                                                                                                                     
      Hand.write(Buf,30);
      Serial.print("send to Hand");
      Serial.println(rec);
    }
  }
}
