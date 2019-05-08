from __future__ import print_function
from imutils.video import VideoStream
from imutils.object_detection import non_max_suppression
import time
import numpy as np
import imutils
import cv2


print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

(H, W) = (None, None)

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=600)

    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow("heavy mathametics", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()
