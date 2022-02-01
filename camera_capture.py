import numpy as np
import cv2


cap = cv2.VideoCapture(0)

# set the maximum resolution
cap.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("cannot acquire frame")
        continue

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
