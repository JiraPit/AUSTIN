from math import sqrt,acos
import numpy as np
import mediapipe as mp

HAND_PARTS = mp.solutions.hands.HandLandmark

##Fake 3d landmarks
class LM:
    def __init__(self, x, y,z):
        self.x=x;self.y=y;self.z=z

##Calculate distance and normalize to 1-9
def normalized_absolute_vector(name:int,ref_point,hand,max:float) -> str:
    landmarks = hand.landmark[name]
    AbsoluteVector = sqrt(
        (landmarks.x - ref_point.x)**2 
        + (landmarks.y - ref_point.y)**2 
        + (landmarks.z - ref_point.z)**2
        )
    return str(round((AbsoluteVector/max)*9))

##Check hand orientation
def orientaion(hand,threshold:float) -> str:
    index = hand.landmark[HAND_PARTS.INDEX_FINGER_MCP]
    pinky = hand.landmark[HAND_PARTS.PINKY_MCP]
    xDistance = pinky.x - index.x + threshold
    if xDistance<0: xDistance= 0
    if xDistance>(2*threshold): xDistance= (2*threshold)
    return str(round((xDistance/(2*threshold))*9))

##Find angle between two vectors
def find_seta(init,mid,final) -> float:
    v1 = np.array([mid.x,mid.y,mid.z]) - np.array([init.x,init.y,init.z])
    v2 = np.array([mid.x,mid.y,mid.z]) - np.array([final.x,final.y,final.z]) 
    seta = acos(np.dot(v1, v2)/np.linalg.norm(v1)/np.linalg.norm(v2))
    seta = np.degrees(seta)
    return seta

