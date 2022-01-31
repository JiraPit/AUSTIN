from time import sleep
import mediapipe as mp
import cv2

cam = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
mpDawingStyles = mp.solutions.drawing_styles
pose = mpPose.Pose()


while True:
    checker,img = cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    pose_result = pose.process(imgRGB)
    # print (pose_result.pose_world_landmarks.landmark)
    
    if pose_result.pose_world_landmarks:
        # print(
        #     f'Nose coordinates: ('
        #     f'{pose_result.pose_world_landmarks.landmark[pose_result.PoseLandmark.NOSE].x}, '
        #     f'{pose_result.pose_world_landmarks.landmark[pose_result.PoseLandmark.NOSE].y})'
        # )
        mpDraw.plot_landmarks(
        pose_result.pose_world_landmarks, mpPose.POSE_CONNECTIONS)

    sleep(0.5)
    cv2.imshow('ResultPose',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()