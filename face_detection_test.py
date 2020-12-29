import cv2

img = cv2.imread('test_pic.jpg')

face_cascade = cv2.CascadeClassifier('easytello2\haarcascade_frontalface_default.xml')
assert (not face_cascade.empty()), "Face Cascade failed to load"
print("Model Loaded")
#breakpoint()

gray = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (480, 360))
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
for (x, y, w, h) in faces:
    cv2.rectangle(gray, (x, y), ((x+w), (y+h)), (255, 0, 0), 2)

print(gray.shape)
cv2.imshow('DJI Tello', gray)
cv2.waitKey()
