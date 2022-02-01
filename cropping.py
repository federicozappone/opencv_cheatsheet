import numpy as np
import cv2


image = cv2.imread("test_image.jpg")

x1 = 20
y1 = 10

x2 = 100
y2 = 100

crop = image[y1:y2, x1:x2].copy()

cv2.imshow("image", image)
cv2.imshow("crop", crop)

cv2.waitKey(0)
cv2.destroyAllWindows()