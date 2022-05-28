from time import sleep
import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark as body
import local_utils.VectorUtils as vUtils
import cv2

cam = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
mpDawingStyles = mp.solutions.drawing_styles
pose = mpPose.Pose(
    model_complexity=2
)

while True:
    checker,img = cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    pose_result = pose.process(imgRGB)
    
    if pose_result.pose_world_landmarks:
        lms = pose_result.pose_world_landmarks.landmark
        rWrist = lms[body.RIGHT_WRIST]
        rElbow = lms[body.RIGHT_ELBOW]
        rShoulder = lms[body.RIGHT_SHOULDER]
        print(vUtils.find_seta(
            init=rWrist,
            mid=rElbow,
            final=rShoulder,
        ))
        # print(rWrist.x)
        # mpDraw.plot_landmarks(pose_result.pose_world_landmarks, mpPose.POSE_CONNECTIONS)
        mpDraw.draw_landmarks(
            img,
            pose_result.pose_landmarks,
            mpPose.POSE_CONNECTIONS
            )
    
    sleep(0.1)
    cv2.imshow('ResultPose',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()