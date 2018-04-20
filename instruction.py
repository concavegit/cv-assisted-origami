'''
@author: Kawin Nikomborirak and Mark Goldwater
@date: 2018/04/02
@brief: These classes display instructions for the folder
'''

import cv2
import os
import re
import numpy as np
import pyttsx3


class Instruction(object):
    def __init__(self, stepDir):
        '''Initialize with a path to the directory containg the images
        named step%d.(jpg).
        '''
        self.finished = False
        self.said = False

        self.stepToSpeech = {0: "Fold in half", 1: "Fold in on the dotted line", 2: "Fold in on the dotted line", 3: "Turn over", 4: "Draw eyes and a nose"}
        self.stepCounter = 0

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 115)

        self.skipCounter = 0

        files = sorted(os.listdir(stepDir))
        stepRegxp = re.compile('Step[1-5]+\.(jpg)')
        stepFiles = list(filter(None, [stepRegxp.match(img) for img in files]))
        stepFiles = [match.group() for match in stepFiles]
        self.steps = [cv2.imread(stepDir + '/' + filepath) for filepath in stepFiles]

    def nextStep(self):
        '''Proceed to next step unless all steps are exhausted'''
        self.skipCounter = 0

        self.said = True
        if self.stepCounter < len(self.steps) - 1:
            self.stepCounter += 1
        else:
            self.finished = True
            self.stepCounter = 0
        self.currentStep = self.steps[self.stepCounter]
        self.said = False


class InstructUser(Instruction):
    """ This class will fetch an instruction and project it into the upper left corner or into the paper
    (currently only does upper left)"""

    # Find centroid AND THEN scale image as well as centroid
    def __init__(self, stepDir):
        super().__init__(stepDir)
        self.cap = cv2.VideoCapture(0)

    def overlayInstructions(self, frame):
        """Instruction mode 1: Instructinos displayed in the upper
        left corner"""

        img = self.steps[self.stepCounter]
        # scales image down by about a third
        res = cv2.resize(img, None, fx=0.7, fy=0.7)
        frame[0:res.shape[0], 0:res.shape[1]
              ] = res[0:res.shape[0], 0:res.shape[1]]
        return frame

    def projectOntoVideo(self):
        """Overlays a jpg of origami instructions onto the frame"""
        if self.said == False:
            self.skipCounter += 1
        # Captures fram-by-frame in "frame" and
        # whether there is a frame or not (boolean) in ret
        ret, frame = self.cap.read()
        frame = self.overlayInstructions(frame)
        #frame = i.overlayInstructions(frame)

        cv2.imshow('frame', frame)


        if not self.said and self.skipCounter > 2:
            self.stateInstructions()

    def stateInstructions(self):
        """States instructions at current step"""

        self.engine.say(self.stepToSpeech[self.stepCounter])
        self.engine.runAndWait()
        self.said = True

if __name__ == "__main__":
    assistant = InstructUser('OrigamiFox')
    while not assistant.finished:
        assistant.projectOntoVideo()
        if cv2.waitKey(1) & 0xFF == ord('k'):
            assistant.nextStep()
    # When everything is done, release the Capture
    assistant.cap.release()
    cv2.destroyAllWindows()
