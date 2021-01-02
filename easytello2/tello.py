import socket
import threading
import time
import cv2
from easytello2.stats import Stats
import numpy as np
import queue

class Tello:
    def __init__(self, tello_ip: str='192.168.10.1', debug: bool=True):
        # Opening local UDP port on 8889 for Tello communication
        print('hi')
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.local_ip, self.local_port))

        # Setting Tello ip and port info
        self.tello_ip = tello_ip
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.log = []

        # Intializing response thread
        self.q = queue.Queue()
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # easyTello runtime options
        self.face_rec = False
        self.stream_state = False
        self.last_frame = None
        self.MAX_TIME_OUT = 15.0
        self.debug = debug
        # Setting Tello to command mode
        self.command()

    def send_command(self, command: str, query: bool =False):
        # New log entry created for the outbound command
        self.log.append(Stats(command, len(self.log)))

        # Sending command to Tello
        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        # Displaying conformation message (if 'debug' os True)
        if self.debug is True:
            print('Sending command: {}'.format(command))

        # Checking whether the command has timed out or not (based on value in 'MAX_TIME_OUT')
        start = time.time()
        while not self.log[-1].got_response():  # Runs while no repsonse has been received in log
            now = time.time()
            difference = now - start
            if difference > self.MAX_TIME_OUT:
                print('Connection timed out!')
                break
        # Prints out Tello response (if 'debug' is True)
        if self.debug is True and query is False:
            print('Response: {}'.format(self.log[-1].get_response()))

    def _receive_thread(self):
        while True:
            # Checking for Tello response, throws socket error
            try:
                self.response, ip = self.socket.recvfrom(1024)
                self.log[-1].add_response(self.response)
            except socket.error as exc:
                print('Socket error: {}'.format(exc))

    def _video_thread(self):
        #Loads face recognition model
        face_cascade = cv2.CascadeClassifier('easytello2\haarcascade_frontalface_default.xml')
        assert (not face_cascade.empty()), "Face Cascade failed to load"

        # Creating stream capture object
        cap = cv2.VideoCapture('udp://'+self.tello_ip+':11111')
        out = cv2.VideoWriter('testvid.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (960, 720))

        # Runs while 'stream_state' is True
        while self.stream_state:
            ret, self.last_frame = cap.read()
            gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)


            if ret:
                #Facial recognition
                if self.face_rec:
                    gray_small = cv2.resize(gray, (240, 180))
                    faces = face_cascade.detectMultiScale(gray_small, 1.1, 4)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(self.last_frame, (x*4, y*4), ((x+w)*4, (y+h)*4), (255, 0, 0), 2)


                prev_gray = cv2.resize(gray, (0,0), fx = 0.125, fy = 0.125)
                prev_points = cv2.goodFeaturesToTrack(prev_gray, maxCorners = 200, qualityLevel = 0.01, minDistance = 30, blockSize = 3)

                if not self.q.empty():
                    curr = self.q.get()

                    cur_gray = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY), (0,0), fx = 0.125, fy = 0.125)
                    curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, cur_gray, prev_points, None)

                    assert prev_points.shape == curr_points.shape

                    idx = np.where(status==1)[0]
                    prev_points = prev_points[idx]
                    curr_points = curr_points[idx]
                    [transform, inlierPoints] = cv2.estimateAffinePartial2D(prev_points, curr_points)
                    t = np.matrix.round(transform, 4)
                    print(t)

                else:
                    pass

                self.q.put(self.last_frame)

                cv2.imshow('DJI Tello', self.last_frame)
                #out.write(self.last_frame)

            # Video Stream is closed if escape key is pressed
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def wait(self, delay: float):
        # Displaying wait message (if 'debug' is True)
        if self.debug is True:
            print('Waiting {} seconds...'.format(delay))
        # Log entry for delay added
        self.log.append(Stats('wait', len(self.log)))
        # Delay is activated
        time.sleep(delay)

    def get_log(self):
        return self.log

    def close(self):
        self.socket.close()

    # Controll Commands
    def command(self):
        self.send_command('command')

    def takeoff(self):
        self.send_command('takeoff')

    def land(self):
        self.send_command('land')

    def streamon(self):
        self.send_command('streamon')
        self.stream_state = True
        self.video_thread = threading.Thread(target=self._video_thread)
        self.video_thread.daemon = True
        self.video_thread.start()

    def streamoff(self):
        self.stream_state = False
        self.send_command('streamoff')

    def emergency(self):
        self.send_command('emergency')

    # Movement Commands
    def up(self, dist: int):
        self.send_command('up {}'.format(dist))

    def down(self, dist: int):
        self.send_command('down {}'.format(dist))

    def left(self, dist: int):
        self.send_command('left {}'.format(dist))

    def right(self, dist: int):
        self.send_command('right {}'.format(dist))

    def forward(self, dist: int):
        self.send_command('forward {}'.format(dist))

    def back(self, dist: int):
        self.send_command('back {}'.format(dist))

    def cw(self, degr: int):
        self.send_command('cw {}'.format(degr))

    def ccw(self, degr: int):
        self.send_command('ccw {}'.format(degr))

    def flip(self, direc: str):
        self.send_command('flip {}'.format(direc))

    def go(self, x: int, y: int, z: int, speed: int):
        self.send_command('go {} {} {} {}'.format(x, y, z, speed))

    def curve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, speed: int):
        self.send_command('curve {} {} {} {} {} {} {}'.format(x1, y1, z1, x2, y2, z2, speed))

    # Set Commands
    def set_speed(self, speed: int):
        self.send_command('speed {}'.format(speed))

    def rc_control(self, a: int, b: int, c: int, d: int):
        self.send_command('rc {} {} {} {}'.format(a, b, c, d))

    def set_wifi(self, ssid: str, passwrd: str):
        self.send_command('wifi {} {}'.format(ssid, passwrd))

    # Read Commands
    def get_speed(self):
        self.send_command('speed?', True)
        return self.log[-1].get_response()

    def get_battery(self):
        self.send_command('battery?', True)
        return self.log[-1].get_response()

    def get_time(self):
        self.send_command('time?', True)
        return self.log[-1].get_response()

    def get_height(self):
        self.send_command('height?', True)
        return self.log[-1].get_response()

    def get_temp(self):
        self.send_command('temp?', True)
        return self.log[-1].get_response()

    def get_attitude(self):
        self.send_command('attitude?', True)
        return self.log[-1].get_response()

    def get_baro(self):
        self.send_command('baro?', True)
        return self.log[-1].get_response()

    def get_acceleration(self):
        self.send_command('acceleration?', True)
        return self.log[-1].get_response()

    def get_tof(self):
        self.send_command('tof?', True)
        return self.log[-1].get_response()

    def get_wifi(self):
        self.send_command('wifi?', True)
        return self.log[-1].get_response()
