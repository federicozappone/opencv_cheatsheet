import os
import cv2
import subprocess as sp
import numpy as np
import urllib.request
import shutil

# camera resolution
image_width = 2560
image_height = 1440

username = "admin"
password = "csermac01"
codec = "h264"
stream = "main"

ffmpeg_bin = "/usr/bin/ffmpeg"
device = "rtsp://" + username + ":" + password + "@" + "192.168.1.118" + ":554//" + codec + "Preview_01_" + stream

# rtsp://admin:csermac01@192.168.1.118:554//h264Preview_01_main


# grab desktop and pipe
ffmpeg_cmd = [ffmpeg_bin,
            "-rtsp_transport", "tcp",
            "-max_delay", "500000",
            "-i", device,               # input device
            "-pix_fmt", "bgr24",        # opencv requires bgr24 pixel format.
            "-vcodec", "rawvideo",      # video codec
            "-an","-sn",                # disable audio processing
            "-f", "image2pipe", "-"]    # write to pipe

# open pipe
pipe = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE, bufsize=5)


while True:
    raw_image = pipe.stdout.read(image_width * image_height * 3)

    # convert read bytes to np
    image = np.frombuffer(raw_image, dtype=np.uint8)
    image = image.reshape((image_height, image_width, 3))

    cv2.imshow("camera", image)

    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        break

pipe.stdout.flush()
cv2.destroyAllWindows()
