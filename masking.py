import cv2
import numpy as np


image = cv2.imread("test_image.jpg")

cv2.imshow("image", image)

mask = np.zeros(image.shape[:2], dtype="uint8")
cv2.rectangle(mask, (0, 90), (290, 450), 255, -1)

cv2.imshow("mask", mask)

masked = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow("masked", masked)

cv2.waitKey(0)
cv2.destroyAllWindows()