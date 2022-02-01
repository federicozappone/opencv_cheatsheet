import os
import cv2
import subprocess as sp
import numpy as np
import urllib.request
import shutil

# camera resolution
image_width = 1920
image_height = 1080


ffmpeg_bin = "/usr/bin/ffmpeg"
grabber = "v4l2"
device = "/dev/video0"


# grab desktop and pipe
ffmpeg_cmd = [ffmpeg_bin,
            "-f", grabber,
            "-video_size", f"{image_width}x{image_height}",
            "-i", device,               # input device
            "-framerate", "25",         # fps
            "-pix_fmt", "bgr24",        # opencv requires bgr24 pixel format.
            "-vcodec", "rawvideo",      # video codec
            "-an","-sn",                # disable audio processing
            "-f", "image2pipe", "-"]    # write to pipe

# open pipe
pipe = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE, bufsize=10)


while True:
    raw_image = pipe.stdout.read(image_width * image_height * 3)

    # convert read bytes to np
    image =  np.frombuffer(raw_image, dtype=np.uint8)
    image = image.reshape((image_height, image_width, 3))

    cv2.imshow("camera", image)

    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        break

pipe.stdout.flush()
cv2.destroyAllWindows()
