from time import sleep
import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark as body
import mimic_robot_utils.VectorUtils as vu
import mimic_robot_utils.SerialCommunication as scu
import cv2

##Serial0
SERIAL_ENABLED = True
if SERIAL_ENABLED : serialPort = scu.get_port()

##Visualize
DRAW = True
PLOT = False

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
        #- Visualize
        if DRAW:
            mpDraw.draw_landmarks(
                        img,
                        pose_result.pose_landmarks,
                        mpPose.POSE_CONNECTIONS
                        )
        if PLOT:
            mpDraw.plot_landmarks(pose_result.pose_world_landmarks, mpPose.POSE_CONNECTIONS)
        #- Get Landmarks
        lms3 = pose_result.pose_world_landmarks.landmark
        lms2 = pose_result.pose_landmarks.landmark
        #-Calculate Angles
        #Elbows
        RZElbow = vu.FindAngle(
            init=lms3[body.RIGHT_WRIST],
            mid=lms3[body.RIGHT_ELBOW],
            final=lms3[body.RIGHT_SHOULDER],
        ).around_ALL.normalized_seta(70,170)
        LZElbow = vu.FindAngle(
            init=lms3[body.LEFT_WRIST],
            mid=lms3[body.LEFT_ELBOW],
            final=lms3[body.LEFT_SHOULDER],
        ).around_ALL.normalized_seta(70,170)
        #Shoulder
        RZShoulder= vu.FindAngle(
            init=lms3[body.RIGHT_HIP],
            mid=lms3[body.RIGHT_SHOULDER],
            final=lms3[body.RIGHT_ELBOW],
        ).around_Z.seta
        LZShoulder = vu.FindAngle(
            init=lms3[body.LEFT_HIP],
            mid=lms3[body.LEFT_SHOULDER],
            final=lms3[body.LEFT_ELBOW],
        ).around_Z.seta
        RXShoulder= vu.FindAngle(
            init=lms3[body.RIGHT_ELBOW],
            mid=lms3[body.RIGHT_SHOULDER],
            final=lms3[body.RIGHT_HIP],
        ).around_X.seta
        LXShoulder= vu.FindAngle(
            init=lms3[body.LEFT_ELBOW],
            mid=lms3[body.LEFT_SHOULDER],
            final=lms3[body.LEFT_HIP],
        ).around_X.seta
        #-Prepare Data
        data = f'''
        r,{RZElbow},{RZShoulder},{RXShoulder}$
        l,{LZElbow},{LZShoulder},{LXShoulder}$
        '''.replace("\n","")
        print(data)
        #-Serial
        if SERIAL_ENABLED: 
            serialPort.write(data.replace("\t","").replace(" ","").replace(",","").encode())
    sleep(0.25)
    cv2.imshow('ResultPose',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

CAM.release()
cv2.destroyAllWindows()