from easytello2 import tello
import time

my_drone = tello.Tello()
#my_drone.streamon()
my_drone.takeoff()
my_drone.wait(2)
my_drone.forward(200)

my_drone.wait(2)

my_drone.cw(180)

my_drone.wait(2)

my_drone.up(100)
my_drone.wait(2)
my_drone.forward(200)

my_drone.land()
#my_drone.streamoff()
