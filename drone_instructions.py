from easytello2 import tello
import time

my_drone = tello.Tello()
my_drone.face_rec = False

my_drone.streamon()
my_drone.takeoff()


my_drone.land()
my_drone.streamoff()
