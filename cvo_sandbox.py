"""Software Design

CV Assisted Origami
Olin College 2017-2018

Mark, Kevin, Sid
"""

import cv2
import numpy as np


def detect_white(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# define upper and lower ranges for detecting
	# a white piece of paper
	lower_white = np.array([100,150,0])
	upper_white = np.array([140,255,255])

	# threshold hsv to get white values only
	mask = cv2.inRange(hsv, lower_white, upper_white)

	# mask original frame
	img = cv2.bitwise_and(img, img, mask=mask)
	return img

def detection(img):
	im = img
	imgc = img

	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	imhsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)

	ret,thresh = cv2.threshold(imgray,127,255,0)

	image, contours, hiers = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	largest = max(contours, key = cv2.contourArea)

	x,y,w,h = cv2.boundingRect(largest)
	imgc = cv2.drawContours(imgc, largest, -1, (0,255,0), 3)

	cv2.rectangle(imgc,(x,y),(x+w,y+h),(0,0,255),3)
	#mask = cv2.inRange(imhsv, lower_white, upper_white)

	blur = cv2.GaussianBlur(img,(5,5),0)
	# Set threshold and maxValue
	thresh = 210
	maxValue = 255

	# Basic threshold example
	th, dst = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY);

	return dst

vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    ret, frame = vc.read()

while ret:
	rval, img = vc.read()
	#img = detection(img)
	img = detect_white(img)
	cv2.imshow("feed", img)
	key = cv2.waitKey(20)

	if key == 27:
		break

cv2.destroyWindow("feed")
