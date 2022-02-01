import sys
import numpy as np

from sensor_msgs.msg import Image


def imgmsg_to_cv2(img_msg):
    if img_msg.encoding != "bgr8":
        rospy.logerr("imgmsg_to_cv2 has been hardcoded to the 'bgr8' encoding.  \
                     Change the code if you're actually trying to implement a new camera")

    dtype = np.dtype("uint8")
    dtype = dtype.newbyteorder('>' if img_msg.is_bigendian else '<')

    image_opencv = np.ndarray(shape=(img_msg.height, img_msg.width, 3),
                              dtype=dtype, buffer=img_msg.data)

    if img_msg.is_bigendian == (sys.byteorder == "little"):
        image_opencv = image_opencv.byteswap().newbyteorder()

    return image_opencv


def cv2_to_imgmsg(cv_image):
    img_msg = Image()

    img_msg.height = cv_image.shape[0]
    img_msg.width = cv_image.shape[1]
    img_msg.encoding = "bgr8"
    img_msg.is_bigendian = 0
    img_msg.data = cv_image.tostring()
    img_msg.step = len(img_msg.data) // img_msg.height

    return img_msg
