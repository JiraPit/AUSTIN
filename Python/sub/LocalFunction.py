from math import sqrt
import numpy as np

##Calculate distance and normalize to 1-9
def normalize_vector(name,wrist,hand,max):
    landmarks = hand.landmark[name]
    AbsoluteVector = sqrt(
        (landmarks.x - wrist.x)**2 
        + (landmarks.y - wrist.y)**2 
        + (landmarks.z - wrist.z)**2
        )
    return str(round((AbsoluteVector/max)*9))

##Check hand orientation
def orientaion(hand,parts,threshold):
    index = hand.landmark[parts.INDEX_FINGER_MCP]
    pinky = hand.landmark[parts.PINKY_MCP]
    xDistance = pinky.x - index.x + threshold
    if xDistance<0: xDistance= 0
    if xDistance>(2*threshold): xDistance= (2*threshold)
    return str(round((xDistance/(2*threshold))*9))
