import cv2
import numpy as np


def auto_white_balance(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

    return result


image = cv2.imread("test_image.jpg")

balanced = auto_white_balance(image)

cv2.imshow("image", image)
cv2.imshow("balanced", balanced)

cv2.waitKey(0)
cv2.destroyAllWindows()
