import numpy as np
import cv2 as cv


img1 = cv.imread("image1.jpg")
img2 = cv.imread("image2.jpg")

# camera pose at location 1
c1pose = np.array([[0.9659258723258972, 0.2588190734386444, 0.0, 1.5529145002365112],
                 [ 0.08852133899927139, -0.3303661346435547, -0.9396926164627075, -0.10281121730804443],
                 [-0.24321036040782928, 0.9076734185218811, -0.342020183801651, 6.130080699920654],
                 [0, 0, 0, 1]], dtype=np.float64)

# camera pose at location 2
c2pose = np.array([[0.9659258723258972, -0.2588190734386444, 0.0, -1.5529145002365112],
                 [-0.08852133899927139, -0.3303661346435547, -0.9396926164627075, -0.10281121730804443],
                 [0.24321036040782928, 0.9076734185218811, -0.342020183801651, 6.130080699920654],
                 [0, 0, 0, 1]], dtype=np.float64)

# camera intrinsics
camera_matrix = np.array([[700.0, 0.0, 320.0], [0.0, 700.0, 240.0], [0, 0, 1]], dtype=np.float32)

# extract rotation
R1 = c1pose[0:3, 0:3]
R2 = c2pose[0:3, 0:3]

# compute rotation displacement
R2 = R2.transpose()
R_2to1 = np.dot(R1, R2)

# compute-homography
H = camera_matrix.dot(R_2to1).dot(np.linalg.inv(camera_matrix))
H = H / H[2][2]

# stitch
img_stitch = cv.warpPerspective(img2, H, (img2.shape[1] * 2, img2.shape[0]))
img_stitch[0:img1.shape[0], 0:img1.shape[1]] = img1

img_space = np.zeros((img1.shape[0], 50, 3), dtype=np.uint8)
img_compare = cv.hconcat([img1, img_space, img2])

cv.imshow("final", img_compare)
cv.imshow("panorama", img_stitch)

cv.waitKey(0)
cv2.destroyAllWindows()
