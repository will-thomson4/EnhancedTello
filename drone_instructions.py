from easytello2 import tello
import time

my_drone = tello.Tello()
my_drone.face_rec = False

my_drone.streamon()
print("after streamon cmd")
my_drone.wait(30)

my_drone.streamoff()
