import numpy as np
import cv2


cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

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
