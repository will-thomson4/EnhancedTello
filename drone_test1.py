from easytello2 import tello
import time

my_drone = tello.Tello()
my_drone.streamon()
my_drone.takeoff()

my_drone.cw(90)
my_drone.wait(10)

my_drone.land()
my_drone.streamoff()
