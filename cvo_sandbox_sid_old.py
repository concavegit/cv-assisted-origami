"""Software Design

CV Assisted Origami
Olin College 2017-2018

Mark, Kevin, Sid
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

"""
def detection(frame):

	MIN_MATCH_COUNT = 10

	img1 = cv2.imread('pattern3.jpg',0)          # queryImage

	img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	orb = cv2.ORB_create()
	kp1, des1 = orb.detectAndCompute(img1,None)
	kp2, des2 = orb.detectAndCompute(img2,None)
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(des1,des2, k=2)
	#matches = sorted(matches, key = lambda x:x.distance)

	good = []
	for m,n in matches:
	    if m.distance < 0.8*n.distance:
	        good.append([m])

	img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)

	return img3
"""
"""
def detection(frame):

	MIN_MATCH_COUNT = 5

	img1 = cv2.imread('checker.jpg',0)          # queryImage

	#img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	img2 = frame

	orb = cv2.ORB_create()
	kp1, des1 = orb.detectAndCompute(img1,None)
	kp2, des2 = orb.detectAndCompute(img2,None)
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	matches = bf.match(des1,des2)
	matches = sorted(matches, key = lambda x:x.distance)

	img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:MIN_MATCH_COUNT], None, flags=2)


	return img3

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

	#blur = cv2.GaussianBlur(img,(5,5),0)
	 
	# Set threshold and maxValue
	thresh = 130	
	maxValue = 220
	 
	# Basic threshold example
	th, dst = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY);

	return dst
"""


def detection(img):
	# Image preprocessing and thresholding
	imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	thresh = imgray.mean()	
	maxValue = 195
	th, dst = cv2.threshold(imgray, thresh, maxValue, cv2.THRESH_BINARY);

	# Image contour detection
	img, cnt, hiers = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	largest - max(cnt, key=cv2.contourArea)
	imgn = cv2.drawContours(img, largest, -1, (0,255,255), 3)

	return img


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


