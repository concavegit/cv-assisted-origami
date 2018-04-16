'''
@author: Kawin Nikomborirak and Mark Goldwater
@date: 2018/04/02
@brief: These classes display instructions for the folder
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

        self.stepOrder = [1, 0, 2, 4, 3]
        self.stepCounter = 0
        self.currentStep = self.stepOrder[self.stepCounter]

        files = os.listdir(stepDir)
        stepRegxp = re.compile('Step[1-5]+\.(jpg)')
        stepFiles = list(filter(None, [stepRegxp.match(img) for img in files]))
        stepFiles = [match.group() for match in stepFiles]
        self.steps = [cv2.imread(stepDir + '/' + filepath) for filepath in stepFiles]

    def nextStep(self):
        '''Proceed to next step unless all steps are exhausted'''
        if self.currentStep < len(self.steps):
            self.stepCounter += 1
        else:
            self.stepCounter = 0
        self.currentStep = self.stepOrder[self.stepCounter]

class projectInstruction(Instruction):
    """ This class will fetch an instruction and project it into the upper left corner or into the paper
    (currently only does upper left)"""

    # Find centroid AND THEN scale image as well as centroid
    def __init__(self, stepDir):
        super().__init__(stepDir)
        self.cap = cv2.VideoCapture(0)

    def overlayInstructions(self, frame):
        """Instruction mode 1: Instructinos displayed in the upper
        left corner"""

        img = self.steps[self.currentStep]
        # scales image down by about a third
        res = cv2.resize(img, None, fx=0.7, fy=0.7)
        frame[0:res.shape[0], 0:res.shape[1]] = res[0:res.shape[0], 0:res.shape[1]]
        return frame

    def projectOntoVideo(self):
        # Captures fram-by-frame in "frame" and
        # whether there is a frame or not (boolean) in ret
        ret, frame = self.cap.read()
        frame = i.overlayInstructions(frame)
        #frame = i.overlayInstructions(frame)
        cv2.imshow('frame', frame)



if __name__ == "__main__":
    i = projectInstruction('OrigamiFox')
    while True:
        i.projectOntoVideo()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('k'):
            i.nextStep()
    # When everything is done, release the Capture
    i.cap.release()
    cv2.destroyAllWindows()
