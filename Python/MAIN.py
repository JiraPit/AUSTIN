from time import sleep
import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark as body
import mimic_robot_utils.VectorUtils as vu
import mimic_robot_utils.SerialCommunication as scu
import cv2

##Serial
SERIAL_ENABLED = True
if SERIAL_ENABLED : 
    R_PORT,L_PORT = scu.get_port()
    print(R_PORT," , ",L_PORT)

##Visualize
DRAW = True
PLOT = False

##Define
CAM = cv2.VideoCapture(0)
MP_POSE = mp.solutions.pose
MP_HANDS = mp.solutions.hands
MP_DRAW = mp.solutions.drawing_utils
MP_DRAW_STYLE = mp.solutions.drawing_styles
PARTS = MP_HANDS.HandLandmark
POSE_MODEL = MP_POSE.Pose(model_complexity=2)
HAND_MODEL = MP_HANDS.Hands()

while True:
    r_hand_data, l_hand_data, r_arm_data, l_arm_data = (None,None,None,None)
    checker,img = CAM.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    pose_result = POSE_MODEL.process(imgRGB)
    hand_result = HAND_MODEL.process(imgRGB)

    ###POSE
    if pose_result.pose_world_landmarks:
        #- Visualize
        if DRAW: 
            MP_DRAW.draw_landmarks(img,pose_result.pose_landmarks,MP_POSE.POSE_CONNECTIONS)

        #- Get Landmarks
        lms3 = pose_result.pose_world_landmarks.landmark
        lms2 = pose_result.pose_landmarks.landmark

        #-Calculate Angles
        #Elbows
        RAElbow = vu.FindAngle(
            init=lms3[body.RIGHT_WRIST],
            mid=lms3[body.RIGHT_ELBOW],
            final=lms3[body.RIGHT_SHOULDER],
        ).around_ALL.normalized_seta(70,170)

        LAElbow = vu.FindAngle(
            init=lms3[body.LEFT_WRIST],
            mid=lms3[body.LEFT_ELBOW],
            final=lms3[body.LEFT_SHOULDER],
        ).around_ALL.normalized_seta(70,170)

        #Shoulder
        RZShoulder= vu.FindAngle(
            init=lms3[body.RIGHT_HIP],
            mid=lms3[body.RIGHT_SHOULDER],
            final=lms3[body.RIGHT_ELBOW],
        ).around_Z.normalized_seta(0,90)

        LZShoulder = vu.FindAngle(
            init=lms3[body.LEFT_HIP],
            mid=lms3[body.LEFT_SHOULDER],
            final=lms3[body.LEFT_ELBOW],
        ).around_Z.normalized_seta(0,90)

        RYShoulder = vu.FindAngle(
            init=lms3[body.RIGHT_WRIST],
            mid=None,
            final=lms3[body.RIGHT_ELBOW]
        ).by_distance(absolue_max=0.17,to_positive=True)

        LYShoulder = vu.FindAngle(
            init=lms3[body.LEFT_WRIST],
            mid=None,
            final=lms3[body.LEFT_ELBOW],
        ).by_distance(absolue_max=0.17,to_positive=True)

        r_arm_data = f'a{RAElbow}{RZShoulder}{RYShoulder}$'
        l_arm_data = f'a{LAElbow}{LZShoulder}{LYShoulder}$'

    if hand_result.multi_hand_landmarks:
        for i in range(len(hand_result.multi_hand_landmarks)):
            #-2D
            MP_DRAW.draw_landmarks(img,hand_result.multi_hand_landmarks[i],MP_HANDS.HAND_CONNECTIONS)
            #-3D
            hand = hand_result.multi_hand_world_landmarks[i]
            #-Wrist (Mid Point)
            wrist = hand.landmark[PARTS.WRIST]
            #-Fingers
            FingerVectors = {
                'thumbVector'   :   vu.Hand(hand).normalized_absolute_vector(PARTS.THUMB_TIP,hand.landmark[PARTS.PINKY_MCP],0.15),
                'indexVector'   :   vu.Hand(hand).normalized_absolute_vector(PARTS.INDEX_FINGER_TIP,wrist,0.2),
                'middleVector'  :   vu.Hand(hand).normalized_absolute_vector(PARTS.MIDDLE_FINGER_TIP,wrist,0.2),
                'ringVector'    :   vu.Hand(hand).normalized_absolute_vector(PARTS.RING_FINGER_TIP,wrist,0.2),
                'pinkyVector'   :   vu.Hand(hand).normalized_absolute_vector(PARTS.PINKY_TIP,wrist,0.2),
            }
            #-Orientation
            orientation = vu.Hand(hand).orientaion(0.1)

            #-Prepare Data
            if (str(hand_result.multi_handedness[i].classification[0].label[0]) == "R"):
                r_hand_data = f'h{orientation}{"".join(list(FingerVectors.values()))}$'
            elif (str(hand_result.multi_handedness[i].classification[0].label[0]) == "L"):
                l_hand_data = f'h{abs(9-orientation)}{"".join(list(FingerVectors.values()))}$'

    print(
        r_hand_data,
        l_hand_data,
        r_arm_data,
        l_arm_data,
    )

    #-Serial
    if SERIAL_ENABLED: 
        #-R
        # if R_PORT != None:
        #     if r_hand_data != None:
        #         R_PORT.write(bytes(r_hand_data.replace("\n","").replace("\t","").replace(" ","").replace(",",""),'UTF-8'))
        #     if r_arm_data != None:
        #         R_PORT.write(bytes(r_arm_data.replace("\n","").replace("\t","").replace(" ","").replace(",",""),'UTF-8'))
        # #-L
        if L_PORT != None:
            if l_hand_data != None:
                L_PORT.write(bytes(l_hand_data.replace("\n","").replace("\t","").replace(" ","").replace(",",""),'UTF-8'))
            if l_arm_data != None:
                L_PORT.write(bytes(l_arm_data.replace("\n","").replace("\t","").replace(" ","").replace(",",""),'UTF-8'))

        sleep(0.2)
    
    
    cv2.imshow('ResultPose',img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

CAM.release()
cv2.destroyAllWindows()