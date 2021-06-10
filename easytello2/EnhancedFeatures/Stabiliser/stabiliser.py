import cv2
import numpy as np
import queue

class Stabiliser:
    def __init__(self):
        #Frame queue
        self.q = queue.Queue()
        self.frame_count = 0
        self.movingLeft = False
        self.movingRight = False

    def stabilise(self, curr):
        #Formatting image and finding points in current frame
        current_frame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
        current_points = cv2.goodFeaturesToTrack(current_frame, maxCorners = 200, qualityLevel = 0.01, minDistance = 30, blockSize = 3)

        #Formatting image and finding points in previous frame
        if not self.q.empty():
            prev = self.q.get()
            previous_frame = cv2.resize(cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
            previous_points, status, err = cv2.calcOpticalFlowPyrLK(current_frame, previous_frame, current_points, None)

        #Sanity check
            assert previous_points.shape == current_points.shape

        #Creating affine matrix between both sets of points
            idx = np.where(status==1)[0]
            previous_points = previous_points[idx]
            current_points = current_points[idx]
            [transform, inlierPoints] = cv2.estimateAffinePartial2D(current_points, previous_points)

        #Adding a counter to measure movement of points to the left(-1) or right(+1)
            if sum(transform[0]) > 1:
                self.frame_count += 1
            else:
                self.frame_count -= 1

            if self.frame_count > 60:
                self.movingLeft = False
                self.movingRight = True
            if self.frame_count < -60:
                self.movingRight = False
                self.movingLeft = True
            print(self.frame_count)

        self.q.put(curr)
