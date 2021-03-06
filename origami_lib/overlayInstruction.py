#!/usr/bin/env python
# @author: Kawin Nikomborirak
# @date: 2018-04-22

import numpy as np
import cv2
from .InstructionPaper import Instruction


def overlayInstruction(real, instruction):
    '''Overlay the instructions onto real camera input

    Parameters:
    real: np.ndarray (shape: (,,3))
      An image of camera input
    instruction: np.ndarray (shape: (,,3))
      An image of the instructions.

    Returns:
    np.ndarray (shape: (,,3))
      An image with the instructions overlayed onto the camera input.
    '''

    gray = cv2.cvtColor(instruction, cv2.COLOR_BGR2GRAY)
    outline = np.uint8(gray > 8) * 255
    verts = cv2.goodFeaturesToTrack(outline, 100, 0.5, 10)[:, 0]
    area = computeArea(verts)
    realGray = cv2.cvtColor(real, cv2.COLOR_BGR2GRAY)
    th = cv2.threshold(realGray, 128, 255, cv2.THRESH_BINARY)[1]
    try:
        realVerts = cv2.goodFeaturesToTrack(th, 100, .4, 10)[:, -1]
    except TypeError:
        return real
    if realVerts.shape[0] < 3:
        return real
    realArea = computeArea(realVerts)
    scale = np.sqrt(realArea / area)
    resized = resizeInstruction(instruction, scale)

    # Get centroid to find point to overlay
    realCentroid = realVerts.mean(0)
    centroid = verts.mean(0) * scale
    shift = np.int0(realCentroid - centroid)
    shiftNonNegative = shift.copy()
    shiftNonNegative[shiftNonNegative < 0] = 0

    # resize image and pad/trim to match real image
    topPad = shift[1]
    bottomPad = real.shape[0] - resized.shape[0] - topPad
    leftPad = shift[0]
    rightPad = real.shape[1] - resized.shape[1] - leftPad
    padding = np.reshape(
        [topPad, bottomPad, leftPad, rightPad, 0, 0], (-1, 2))
    nonNegPadding = padding.copy()
    nonNegPadding[nonNegPadding < 0] = 0
    padded = np.pad(resized, nonNegPadding,
                    'constant', constant_values=255)
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

    # add instruction on top of real
    gray = cv2.cvtColor(trimmed, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]
    invMask = np.bitwise_not(mask)
    fg = cv2.bitwise_and(trimmed, trimmed, mask=invMask)
    bg = cv2.bitwise_and(real, real, mask=mask)
    return cv2.add(bg, fg)


def sortVerts(verts):
    '''Sort vertices in clockwise order

    Parameters:
    verts: np.ndarray (shape: (-1,2))
      Coordinates of vertices.

    Returns:
    np.ndarray (shape: (-1, 2))
      Vertices sorted in clockwise order.
    '''

    centroid = verts.mean(0)
    d = verts - centroid
    an = (np.arctan2(d[:, 0], d[:, 1]) + 2 * np.pi) % (2 * np.pi)
    cornersWithAn = np.hstack((verts, an.reshape(-1, 1))).tolist()
    cornersWithAn.sort(key=lambda p: p[-1])
    return np.array(cornersWithAn)[:, :-1]


def computeArea(verts):
    '''Compute area using the shoelace formula.

    Parameters:
    verts: np.ndarray (shape: (-1,2))
      Coordinates of vertices.

    Returns:
    A float for the area of the polygon traced by the vertices.
    '''

    verts = sortVerts(verts)
    rolled = np.roll(verts, -1, 0)
    shoelace = verts[:, 0] * rolled[:, 1]\
        - verts[:, 1] * rolled[:, 0]
    return np.abs(shoelace.sum()) / 2


def resizeInstruction(instruction, scale):
    '''Resize the instruction image based on a scale.
    Parameters:
    instruction: np.ndarray (shape: (,,3))
      An image of the instructions.
    scale: float
      A scale factor.

    Returns:
    np.ndarray (shape: (,,3))
     An scaled image.
    '''
    dim = np.int0(scale * np.float64(instruction.shape))[:-1]
    return cv2.resize(instruction, (dim[1], dim[0]))


def overlayVideo(cap, directory):
    '''Overlay the instructions on a video
    Parameters:
    cap: cv2.VideoCapture
      A source from which to get camera input.
    directory: string
      A string pointing to a directory of instruction images.

    Returns:
    NoneType
    '''
    x = Instruction(directory)
    while x.running:
        ret, frame = cap.read()
        instruction = x.steps[x.currentStep]
        cv2.imshow("test", overlayInstruction(frame, instruction))
        if cv2.waitKey(1) == ord(' '):
            x.nextStep()

    cap.release()
    cv2.destroyAllWindows()


def run(directory):
    '''Run the overlayVideo on a video device.
    Parameters:
    directory: string
      A string pointing to a directory of instruction images.

    Returns:
    NoneType
    '''
    try:
        cap = cv2.VideoCapture(1)
        overlayVideo(cap, directory)
    except cv2.error:
        cap = cv2.VideoCapture(0)
        overlayVideo(cap, directory)


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    overlayVideo(cap, "CompGenInstructions")
