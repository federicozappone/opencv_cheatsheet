import cv2
import numpy as np
import apriltag


def draw_pose(overlay, camera_params, tag_size, pose, z_sign=1):

    opoints = np.array([
        -1, -1,  0,
         1, -1,  0,
         1,  1,  0,
        -1,  1,  0,
        -1, -1, -2*z_sign,
         1, -1, -2*z_sign,
         1,  1, -2*z_sign,
        -1,  1, -2*z_sign,
    ]).reshape(-1, 1, 3) * 0.5 * tag_size

    edges = np.array([
        0, 1,
        1, 2,
        2, 3,
        3, 0,
        0, 4,
        1, 5,
        2, 6,
        3, 7,
        4, 5,
        5, 6,
        6, 7,
        7, 4
    ]).reshape(-1, 2)

    fx, fy, cx, cy = camera_params

    K = np.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape(3, 3)

    rvec, jacobian = cv2.Rodrigues(pose[:3, :3])
    tvec = pose[:3, 3]

    dcoeffs = np.zeros(5)

    ipoints, _ = cv2.projectPoints(opoints, rvec, tvec, K, dcoeffs)

    ipoints = np.round(ipoints).astype(int)

    ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

    for i, j in edges:
        cv2.line(overlay, ipoints[i], ipoints[j], (0, 255, 0), 1, 16)


cap = cv2.VideoCapture(0)
detector = apriltag.Detector()

if not cap.isOpened():
    print("cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("cannot acquire frame")
        continue

    results = detector.detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    # loop over the apriltag detection results
    for detection in results:

        pose, e0, e1 = detector.detection_pose(detection, (640.0541384, 640.29663381, 324.47047202, 230.48852561), 3.0)

        draw_pose(frame, (640.0541384, 640.29663381, 324.47047202, 230.48852561), 3.0, pose)

        rvec, jacobian = cv2.Rodrigues(pose[:3, :3])
        tvec = pose[:3, 3]

        print("rvec=", rvec)
        print("tvec=", tvec)

    # display the resulting frame
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()
