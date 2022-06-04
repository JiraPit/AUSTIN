from math import sqrt,acos
import numpy as np
import mediapipe as mp

HAND_PARTS = mp.solutions.hands.HandLandmark

##Fake 3d landmarks
class FakeLandmark:

    def __init__(self, x, y,z) -> None:
        self.x=x
        self.y=y
        self.z=z

##Get hand values
class Hand:

    def __init__(self,hand) -> None:
        self.hand = hand

    ##Calculate distance and normalize to 0-9
    def normalized_absolute_vector(self,name:int,ref_point,max:float) -> str:
        landmarks = self.hand.landmark[name]
        AbsoluteVector = sqrt(
            (landmarks.x - ref_point.x)**2 
            + (landmarks.y - ref_point.y)**2 
            + (landmarks.z - ref_point.z)**2
            )
        return str(round((AbsoluteVector/max)*9))

    ##Check hand orientation
    def orientaion(self,threshold:float) -> str:
        index = self.hand.landmark[HAND_PARTS.INDEX_FINGER_MCP]
        pinky = self.hand.landmark[HAND_PARTS.PINKY_MCP]
        xDistance = pinky.x - index.x + threshold
        if xDistance<0: xDistance= 0
        if xDistance>(2*threshold): xDistance= (2*threshold)
        return str(round((xDistance/(2*threshold))*9))

##Angle Object
class Seta:
    def __init__(self,seta) -> None:
        self.__seta = round(np.degrees(seta))
    
    ##Normalize seta to 0-9
    def normalized(self,min_value : int, max_value: int) -> int:
        step = (max_value - min_value)/9
        checker_value = min_value
        checker_time = 0
        while (checker_value < self.__seta):
            checker_value += step
            checker_time += 1
        return min(checker_time,9)
    
    ##Get seta
    @property
    def seta(self):
        return self.__seta

##Find angle between two vectors
class FindAngle:

    def __init__(self,init,mid,final) -> None:
        self.__init = init
        self.__mid = mid
        self.__final = final

    @property
    def around_ALL(self) -> Seta:
        v1 = np.array([self.__mid.x,self.__mid.y,self.__mid.z]) - np.array([self.__init.x,self.__init.y,self.__init.z])
        v2 = np.array([self.__mid.x,self.__mid.y,self.__mid.z]) - np.array([self.__final.x,self.__final.y,self.__final.z]) 
        seta = acos(np.dot(v1, v2)/np.linalg.norm(v1)/np.linalg.norm(v2))
        return Seta(seta)

    @property
    def around_Z(self) -> Seta:
        v1 = np.array([self.__mid.x,self.__mid.y]) - np.array([self.__init.x,self.__init.y])
        v2 = np.array([self.__mid.x,self.__mid.y]) - np.array([self.__final.x,self.__final.y]) 
        seta = acos(np.dot(v1, v2)/np.linalg.norm(v1)/np.linalg.norm(v2))
        return Seta(seta)

    @property
    def around_X(self) -> Seta:
        v1 = np.array([self.__mid.y,self.__mid.z]) - np.array([self.__init.y,self.__init.z])
        v2 = np.array([self.__mid.y,self.__mid.z]) - np.array([self.__final.y,self.__final.z]) 
        seta = acos(np.dot(v1, v2)/np.linalg.norm(v1)/np.linalg.norm(v2))
        return Seta(seta)


