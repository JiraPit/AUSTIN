import local_utils.VectorUtils as vUtils
import local_utils.SerialCommunication as scu
from time import sleep
import mediapipe as mp

import cv2

##Serial
SERIAL_ENABLED = True
if SERIAL_ENABLED : serialPort = scu.get_port()

##Define
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
parts = mpHands.HandLandmark
HAND_MODEL = mpHands.Hands()
CAM = cv2.VideoCapture(0)

while True:
    #-generating image
    checker,img = CAM.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    #-processing
    result = HAND_MODEL.process(imgRGB)
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
                'thumbVector'   :   vUtils.normalized_absolute_vector(parts.THUMB_TIP,hand.landmark[parts.PINKY_MCP],hand,0.15),
                'indexVector'   :   vUtils.normalized_absolute_vector(parts.INDEX_FINGER_TIP,wrist,hand,0.2),
                'middleVector'  :   vUtils.normalized_absolute_vector(parts.MIDDLE_FINGER_TIP,wrist,hand,0.2),
                'ringVector'    :   vUtils.normalized_absolute_vector(parts.RING_FINGER_TIP,wrist,hand,0.2),
                'pinkyVector'   :   vUtils.normalized_absolute_vector(parts.PINKY_TIP,wrist,hand,0.2),
            }
            #-Orientation
            orientation = vUtils.orientaion(hand,0.1)
            #-Serial
            if SERIAL_ENABLED: 
                data = f'{result.multi_handedness[i].classification[0].label[0]}{orientation}{"".join(list(FingerVectors.values()))}$'
                print(data)
                serialPort.write(data.encode())
                sleep(0.25)

    cv2.imshow('ResultHand',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    # sleep(0.33)

CAM.release()
cv2.destroyAllWindows()

