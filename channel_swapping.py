import cv2
import numpy as np

image_bgr = cv2.imread("test_image.jpg")

image_rgb = image_bgr[:, :, [2, 1, 0]]
image_bgr = image_rgb[:, :, ::-1]
