import cv2
import numpy as np
import queue

q = queue.Queue()

cap = cv2.VideoCapture('testvid.mp4')

while cap.isOpened():
    ret, last_frame = cap.read()
    gray = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)

    if ret:

        prev_gray = cv2.resize(gray, (0,0), fx = 0.125, fy = 0.125)
        prev_points = cv2.goodFeaturesToTrack(prev_gray, maxCorners = 200, qualityLevel = 0.01, minDistance = 30, blockSize = 3)

        if not q.empty():
            curr = q.get()

            cur_gray = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
            curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, cur_gray, prev_points, None)

            assert prev_points.shape == curr_points.shape

            idx = np.where(status==1)[0]
            prev_points = prev_points[idx]
            curr_points = curr_points[idx]
            [transform, inlierPoints] = cv2.estimateAffinePartial2D(prev_points, curr_points)
            t = np.matrix.round(transform, 4)

            if sum(t[0]) > 1:
                print("Right")
            else:
                print("Left")

        else:
            pass

        q.put(last_frame)

        cv2.imshow('Vid Test', last_frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
