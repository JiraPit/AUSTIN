#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial Bluetooth(10, 11);

int init_pos = 9;

Servo thumb;
int thumb_position = init_pos;
int thumb_angles[9] = {140, 140, 140, 140, 110, 70, 30, 30, 30};

Servo index;
int index_position = init_pos;
int index_angles[9] = {30, 30, 30, 50, 80, 120, 170, 170, 170};

Servo middle;
int middle_position = init_pos;
int middle_angles[9] = {170, 170, 170, 150, 120, 60, 30, 20, 20};

Servo ring;
int ring_position = init_pos;
int ring_angles[9] = {50, 50, 50, 60, 100, 130, 170, 170, 170};

Servo pinky;
int pinky_position = init_pos;
int pinky_angles[9] = {50, 50, 50, 60, 80, 120, 150, 150, 150};

void setup() {
  Bluetooth.begin(9600);
  Serial.begin(115200);

  thumb.attach(3);
  index.attach(4);
  middle.attach(5);
  ring.attach(6);
  pinky.attach(7);

  thumb.write(thumb_angles[thumb_position - 1]);
  index.write(index_angles[index_position - 1]);
  middle.write(middle_angles[middle_position - 1]);
  ring.write(ring_angles[ring_position - 1]);
  pinky.write(pinky_angles[pinky_position - 1]);

}
void loop() {
  if (Bluetooth.available() > 0) {
    String rec = Bluetooth.readStringUntil('$');
    if (rec[0] == 'L') {
      thumb_position = translate(thumb, rec[2], thumb_position, thumb_angles);
      index_position = translate(index, rec[3], index_position, index_angles);
      middle_position = translate(middle, rec[4], middle_position, middle_angles);
      ring_position = translate(ring, rec[5], ring_position, ring_angles);
      pinky_position = translate(pinky, rec[6], pinky_position, pinky_angles);
      Serial.println("-----------------------------");
    }

  }
}

int translate(
  Servo _servo,
  char _rec,
  int _position,
  int _angles[9])
{
  if (abs(_position - (_rec - '0')) > 1) {
    _position = (_rec - '0');
    Serial.println(_position);
    _servo.write(_angles[_position - 1]);
  }
  return _position;

}
