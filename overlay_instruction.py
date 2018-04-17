#!/usr/bin/env python
'''
@author: Kawin Nikomborirak
@date: 2018/04/13
'''

import numpy as np
import cv2
from Instruction2 import Instruction


class OverlayInstruction(Instruction):
    def __init__(self, real, instructionDir):
        '''
        Fields:
        - instruction: full color of instruction image
        - outline: grayscale instruction outline
        - verts: vertices of instruction outline
        - realVerts: vertices of real camera input
        '''

        super().__init__(instructionDir)

        self.nextStep()
        gray = cv2.cvtColor(self.steps[self.currentStep], cv2.COLOR_BGR2GRAY)

        # Just the outline of the shape
        self.outline = np.uint8((gray > 4)) * 255

        # An array of verts
        self.verts = cv2.goodFeaturesToTrack(
            self.outline, 100, 0.5, 10)[:, 0]
        self.verts = self.sortVerts(self.verts)
        self.area = self.computeArea(self.verts)

        self.real = real
        realGray = cv2.cvtColor(self.real, cv2.COLOR_BGR2GRAY)
        self.th = cv2.threshold(realGray, 128, 255, cv2.THRESH_BINARY)[1]

        # array of real verts
        self.realVerts = cv2.goodFeaturesToTrack(self.th, 100, .4, 10)[:, -1]
        self.realVerts = self.sortVerts(self.realVerts)
        self.realArea = self.computeArea(self.realVerts)

        self.resizeInstruction()
        self.overlayInstructions()

    def sortVerts(self, verts):
        '''
        Sort the verts in clockwise order.
        '''
        centroid = verts.mean(0)
        d = verts - centroid
        an = (np.arctan2(d[:, 0], d[:, 1]) + 2 * np.pi) % (2 * np.pi)
        cornersWithAngles = np.hstack((verts, an.reshape(-1, 1)))
        x = cornersWithAngles.tolist()
        x.sort(key=lambda point: point[-1])
        return np.array(x)[:, :-1]

    def computeArea(self, verts):
        '''
        Use shoelace formula to calculate area
        '''

        rolled = np.roll(verts, -1, 0)
        shoelace = verts[:, 0] * rolled[:, 1]\
            - verts[:, 1] * rolled[:, 0]
        return np.abs(shoelace.sum()) / 2

    def resizeInstruction(self):
        '''
        Resize the instruction image to match the area of the real image
        '''

        scale = np.sqrt(self.realArea / self.area)
        dim = np.int0(
            scale * np.float64(self.steps[self.currentStep].shape))[:-1]
        self.scale = scale
        self.resized = cv2.resize(
            self.steps[self.currentStep], (dim[1], dim[0]))

    def overlayInstructions(self):
        '''
        Draw the rest of the owl
        '''
        realCentroid = self.realVerts.mean(0)
        centroid = self.verts.mean(0) * self.scale
        shift = np.int0(realCentroid - centroid)
        shiftNonNegative = shift.copy()
        shiftNonNegative[shiftNonNegative < 0] = 0

        # pad the instruction according to the real image
        topPad = shift[1]
        bottomPad = self.real.shape[0] - self.resized.shape[0] - topPad
        leftPad = shift[0]
        rightPad = self.real.shape[1] - self.resized.shape[1] - leftPad
        padding = np.reshape(
            [topPad, bottomPad, leftPad, rightPad, 0, 0], (-1, 2))
        nonNegPadding = padding.copy()
        nonNegPadding[nonNegPadding < 0] = 0

        padded = np.pad(self.resized, nonNegPadding,
                        'constant', constant_values=255)

        # trim the padded image according to the real image
        trim = padding.copy()[:-1]
        trim[trim > 0] = 0
        trim[:, 0] = -trim[:, 0]
        bottomTrim = trim[0, 1]

        # if the trim on the side is zero, do not cut from the beginning
        rightTrim = trim[1, 1]
        bottomTrim = bottomTrim if bottomTrim < 0 \
            else padded.shape[0]
        rightTrim = rightTrim if rightTrim < 0 \
            else padded.shape[1]
        trimmed = padded[trim[0, 0]:bottomTrim, trim[1, 0]:rightTrim]

        gray = cv2.cvtColor(trimmed, cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]
        invMask = np.bitwise_not(mask)
        fg = cv2.bitwise_and(trimmed, trimmed, mask=invMask)
        bg = cv2.bitwise_and(self.real, self.real, mask=mask)
        overlayed = cv2.add(bg, fg)
        self.overlayed = overlayed


if __name__ == '__main__':
    # testing
    r = cv2.imread('PaperPics/triangle.jpg')
    x = OverlayInstruction(r, 'CompGenInstructions')
    for vert in np.int0(x.realVerts):
        w, y = vert.ravel()
        cv2.circle(x.overlayed, (w, y), 3, 255, -1)
    cv2.imshow('y', x.overlayed)
    cv2.waitKey()
    cv2.destroyAllWindows()
