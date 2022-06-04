#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial Bluetooth(D5, D6);

int init_pos = 9;

Servo thumbS;
Servo palmS;
int thumb_position = init_pos;
int thumb_angles[9] = {140, 140, 140, 140, 110, 70, 30, 30, 30};
int palm_angles[9] = {140, 140, 140, 140, 110, 70, 30, 30, 30};

Servo indexS;
int index_position = init_pos;
int index_angles[9] = {30, 30, 30, 50, 80, 120, 170, 170, 170};

Servo middleS;
int middle_position = init_pos;
int middle_angles[9] = {170, 170, 170, 150, 120, 60, 30, 20, 20};

Servo ringS;
int ring_position = init_pos;
int ring_angles[9] = {50, 50, 50, 60, 100, 130, 170, 170, 170};

Servo pinkyS;
int pinky_position = init_pos;
int pinky_angles[9] = {50, 50, 50, 60, 80, 120, 150, 150, 150};

void setup() {
  //-Communication
  Bluetooth.begin(9600);
  Serial.begin(115200);
  
  //-Init Servos
  thumbS.attach(D0,500,2400);
  indexS.attach(D1,500,2400);
  middleS.attach(D2,500,2400);
  ringS.attach(D3,500,2400);
  pinkyS.attach(D4,500,2400);
  
  //-Init position
  thumbS.write(thumb_angles[thumb_position-1]);
  indexS.write(index_angles[index_position-1]);
  middleS.write(middle_angles[middle_position-1]);
  ringS.write(ring_angles[ring_position-1]);
  pinkyS.write(pinky_angles[pinky_position-1]);

}
void loop() {
  if (Bluetooth.available() > 0) {
    String rec = Bluetooth.readStringUntil('$');
    if (rec[0] == 'L') {
//      thumb_position = translate(thumbS, rec[2], thumb_position, thumb_angles);
      index_position = translate(indexS, rec[3], index_position, index_angles);
      middle_position = translate(middleS, rec[4], middle_position, middle_angles);
      ring_position = translate(ringS, rec[5], ring_position, ring_angles);
      pinky_position = translate(pinkyS, rec[6], pinky_position, pinky_angles);
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
    servo.write(_angles[_position - 1]);
    Serial.println(_position);
  }
  return _position;
}
