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
def around(x, base=5):
	return int(base * round(float(x)/base))

def detection(img):
	# Image preprocessing and thresholding
	canvas = np.zeros((img.shape[0], img.shape[1], 3), dtype = "uint8")

	imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	thresh = imgray.mean()
	maxValue = 180
	ret, thresh = cv2.threshold(imgray, thresh, maxValue, 0);

	# Image contour detection
	#img, cnt, hiers = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#largest = max(cnt, key=cv2.contourArea)
	#imgn = cv2.drawContours(img, cnt, 2, (0,255,0), 3)

	gray = cv2.bilateralFilter(thresh, 9, 17, 17)
	edges = cv2.Canny(gray, 100, 200, apertureSize = 3)
	"""
	corners = cv2.goodFeaturesToTrack(edged, 4, 0.01, 10)
	corners = np.int0(corners)

	for corner in corners:
	    x,y = corner.ravel()
	    cv2.circle(edged,(x,y),3,255,-1)

		im2,contours,hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		if len(contours) != 0:
			c = max(contours, key = cv2.contourArea)
			cv2.drawContours(edges, c, -1, 255, 3)

	"""

	minLineLength = 5
	maxLineGap = 10


	#dst = cv2.cornerHarris(edges,30,17,0.06)
	#dst = cv2.dilate(dst,None)

	# Threshold for an optimal value, it may vary depending on the image.
	#canvas[dst>0.5*dst.max()]=[255,255,255]

	lines = cv2.HoughLines(edges,1,np.pi/360,6,minLineLength,maxLineGap)

	# We need to filter these lines somehow to reduce random/arbitrary data
	theta_bins = dict()

	for line in lines[:50]:
		for rho,theta in line:
			nearest = str(around(int(np.degrees(theta)), base=10))
			if nearest in theta_bins:
				theta_bins[nearest] += 1
			else:
				theta_bins[nearest] = 1

	common_theta_base = sorted(theta_bins, key=theta_bins.get, reverse=True)
	print(common_theta_base)
	print(theta_bins)

	for line in lines[:40]:
		for rho,theta in line:
			nearest = around(int(np.degrees(theta)), base=5)
			if nearest in common_theta_base:
				a = np.cos(np.radians(nearest))
				b = np.sin(np.radians(nearest))
				x0 = a*rho
				y0 = b*rho
				x1 = int(x0 + 1000*(-b))
				y1 = int(y0 + 1000*(a))
				x2 = int(x0 - 1000*(-b))
				y2 = int(y0 - 1000*(a))
				cv2.line(canvas,(x1,y1),(x2,y2),(255,255,255),2)



	return gray


	#dst = cv2.cornerHarris(canvas,10,17,0.06)
	#dst = cv2.dilate(dst,None)

	# Threshold for an optimal value, it may vary depending on the image.
	#canvas[dst>0.5*dst.max()]=[0,0,255]


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
