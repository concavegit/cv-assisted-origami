'''
@author: Kawin Nikomborirak
@date: 2018/04/02
@brief: This class has keeps track of the paper state.
'''

import cv2
import os
import re


class Instruction:
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

        files = os.listdir('stepDir')
        stepRegxp = re.compile('step[0-9]+\.(jpg|png)')
        stepFiles = list(filter(None, [stepRegxp.match(img) for img in files]))
        stepFiles = [match.group() for match in stepFiles]
        self.steps = [cv2.imread(filepath) for filepath in stepFiles]

    def nextStep(self):
        '''Proceed to next step unless all steps are exhausted'''
        self.currentStep += 1 if self.currentStep < len(self.steps) else 0
