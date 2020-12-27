import socket
import threading
import time
import math


class Tello:

    def __init__(self):
        # IP and port of Tello
        self.tello_address = ('192.168.10.1', 8889)

        # IP and port of local computer
        self.local_address = ('', 9000)

        # Create a UDP connection that we'll send the command to
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the local address and port
        self.sock.bind(self.local_address)

        # Create and start a listening thread that runs in the background
        # This utilizes our receive functions and will continuously monitor for incoming messages
        self.receiveThread = threading.Thread(target=self.receive)
        self.receiveThread.daemon = True
        self.receiveThread.start()

        self.event = threading.Event()

        # default value
        self.x = 0
        self.y = 0
        self.angle = 0
        self.distance = 20
        self.rotateAngle = 15
        self.manual = True
        self.takeOff = False
        self.landed = True

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
        print("Drone move up by " + str(self.distance))

    def move_down(self):
        self.send('down ' + str(self.distance), 4)
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
