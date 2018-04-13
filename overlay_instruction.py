'''
@author: Kawin Nikomborirak
@date: 2018/04/13
'''

import numpy as np
import cv2


class OverlayInstruction:
    def __init__(self, real, instruction):
        self.alphaToWhite(instruction)

        gray = cv2.cvtColor(self.instruction, cv2.COLOR_BGR2GRAY)

        # Just the outline of the shape
        self.outline = np.uint8((gray > 0)) * 255

        # An array of vertices
        self.vertices = cv2.goodFeaturesToTrack(
            self.outline, 100, 0.1, 10)[:, 0, :]

    def alphaToWhite(self, instruction):
        '''
        @brief: Convert the transparent instruction background to white.
        '''

        img = cv2.imread(instruction, -1)
        alpha = img[:, :, -1]
        mask = np.int8((alpha == 0) * 255)
        color = img[:, :, :-1]
        whiteBack = cv2.bitwise_not(color, np.array(color), mask=mask)

        # Color representation of instruction
        self.instruction = whiteBack
