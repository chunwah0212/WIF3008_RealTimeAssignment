import math


class Sweep:
    # first route
    polygon_route = [[1, "ccw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40], [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]

    # second route
    triangle_route = [[1, "ccw", 120, "forward", 100], [2, "ccw", 120, "forward", 100], [0, "ccw", 120, "forward", 100]]

    current_route = polygon_route
    step = 0
    checkpoint_x = 0
    checkpoint_y = 0
    checkpoint_angle = 0

    # default out from base
    # frombase = ["forward", 50, "ccw", 90]
    # tobase = ["ccw", 120, "forward", 50]

    def __init__(self, tello):
        self.tello = tello

    # def update_location(self, direction, angle, distance):  # defines function
    #     # 0 degrees = North, 90 = East, 180 = South, 270 = West
    #     # if angle anticlockwise turn to cw
    #     if direction.lower() == "ccw":
    #         angle = 360 - angle
    #
    #     # update angle
    #     self.tello.angle += angle
    #     if self.tello.angle > 360:
    #         self.tello.angle = self.tello.angle - 360
    #
    #     # update location
    #     dy = distance * math.cos(math.radians(self.tello.angle))  # change in y
    #     dx = distance * math.sin(math.radians(self.tello.angle))  # change in x
    #     self.tello.y += round(dy)
    #     self.tello.x += round(dx)

    def set_route(self, route):
        if route == 1:
            self.current_route = self.polygon_route
            print("Pre-plan Route set to Irregular Polygon route and route checkpoint is reset")
        elif route == 2:
            self.current_route = self.triangle_route
            print("Pre-plan Route set to Triangle route and route checkpoint is reset")

    def back_checkpoint(self):
        # turn to previous checkpoint angle
        diff = self.tello.angle - self.checkpoint_angle
        if diff <= 0:
            self.tello.send("cw " + str(abs(diff)), 4)
            self.tello.update_location("cw", abs(diff))

        if diff > 0:
            self.tello.send("ccw" + str(diff), 4)
            self.tello.update_location("ccw", diff)

        # find the distance to move back
        dx = abs(self.tello.x - self.checkpoint_x)
        distance_h = dx / (math.sin(math.radians(self.checkpoint_angle)))
        self.tello.send("forward " + str(distance_h), 5)
        self.tello.update_location("forward", distance_h)

        print("Drone back to previous checkpoint")

    # def out_base(self):
    #     self.tello.send(self.frombase[0] + " " + str(self.frombase[1]), 4)
    #     self.tello.send(self.frombase[2] + " " + str(self.frombase[3]), 4)

    def perform_sweep(self):
        self.tello.manual = False
        # get current location as checkpoint location if is a new sweep route
        if self.step == 0:
            self.checkpoint_x = self.tello.x
            self.checkpoint_y = self.tello.y
            self.checkpoint_angle = self.tello.angle

        # if not a new route, get back to previous checkpoint
        if self.step != 0:
            self.back_checkpoint()

        for self.step in range(len(self.current_route)):
            if not self.tello.manual: # each loop check whether is stop
                if self.step == len(self.current_route)-1:
                    print("Returning to Checkpoint 0. \n")

                self.tello.send(self.current_route[self.step][1] + " " + str(self.current_route[self.step][2]), 4)
                self.tello.update_location(self.current_route[self.step][1], self.current_route[self.step][2])
                self.tello.send(self.current_route[self.step][3] + " " + str(self.current_route[self.step][4]), 4)
                self.tello.update_location(self.current_route[self.step][3], self.current_route[self.step][4])
                # update checkpoint location
                self.checkpoint_x = self.tello.x
                self.checkpoint_y = self.tello.y
                self.checkpoint_angle = self.tello.angle
                print("Arrived at Checkpoint: " + str(self.current_route[self.step][0]) + "\n")
                self.step += 1

        if self.step == len(self.current_route):
            print("Complete sweep.")
