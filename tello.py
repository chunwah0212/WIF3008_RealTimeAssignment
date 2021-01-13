import socket
import threading
import time
import math
import libh264decoder
import numpy as np


class Tello:

    def __init__(self, command_timeout=.3):
        # stream video
        self.decoder = libh264decoder.H264Decoder()
        self.frame = None  # numpy array BGR -- current camera output frame
        self.is_freeze = False  # freeze current camera output
        self.last_frame = None
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.command_timeout = command_timeout
        self.abort_flag = False
        self.response = None

        # IP and port of Tello
        self.tello_address = ('192.168.10.1', 8889)

        # IP and port of local computer
        self.local_address = ('', 9000)

        # Create a UDP connection that we'll send the command to
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.local_video_port = 11111  # port for receiving video stream

        # Bind to the local address and port
        self.sock.bind(self.local_address)

        # receive video
        self.sock.sendto(b'command', self.tello_address)
        print ('sent: command')
        self.sock.sendto(b'streamon', self.tello_address)
        print ('sent: streamon')

        self.socket_video.bind((local_ip, self.local_video_port))

        # Create and start a listening thread that runs in the background
        # This utilizes our receive functions and will continuously monitor for incoming messages
        self.receiveThread = threading.Thread(target=self.receive)
        self.receiveThread.daemon = True
        self.receiveThread.start()

        self.event = threading.Event()

        # # thread for receiving video
        self.receive_video_thread = threading.Thread(target=self._receive_video_thread)
        self.receive_video_thread.daemon = True
        self.receive_video_thread.start()

        # default value
        self.x = 0
        self.y = 0
        self.angle = 0
        self.distance = 20
        self.rotateAngle = 15
        self.manual = True
        self.takeOff = False
        self.landed = True
        self.height = 0

        # enter SDK mode during init
        self.send('Command', 3)

    # Send the message to Tello and allow for a delay in seconds
    def send(self, message, delay):
        # Try to send the message otherwise print the exception
        try:
            print("Sending message: " + message)
            self.sock.sendto(message.encode(), self.tello_address)
        except Exception as e:
            print("Error sending: " + str(e))

        # Delay for a user-defined period of time
        time.sleep(delay)

    def send_route(self, message):
        # Try to send the message otherwise print the exception
        try:
            print("Sending message: " + message)
            self.sock.sendto(message.encode(), self.tello_address)
        except Exception as e:
            print("Error sending: " + str(e))

    # Receive the message from Tello
    def receive(self):
        # Continuously loop and listen for incoming messages
        while True:
            # Try to receive the message otherwise print the exception
            try:
                response, ip_address = self.sock.recvfrom(128)
                print("Received message: " + response.decode(encoding='utf-8'))
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                self.sock.close()
                print("Error receiving: " + str(e))
            break

    def update_location(self, command, value):
        # 0 degrees = North, 90 = East, 180 = South, 270 = West
        # if angle anticlockwise turn to cw
        if command.lower() == "ccw":
            rotated_angle = 360 - value
            # update angle
            self.angle += rotated_angle
            if self.angle >= 360:
                self.angle = self.angle - 360

        if command.lower() == "cw":
            # update angle
            self.angle += value
            if self.angle > 360:
                self.angle = self.angle - 360

        if command.lower() == "forward":
            # update location
            dy = value * math.cos(math.radians(self.angle))  # change in y
            dx = value * math.sin(math.radians(self.angle))  # change in x
            self.y += round(dy)
            self.x += round(dx)

        if command.lower() == "back":
            # update location
            dy = value * math.cos(math.radians(self.angle + 180))  # change in y
            dx = value * math.sin(math.radians(self.angle + 180))  # change in x
            self.y += round(dy)
            self.x += round(dx)

        if command.lower() == "left":
            dy = value * math.cos(math.radians(self.angle + 270))  # change in y
            dx = value * math.sin(math.radians(self.angle + 270))  # change in x
            self.y += round(dy)
            self.x += round(dx)

        if command.lower() == "right":
            dy = value * math.cos(math.radians(self.angle + 90))  # change in y
            dx = value * math.sin(math.radians(self.angle + 90))  # change in x
            self.y += round(dy)
            self.x += round(dx)

        print("Current location: X = {} , Y = {}, Current direction: {}\n".format(self.x, self.y, self.angle))

    def takeoff(self):
        if not self.takeOff:
            self.send('takeoff', 3)
            self.takeOff = True
            self.landed = False
            self.height = self.height + 30
            print("Drone take off")
        else:
            print("Drone already take off!")

    def land(self):
        if not self.landed:
            self.send('land', 3)
            self.landed = True
            self.takeOff = False
            print("Drone landed")
        else:
            print("Drone already landed!")

    def rotate_cw(self):
        if self.landed:
            print("Please take off the drone to perform rotation.")
        else:
            self.send('cw ' + str(self.rotateAngle), 4)
            self.update_location('cw', self.rotateAngle)

    def rotate_ccw(self):
        if self.landed:
            print("Please take off the drone to perform rotation.")
        else:
            self.send('ccw ' + str(self.rotateAngle), 4)
            self.update_location('ccw', self.rotateAngle)

    def move_up(self):
        self.send('up ' + str(self.distance), 4)
        self.height = self.height + self.distance
        self.takeOff = True
        self.landed = False
        print("Drone move up by " + str(self.distance))

    def move_down(self):
        if self.landed:
            print ("Drone already landed.")
        else:
            self.send('down ' + str(self.distance), 4)
            if self.height - self.distance <= 0:
                self.height = 0
                self.takeOff = False
                self.landed = True
            else:
                self.height = self.height - self.distance
            print("Drone move down by " + str(self.distance))

    def move_forward(self):
        if self.landed:
            print("Please take off the drone to perform movement.")
        else:
            self.send('forward ' + str(self.distance), 4)
            self.update_location('forward', self.distance)

    def move_backward(self):
        if self.landed:
            print("Please take off the drone to perform movement.")
        else:
            self.send('back ' + str(self.distance), 4)
            self.update_location('back', self.distance)

    def move_left(self):
        if self.landed:
            print("Please take off the drone to perform movement.")
        else:
            self.send('left ' + str(self.distance), 4)
            self.update_location('left', self.distance)

    def move_right(self):
        if self.landed:
            print("Please take off the drone to perform movement.")
        else:
            self.send('right ' + str(self.distance), 4)
            self.update_location('right', self.distance)

    def set_distance(self, distance):
        self.distance = distance
        print("Moving distance changed to : " + str(self.distance))

    def set_degree(self, rotate_angle):
        self.rotateAngle = rotate_angle
        print("Rotation angle changed to : " + str(self.rotateAngle))

    def stop(self):
        self.manual = True  # stop the pre-plan
        self.send('stop', 1)
        print("Drone stop and hovers in the air")

    def back_base(self):
        # turn to default angle, 0
        self.send("ccw " + str(self.angle), 4)
        self.angle = 0
        print("Drone rotated to default direction: " + str(self.angle))

        # move back to (0,0) origin
        if self.x >= 0:
            # if x is positive move left
            self.send("left " + str(self.x), 5)
        else:
            # if x is negative move right
            self.send("right " + str(abs(self.x)), 5)

        self.x = 0
        print("Drone moved to original X-axis position, X = " + str(self.x))

        if self.y >= 0:
            # if y is positive move backward
            self.send("back " + str(self.y), 5)
        else:
            # if y is negative move forward
            self.send("forward " + str(abs(self.y)), 5)

        self.y = 0
        print("Drone moved to original Y-axis position, Y = " + str(self.y))
        print("Drone backed to base!\n")

    def _receive_video_thread(self):
        """
        Listens for video streaming (raw h264) from the Tello.
        Runs as a thread, sets self.frame to the most recent frame Tello captured.
        """
        packet_data = ""
        print("Try to get video streaming\n")
        while True:
            try:
                res_string, ip = self.socket_video.recvfrom(2048)
                packet_data += res_string
                # end of frame
                if len(res_string) != 1460:
                    for frame in self._h264_decode(packet_data):
                        self.frame = frame
                    packet_data = ""

            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)

    def _h264_decode(self, packet_data):
        """
        decode raw h264 format data from Tello

        :param packet_data: raw h264 data array

        :return: a list of decoded frame
        """
        res_frame_list = []
        frames = self.decoder.decode(packet_data)
        for framedata in frames:
            (frame, w, h, ls) = framedata
            if frame is not None:
                # print 'frame size %i bytes, w %i, h %i, linesize %i' % (len(frame), w, h, ls)

                frame = np.fromstring(frame, dtype=np.ubyte, count=len(frame), sep='')
                frame = (frame.reshape((h, ls / 3, 3)))
                frame = frame[:, :w, :]
                res_frame_list.append(frame)

        return res_frame_list

    def read(self):
        """Return the last frame from camera."""
        if self.is_freeze:
            return self.last_frame
        else:
            return self.frame

    def video_freeze(self, is_freeze=True):
        """Pause video output -- set is_freeze to True"""
        self.is_freeze = is_freeze
        if is_freeze:
            self.last_frame = self.frame

    def send_command(self, command):
        """
        Send a command to the Tello and wait for a response.
        :param command: Command to send.
        :return (str): Response from Tello.
        """

        # print (">> send cmd: {}".format(command))
        self.abort_flag = False
        timer = threading.Timer(self.command_timeout, self.set_abort_flag)

        self.sock.sendto(command.encode('utf-8'), self.tello_address)

        timer.start()
        while self.response is None:
            if self.abort_flag is True:
                break
        timer.cancel()

        if self.response is None:
            response = 'none_response'
        else:
            response = self.response.decode('utf-8')

        self.response = None

        return response

    def set_abort_flag(self):
        """
        Sets self.abort_flag to True.
        Used by the timer in Tello.send_command() to indicate to that a response

        timeout has occurred.
        """

        self.abort_flag = True

    def __del__(self):
        """Closes the local socket."""

        self.sock.close()
        self.socket_video.close()