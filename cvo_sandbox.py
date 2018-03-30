"""Software Design

CV Assisted Origami
Olin College 2017-2018

Mark, Kevin, Sid
"""

import cv2
import numpy as np

lower_white = np.array([0,0,0], dtype=np.uint8)
upper_white = np.array([0,0,255], dtype=np.uint8)


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
    rval, frame = vc.read()
else:
    rval = False

while rval:
	rval, img = vc.read()
	img = detection(img)
	cv2.imshow("feed", img)
	key = cv2.waitKey(20)

	if key == 27:
		break
    
cv2.destroyWindow("feed")

