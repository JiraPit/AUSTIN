from math import sqrt
from time import sleep
import mediapipe as mpp
import serial
import cv2

##Serial
SERIAL_ENABLED = False
SERIAL_PORT = 'COM7'
if SERIAL_ENABLED : serialPort = serial.Serial(port=SERIAL_PORT, baudrate=9600, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)

## Solutions
mpHands = mpp.solutions.hands
mpDraw = mpp.solutions.drawing_utils

##Define
lms = mpHands.HandLandmark #-Landmark List
hand_model = mpHands.Hands() #-Model
cam = cv2.VideoCapture(0) #-Camera

##Method
def NormalVector(name,wrist,hand):
    landmarks = hand.landmark[name]
    AbsoluteVector = sqrt(
        (landmarks.x - wrist.x)**2 
        + (landmarks.y - wrist.y)**2 
        + (landmarks.z - wrist.z)**2
        )
    return int((AbsoluteVector/0.2)*9)

while True:
    #-generating image
    checker,img = cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    #-processing
    result = hand_model.process(imgRGB)
    if result.multi_hand_landmarks:
        for i in range(len(result.multi_hand_landmarks)):
            #-2D
            mpDraw.draw_landmarks(
            img,
            result.multi_hand_landmarks[i],
            mpHands.HAND_CONNECTIONS,)

            #-3D
            hand = result.multi_hand_world_landmarks[i]

            #-Wrist (Mid Point)
            wrist = hand.landmark[lms.WRIST]

            #-Fingers
            indexVector = NormalVector(lms.INDEX_FINGER_TIP,wrist,hand)
            middleVector = NormalVector(lms.MIDDLE_FINGER_TIP,wrist,hand)

            #-Serial
            if True: 
                print(f'{result.multi_handedness[i].classification[0].label[0]},{indexVector},{middleVector}')

    cv2.imshow('ResultHand',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    sleep(0.33)

cam.release()
cv2.destroyAllWindows()

