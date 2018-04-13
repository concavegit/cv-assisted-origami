'''
@author: Kawin Nikomborirak
@date: 2018/04/02
@brief: These classes has keeps track of the paper state.
'''

import cv2
import os
import re
import numpy as np
from PIL import Image


class Instruction(object):
    def __init__(self, stepDir):
        '''Initialize with a path to the directory containg the images
        named step%d.(png|jpg).
        Each image has edges drawn in black (#000000), with the new
        fold in red (#ff0000)

        Fields:
        currentStep: The current step in the instructions, an Int
        steps: A list of images as described above.
        '''

        self.currentStep = 0

        files = os.listdir(stepDir)
        stepRegxp = re.compile('step[0-9]+\.(jpg)')
        stepFiles = list(filter(None, [stepRegxp.match(img) for img in files]))
        stepFiles = [match.group() for match in stepFiles]
        self.steps = [cv2.imread(stepDir + '/' + filepath) for filepath in stepFiles]

    def nextStep(self):
        '''Proceed to next step unless all steps are exhausted'''
        self.currentStep += 1 if self.currentStep < len(self.steps) else 0

class projectInstruction(Instruction):
    """ This class will fetch an instruction and project in onto the origami paper in real time"""
    # Find centroid AND THEN scale image as well as centroid
    def __init__(self, stepDir):
        super().__init__(stepDir)

    def overlayInstructions(self, frame):
        img = Image.open(self.steps[1])
        img = img.thumbnail((480,640), Image.ANTIALIAS)
        rows, cols, channels = img.shape
        print(rows, cols)
        roi = frame[0:rows, 0:cols]
        img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 150, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        cv2.imshow("mask", mask_inv)
        img_b = cv2.bitwise_and(roi, roi, mask = mask_inv)
        return frame
        
i = projectInstruction('sample')
#cv2.imshow("help", i.steps[1])
print(len(i.steps))

cap = cv2.VideoCapture(0)
while(True):
    # Captures fram-by-frame in "frame" and
    # whether there is a frame or not (boolean) in ret
    ret, frame = cap.read()
    frame = i.overlayInstructions(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything is done, release the Capture
cap.release()
cv2.destroyAllWindows()
