'''
@author: Kawin Nikomborirak
@date: 2018/04/02
@brief: This class has keeps track of the paper state.
'''

import cv2
import os
import re
import numpy as np


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
        stepRegxp = re.compile('step[0-9]+\.(jpg|png)')
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
        self.step = self.steps[0]
        self.cap = cv2.VideoCapture(0)

    def project(self):
        while(True):
            # Captures fram-by-frame in "frame" and
            # whether there is a frame or not (boolean) in ret
            ret, frame = self.cap.read()
            # Display the resulting frame, note that the 0xFF is only really needed when numlock is on
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything is done, release the Capture
        self.cap.release()
        cv2.destroyAllWindows()




i = projectInstruction('sample')
i.project()
#cv2.imshow("help",i.steps[0])
