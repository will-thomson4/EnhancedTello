import cv2
import numpy as np
import queue

cap = cv2.VideoCapture('stabiliserTest.avi')
q = queue.Queue()
frame_count = 0

while True:
    ret, img1 = cap.read()

    prev_gray = cv2.resize(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
    prev_points = cv2.goodFeaturesToTrack(prev_gray, maxCorners = 200, qualityLevel = 0.01, minDistance = 30, blockSize = 3)

    if not q.empty():
        img2 = q.get()
        cur_gray = cv2.resize(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
        curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, cur_gray, prev_points, None)

        assert prev_points.shape == curr_points.shape

        idx = np.where(status==1)[0]
        prev_points = prev_points[idx]
        curr_points = curr_points[idx]

        [transform, inlierPoints] = cv2.estimateAffinePartial2D(prev_points, curr_points)

        if sum(transform[0]) > 1:
            frame_count += 1
        else:
            frame_count -= 1
        print(frame_count)

    q.put(img1)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

#print(sum(transform[0]))
#print(sum(transform[1]))
