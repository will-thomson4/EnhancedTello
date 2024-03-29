import cv2

class Facial_Rec:
    def __init__(self):
        self.model = cv2.CascadeClassifier('easytello2\EnhancedFeatures\FacialRecognition\haarcascade_frontalface_default.xml')
        self.resize_factor = 4

    def scan_faces(self, input_img):
        #Resize input image
        resized = cv2.resize(cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY), (0,0), fx = 1/self.resize_factor, fy = 1/self.resize_factor)
        #Detect faces
        faces = self.model.detectMultiScale(resized, 1.3, 4)
        #Draw box around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(input_img, (x*self.resize_factor, y*self.resize_factor), ((x+w)*self.resize_factor, (y+h)*self.resize_factor), (255, 0, 0), 2)
