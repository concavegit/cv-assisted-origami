import numpy as np
import cv2


def is_contour_bad(img, c):
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)

    area = cv2.contourArea(c)
    if area < (img.shape[0] * img.shape[1]) / 12:
        return True
    elif area > (img.shape[0] * img.shape[1]) / 2:
        return True
    elif len(approx) < 6:
        return False
    else:
        return True


def detection(img, REF):

    REFb = REF
    ref_ret, ref_thresh = cv2.threshold(REF, 127, 255, 0)
    ref_img, ref_conts, ref_hiers = cv2.findContours(ref_thresh, 2, 1)

    mask_off = REFb

    imgb = img
    # Research adaptive thresholding

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = imgray.mean() + 100
    maxValue = 180
    ret, thresh = cv2.threshold(imgray, thresh, maxValue, 0)

    #thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,17,9)

    img, cnt, hiers = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = []

    for c in cnt:
        if not is_contour_bad(img, c):
            cnts.append(c)

    lowest_cnt = cnt[0]
    lowest_ev = 8

    best_thot = 0
    instruction_cnt = ref_conts[0]
    bat = instruction_cnt
    batc = instruction_cnt

    OR_space = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    for goodcnt in cnts:
        approx = cv2.approxPolyDP(
            goodcnt, 0.03 * cv2.arcLength(goodcnt, True), True)
        if len(approx) < lowest_ev:
            lowest_ev = len(approx)
            lowest_cnt = goodcnt
            batc = approx

        for rc in ref_conts:
            approx_ref = cv2.approxPolyDP(
                rc, 0.02 * cv2.arcLength(rc, True), True)
            thot = cv2.matchShapes(approx_ref, lowest_cnt, 1, 0.0)

            if int(len(approx_ref)) == int(len(approx)):
                if cv2.contourArea(rc) < img.shape[0] * img.shape[1] and thot > 0:
                    instruction_cnt = approx_ref
                    bat = approx_ref

    # Translate selected instruction shape from shape collection to OR spaces

            cv2.drawContours(OR_space, [instruction_cnt], -1, (0, 0, 255), -1)

    # Transform the instruction shape space by the homographic perspective transform
    # TODO: Transform fold instructions/geometry

    delevated = OR_space
    mask_off = cv2.copyMakeBorder(
        mask_off, 0, img.shape[0] - mask_off.shape[0], 0, img.shape[1] - mask_off.shape[1], cv2.BORDER_CONSTANT, value=0)

    try:
        if batc is not None and bat is not None:
            H, mask = cv2.findHomography(bat, batc)
        if not np.isnan(H[0, 0]):
            mask_off = cv2.warpPerspective(
                mask_off, H, (img.shape[1], img.shape[0]))
            delevated = cv2.warpPerspective(
                OR_space, H, (img.shape[1], img.shape[0]))

    except cv2.error:
        print("none")

    cv2.drawContours(imgb, [lowest_cnt], 0, (0, 255, 0), -1)

    res, overlayMask = cv2.threshold(mask_off, 10, 1, cv2.THRESH_BINARY_INV)
    h, w = overlayMask.shape
    overlayMask = np.repeat(overlayMask, 3).reshape((h, w, 3))
    mask_off = np.repeat(mask_off, 3).reshape((h, w, 3))

    imgb *= overlayMask
    imgb += mask_off

    return imgb


def run(imgname):
    vc = cv2.VideoCapture(0)
    img1 = cv2.imread('AR_instructions/' + str(imgname), 0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, img = vc.read()
        img = detection(img, img1)
        cv2.namedWindow("feed", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            "feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("feed", img)
        key = cv2.waitKey(20)

        if key == 27:
            break

    cv2.destroyWindow("feed")
