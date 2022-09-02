#include <Servo.h>

int init_pos = 9;
char Buf[30];
char part = 'h';

Servo thumbS;
Servo palmS;
int thumb_position = init_pos;
int palm_position = init_pos;
int thumb_angles[9] = {50, 50, 60, 80, 90, 110, 130, 130, 130};
int palm_angles[9] = {140, 140, 120, 110, 100, 80, 70, 60, 60};

Servo indexS;
int index_position = init_pos;
int index_angles[9] = {160, 160, 160, 150, 130, 110, 80, 60, 60};

Servo middleS;
int middle_position = init_pos;
int middle_angles[9] = {0, 20, 40, 60, 80, 100, 120, 140, 140};

Servo ringS;
int ring_position = init_pos;
int ring_angles[9] = {10, 20, 40, 60, 80, 120, 140, 160, 160};

Servo pinkyS;
int pinky_position = init_pos;
int pinky_angles[9] = {20, 40, 60, 80, 120, 140, 160, 180, 180};

Servo rotationS;
int rotation_position = init_pos;
int rotation_angles[9] = {150, 150, 130, 110, 90, 70, 50, 30, 0};

void setup() {
  //-Communication
  Serial.begin(9600);
  
  //-Init Servos
  thumbS.attach(D0,500,2400);
  indexS.attach(D6,500,2400);
  middleS.attach(D2,500,2400);
  ringS.attach(D3,500,2400);
  pinkyS.attach(D4,500,2400);
  palmS.attach(D5,500,2400);
  rotationS.attach(D7,500,2400);
  
  //-Init position
  thumbS.write(thumb_angles[thumb_position-1]);
  indexS.write(index_angles[index_position-1]);
  middleS.write(middle_angles[middle_position-1]);
  ringS.write(ring_angles[ring_position-1]);
  pinkyS.write(pinky_angles[pinky_position-1]);
  palmS.write(palm_angles[palm_position-1]);
  rotationS.write(rotation_angles[rotation_position-1]);

}
void loop() {
  if (Serial.available() > 0) {
    Serial.readBytes(Buf,30);
    String rec = String(Buf);
    Serial.println(rec);
    if (rec[0] == part) {
      thumb_position = translate(thumbS, rec[2], thumb_position, thumb_angles);
      palm_position = translate(palmS, rec[2], palm_position, palm_angles);
      index_position = translate(indexS, rec[3], index_position, index_angles);
      middle_position = translate(middleS, rec[4], middle_position, middle_angles);
      ring_position = translate(ringS, rec[5], ring_position, ring_angles);
      pinky_position = translate(pinkyS, rec[6], pinky_position, pinky_angles);
      rotation_position = translate(rotationS, rec[1], rotation_position, rotation_angles);
//      Serial.println(rotation_position,thumb_position,palm_position,index_position,middle_position,ring_position,pinky_position)
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
  if ((_rec - '0') != _position) {
    _position = (_rec - '0');
    int topos = _position - 1;
    if (topos<0){
      topos = 0;
    }
    servo.write(_angles[topos]);
  }
  return _position;
}
