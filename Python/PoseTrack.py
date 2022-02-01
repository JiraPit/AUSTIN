from time import sleep
import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark as body
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
    # print (pose_result.pose_world_landmarks.landmark)
    
    if pose_result.pose_world_landmarks:
        lms = pose_result.pose_world_landmarks.landmark
        print(
            lms[body.RIGHT_WRIST]
        )
        # mpDraw.plot_landmarks(pose_result.pose_world_landmarks, mpPose.POSE_CONNECTIONS)

    sleep(0.2)
    cv2.imshow('ResultPose',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()