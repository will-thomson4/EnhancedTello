import cv2

class Facial_Rec:
    def __init__(self):
        self.model = cv2.CascadeClassifier('easytello2\haarcascade_frontalface_default.xml')
        self.resize_factor = 4

    def scan_faces(self, input_img, output_img):
        resized = cv2.resize(input_img, (0,0), fx = 1/self.resize_factor, fy = 1/self.resize_factor)
        faces = self.model.detectMultiScale(resized, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(output_img, (x*self.resize_factor, y*self.resize_factor), ((x+w)*self.resize_factor, (y+h)*self.resize_factor), (255, 0, 0), 2)
