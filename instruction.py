'''
@author: Kawin Nikomborirak
@date: 2018/04/02
@brief: These classes has keeps track of the paper state.
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
        stepRegxp = re.compile('step[0-9]+\.(png)')
        stepFiles = list(filter(None, [stepRegxp.match(img) for img in files]))
        stepFiles = [match.group() for match in stepFiles]
        self.steps = [cv2.imread(stepDir + '/' + filepath)
                      for filepath in stepFiles]

    def nextStep(self):
        '''Proceed to next step unless all steps are exhausted'''
        self.currentStep += 1 if self.currentStep < len(self.steps) else 0


class projectInstruction(Instruction):
    """ This class will fetch an instruction and project it into the upper left corner or into the paper
    (currently only does upper left)"""

    # Find centroid AND THEN scale image as well as centroid
    def __init__(self, stepDir):
        super().__init__(stepDir)

    def overlayInstructions(self, frame):
        """Instruction mode 1: Instructinos displayed in the upper
        left corner"""

        img = self.steps[1]
        # scales image down by about a third
        res = cv2.resize(img, None, fx=0.3, fy=0.3)
        frame[0:res.shape[0] - 130, 0:res.shape[1] -
              30] = res[40:res.shape[0] - 90, 20:res.shape[1] - 10]
        return frame


if __name__ == "__main__":
    i = projectInstruction('CompGenInstructions')
    cap = cv2.VideoCapture(0)
    while(True):
        # Captures fram-by-frame in "frame" and
        # whether there is a frame or not (boolean) in ret
        ret, frame = cap.read()
        frame = i.overlayInstructions(frame)
        #frame = i.overlayInstructions(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything is done, release the Capture
    cap.release()
    cv2.destroyAllWindows()
