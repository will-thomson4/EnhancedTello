import cv2
import mediapipe as mp

class Action_rec:


    def detect_hands(self, img):
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        results = hands.process(img)
        print(results.multi_hand_landmarks)
