import sub.LocalFunction as lFunc
from time import sleep
import mediapipe as mp
import serial
import cv2

##Serial
SERIAL_ENABLED = True
SERIAL_PORT = 'COM7'
if SERIAL_ENABLED : serialPort = serial.Serial(port=SERIAL_PORT, baudrate=115200, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)

## Solutions
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

##Define
parts = mpHands.HandLandmark #-Landmark List
hand_model = mpHands.Hands() #-Model
cam = cv2.VideoCapture(0) #-Camera

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
            wrist = hand.landmark[parts.WRIST]
            #-Fingers
            FingerVectors = {
                'thumbVector'   :   lFunc.normalize_vector(parts.THUMB_TIP,hand.landmark[parts.PINKY_MCP],hand,0.15),
                'indexVector'   :   lFunc.normalize_vector(parts.INDEX_FINGER_TIP,wrist,hand,0.2),
                'middleVector'  :   lFunc.normalize_vector(parts.MIDDLE_FINGER_TIP,wrist,hand,0.2),
                'ringVector'    :   lFunc.normalize_vector(parts.RING_FINGER_TIP,wrist,hand,0.2),
                'pinkyVector'   :   lFunc.normalize_vector(parts.PINKY_TIP,wrist,hand,0.2),
            }
            #-Orientation
            orientation = lFunc.orientaion(hand,parts,0.1)
            #-Serial
            if SERIAL_ENABLED: 
                data = f'{result.multi_handedness[i].classification[0].label[0]}{orientation}{"".join(list(FingerVectors.values()))}'
                print(data)
                serialPort.write(data.encode())
                sleep(1)

    cv2.imshow('ResultHand',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    # sleep(0.33)

cam.release()
cv2.destroyAllWindows()

