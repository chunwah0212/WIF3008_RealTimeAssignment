import math


class Sweep:
    # default route
    sweep_route1 = [[1, "ccw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
                    [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]

    # second route //to do
    sweep_route2 = [[1, "ccw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 100],
                    [0, "ccw", 90, "forward", 80]]

    current_route = sweep_route1
    step = 0

    # default out from base
    frombase = ["forward", 50, "ccw", 90]
    # tobase = ["ccw", 120, "forward", 50]

    def __init__(self, tello):
        self.tello = tello

    def update_location(self, direction, angle, distance):  # defines function
        # 0 degrees = North, 90 = East, 180 = South, 270 = West
        # if angle anticlockwise turn to cw
        if direction.lower() == "ccw":
            angle = 360 - angle

        # update angle
        self.tello.angle += angle
        if self.tello.angle > 360:
            self.tello.angle = self.tello.angle - 360

        # update location
        dy = distance * math.cos(math.radians(self.tello.angle))  # change in y
        dx = distance * math.sin(math.radians(self.tello.angle))  # change in x
        self.tello.y += round(dy)
        self.tello.x += round(dx)

    def set_route(self, route):
        if route == 1:
            self.current_route = self.sweep_route1
        elif route == 2:
            self.current_route = self.sweep_route2

    def out_base(self):
        self.tello.send(self.frombase[0] + " " + str(self.frombase[1]), 4)
        self.tello.send(self.frombase[2] + " " + str(self.frombase[3]), 4)

    def back_base(self):
        # turn to default angle, 0
        self.tello.send("ccw " + str(self.tello.angle), 4)

        # move back to (0,0) origin
        if self.tello.x >= 0:
            # if x is positive move left
            self.tello.send("left " + str(self.tello.x), 5)
        else:
            # if x is negative move right
            self.tello.send("right " + str(abs(self.tello.x)), 5)

        if self.tello.y >= 0:
            # if y is positive move backward
            self.tello.send("back " + str(self.tello.y), 5)
        else:
            # if y is negative move forward
            self.tello.send("forward " + str(abs(self.tello.y)), 5)

    def perform_sweep(self):
        pass
