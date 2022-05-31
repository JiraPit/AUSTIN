from time import sleep
import mediapipe as mp
import serial
from mediapipe.python.solutions.pose import PoseLandmark as body
import local_utils.VectorUtils as vUtils
import cv2

##Serial
SERIAL_ENABLED = False
SERIAL_PORT = 'COM7'
if SERIAL_ENABLED : serialPort = serial.Serial(port=SERIAL_PORT, baudrate=115200, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)

##Define
CAM = cv2.VideoCapture(0)
mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
mpDawingStyles = mp.solutions.drawing_styles
pose = mpPose.Pose(model_complexity=2)

while True:
    checker,img = CAM.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    pose_result = pose.process(imgRGB)
    
    if pose_result.pose_world_landmarks:
        #- Draw
        mpDraw.draw_landmarks(
                    img,
                    pose_result.pose_landmarks,
                    mpPose.POSE_CONNECTIONS
                    )
        #- Get Landmarks
        lms = pose_result.pose_world_landmarks.landmark
        #-Calculate Angles
        #Elbows
        RZElbow = vUtils.find_seta(
            init=lms[body.RIGHT_WRIST],
            mid=lms[body.RIGHT_ELBOW],
            final=lms[body.RIGHT_SHOULDER],
        )
        LZElbow = vUtils.find_seta(
            init=lms[body.LEFT_WRIST],
            mid=lms[body.LEFT_ELBOW],
            final=lms[body.LEFT_SHOULDER],
        )
        #Shoulder
        RZShoulder= vUtils.find_seta(
            init=lms[body.RIGHT_HIP],
            mid=lms[body.RIGHT_SHOULDER],
            final=lms[body.RIGHT_ELBOW],
        )
        LZShoulder = vUtils.find_seta(
            init=lms[body.LEFT_HIP],
            mid=lms[body.LEFT_SHOULDER],
            final=lms[body.LEFT_ELBOW],
        )
        RXShoulder= vUtils.find_seta(
            init=lms[body.RIGHT_ELBOW],
            mid=lms[body.RIGHT_SHOULDER],
            final=lms[body.LEFT_SHOULDER],
        )
        LXShoulder= vUtils.find_seta(
            init=lms[body.LEFT_ELBOW],
            mid=lms[body.LEFT_SHOULDER],
            final=lms[body.RIGHT_SHOULDER],
        )
        #-Serial
        data = f'''
            rze{RZElbow}
            lze{LZElbow}
            rzs{RZShoulder}
            lzs{LZShoulder}
            rxs{RXShoulder}
            lxs{LXShoulder}
            $'''
        print(data)
        if SERIAL_ENABLED: 
                serialPort.write(data.encode())
                sleep(0.25)
    
    sleep(0.1)
    cv2.imshow('ResultPose',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

CAM.release()
cv2.destroyAllWindows()