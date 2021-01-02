import cv2
import numpy as np

img1 = cv2.imread('Img1.jpg')
img2 = cv2.imread('Img2.jpg')

prev_gray = cv2.resize(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)


prev_points = cv2.goodFeaturesToTrack(prev_gray, maxCorners = 200, qualityLevel = 0.01, minDistance = 30, blockSize = 3)

cur_gray = cv2.resize(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)

curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, cur_gray, prev_points, None)

assert prev_points.shape == curr_points.shape

idx = np.where(status==1)[0]
prev_points = prev_points[idx]
curr_points = curr_points[idx]

[transform, inlierPoints] = cv2.estimateAffinePartial2D(prev_points, curr_points)

cv2.imshow('Input', prev_gray)
cv2.waitKey()

warped = cv2.warpAffine(prev_gray, transform, (prev_gray.shape[1], prev_gray.shape[0]))
cv2.imshow('Warped', warped)
cv2.waitKey()

print(sum(transform[0]))
print(sum(transform[1]))
