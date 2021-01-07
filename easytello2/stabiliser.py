import cv2
import numpy as np
import queue

class Stabiliser:
    def __init__(self):
        self.q = queue.Queue()
        self.frame_count = 0

    def stabilise(self, curr):
        curr_gray = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
        curr_points = cv2.goodFeaturesToTrack(curr_gray, maxCorners = 200, qualityLevel = 0.01, minDistance = 30, blockSize = 3)

        #Finding points in previous frame
        if not self.q.empty():
            prev = self.q.get()
            prev_gray = cv2.resize(cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
            prev_points, status, err = cv2.calcOpticalFlowPyrLK(curr_gray, prev_gray, curr_points, None)

        #Sanity check
            assert prev_points.shape == curr_points.shape

        #Creating affine matrix between both sets of points
            idx = np.where(status==1)[0]
            prev_points = prev_points[idx]
            curr_points = curr_points[idx]
            [transform, inlierPoints] = cv2.estimateAffinePartial2D(curr_points, prev_points)

            if sum(transform[0]) > 1:
                self.frame_count += 1
            else:
                self.frame_count -= 1
            print(self.frame_count)

            if self.frame_count > 30:
                print("right")
            if self.frame_count < -30:
                print("left")


        self.q.put(curr)
