import numpy as np
import cv2

def is_contour_bad(img, c):
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)
 
    area = cv2.contourArea(c)
    if area < 10000:
        return True
    elif area > (img.shape[0]*img.shape[1])/8:
        return True
    elif len(approx) < 8:
        return False
    else:
        return True
    
def detection(img):

    imgb = img

    # Research adaptive thresholding
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh = imgray.mean()
    maxValue = 180
    ret, thresh = cv2.threshold(imgray, thresh, maxValue, 0);

    img, cnt, hiers = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.ones(img.shape[:2], dtype="uint8") * 255

    cnts = []

    for c in cnt:
        if not is_contour_bad(img, c):
            cnts.append(c)

    lowest_cnt = cnt[0]
    lowest_ev = 8

    for goodcnt in cnts:
        approx = cv2.approxPolyDP(goodcnt,0.03*cv2.arcLength(goodcnt,True),True)
        if len(approx) < lowest_ev:
            lowest_ev = len(approx)
            lowest_cnt = goodcnt
        if len(approx)==3:
            print("triangle")
        elif len(approx)==4:
            print("square")
        elif len(approx)==5:
            print("pentagon")

    cv2.drawContours(imgb,[lowest_cnt],0,(0,255,0),-1)

    return imgb


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
