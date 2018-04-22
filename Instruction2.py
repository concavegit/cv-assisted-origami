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

        self.running = True
        files = sorted(os.listdir(stepDir))
        stepRegxp = re.compile('step[0-9]+\.png')
        stepFiles = list(filter(None, [stepRegxp.match(img) for img in files]))
        stepFiles = [match.group() for match in stepFiles]
        self.steps = [self.alphaToWhite(cv2.imread(stepDir + '/' + filepath, -1))
                      for filepath in stepFiles]

    def nextStep(self):
        '''Proceed to next step unless all steps are exhausted'''
        if self.currentStep < len(self.steps) - 1:
            self.currentStep += 1
        else:
            self.running = False

    def prevStep(self):
        '''Proceed to next step unless all steps are exhausted'''
        self.currentStep -= 1 if self.currentStep > 0 else 0

    def alphaToWhite(self, instruction):
        alpha = instruction[:, :, -1]
        mask = np.int8((alpha == 0) * 255)
        color = instruction[:, :, :-1]
        whiteBack = cv2.bitwise_not(color, np.array(color), mask=mask)

        # Color representation of instruction
        return whiteBack
