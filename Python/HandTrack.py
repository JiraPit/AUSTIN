from math import sqrt
from time import sleep
import mediapipe as mpp
import serial
import cv2

SEND_DATA = False

cam = cv2.VideoCapture(0)
serialPort = serial.Serial(port='COM7', baudrate=9600, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)
mpHands = mpp.solutions.hands
mpDraw = mpp.solutions.drawing_utils
hands = mpHands.Hands()

while True:
    checker,img = cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    result = hands.process(imgRGB)
    if result.multi_hand_world_landmarks:
        for handlm in result.multi_hand_world_landmarks:
            # mpDraw.draw_landmarks(img, handlm)
            wrist = handlm.landmark[mpHands.HandLandmark.WRIST]

            indexF = handlm.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            indexAbsoluteVector = sqrt((indexF.x - wrist.x)**2 + (indexF.y - wrist.y)**2 + (indexF.z - wrist.z)**2)
            indexNormalVector = int((indexAbsoluteVector/0.2)*9)

            midF = handlm.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
            midAbsoluteVector = sqrt((midF.x - wrist.x)**2 + (midF.y - wrist.y)**2 + (midF.z - wrist.z)**2)
            midNormalVector = int((midAbsoluteVector/0.2)*9)

            if SEND_DATA: serialPort.write(str(indexNormalVector).encode())


    cv2.imshow('ResultHand',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    sleep(0.33)

cam.release()
cv2.destroyAllWindows()