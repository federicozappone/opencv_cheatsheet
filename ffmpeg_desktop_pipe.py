import os
import cv2
import subprocess as sp
import numpy as np
import urllib.request
import shutil


# download ffmpeg binaries for windows
if not os.path.isfile("bin/ffmpeg.exe") and os.name == "nt":
    print("downloading ffmpeg for windows, please wait")

    # check if we already downloaded the archive
    if not os.path.isfile("ffmpeg.zip"):
        ffmpeg_bin_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-12-09-12-21/ffmpeg-N-104826-g408b974796-win64-gpl.zip"
        urllib.request.urlretrieve(ffmpeg_bin_url, "ffmpeg.zip")

    # unpack archive and rename the folder to ffmpeg
    print("unpacking ffmpeg archive")
    shutil.unpack_archive("ffmpeg.zip", format="zip")
    shutil.move("ffmpeg-N-104826-g408b974796-win64-gpl", "ffmpeg")

# desktop resolution
image_width = 1920
image_height = 1080

if os.name == "nt": # windows
    ffmpeg_bin = "ffmpeg/bin/ffmpeg.exe"
    grabber = "gdigrab"
    device = "desktop"
else: # linux
    ffmpeg_bin = "/usr/bin/ffmpeg"
    grabber = "x11grab"
    device = ":1"


# grab desktop and pipe
ffmpeg_cmd = [ffmpeg_bin,
            "-f", grabber,
            "-video_size", f"{image_width}x{image_height}",
            "-i", device,               # input device
            "-r", "30",                 # fps
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

    cv2.imshow("desktop", image)

    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        break

pipe.stdout.flush()
cv2.destroyAllWindows()
