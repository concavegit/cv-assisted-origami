import cv2
import numpy as np


img = cv2.imread("sample/step02.png", -1)
alpha = img[:, :, -1]
mask = np.array(alpha == 0, dtype=np.uint8)
color = img[:, :, :-1]
new_img = cv2.bitwise_not(color, np.array(color), mask=mask)

gray = np.array(cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
                > 2, dtype=np.uint8) * 255
# dst = cv2.cornerHarris(gray, 2, 3, 0.04)
# ret, dst = cv2.threshold(dst, .1 * dst.max(), 255, 0)
# dst = np.uint8(dst)

corners = np.int0(cv2.goodFeaturesToTrack(gray, 100, 0.01, 10))[:, 0, :]


print(corners)
cv2.imshow('test', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
