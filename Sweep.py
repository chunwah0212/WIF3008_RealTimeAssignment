import math
import time

class Sweep:

    def __init__(self, tello):
        self.tello = tello
        # first route
        self.polygon_route = [[1, "ccw", 90, "forward", 100], [2, "ccw", 90, "forward", 80],
                              [3, "ccw", 90, "forward", 40],
                              [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60],
                              [0, "ccw", 90, "forward", 40]]

        # second route
        self.triangle_route = [[1, "ccw", 120, "forward", 100], [2, "ccw", 120, "forward", 100],
                               [0, "ccw", 120, "forward", 100]]

        self.current_route = self.polygon_route
        self.route_name = "Polygon Route"
        self.step = 0
        self.checkpoint_x = 0
        self.checkpoint_y = 0
        self.checkpoint_angle = 0

    def set_route(self, route):
        if route == 1:
            self.current_route = self.polygon_route
            self.route_name = "Polygon Route"
            self.step = 0
            print("Pre-plan Route set to Irregular Polygon route and route step is reset to 0.")
        elif route == 2:
            self.current_route = self.triangle_route
            self.route_name = "Triangle Route"
            self.step = 0
            print("Pre-plan Route set to Triangle route and route step is reset to 0.")

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
        distance_h = 0
        if math.sin(math.radians(self.checkpoint_angle)) != 0:
            distance_h = dx / (math.sin(math.radians(self.checkpoint_angle)))

        self.tello.send("forward " + str(distance_h), 5)
        self.tello.update_location("forward", distance_h)

        print("Drone back to previous checkpoint")

    def perform_sweep(self):
        if self.tello.landed:
            print("Please take off the drone to perform sweep.")
        else:
            self.tello.manual = False
            # get current location as checkpoint location if is a new sweep route
            if self.step == 0:
                self.checkpoint_x = self.tello.x
                self.checkpoint_y = self.tello.y
                self.checkpoint_angle = self.tello.angle

            # if not a new route, get back to previous checkpoint
            if self.step != 0:
                self.back_checkpoint()

            for i in range(len(self.current_route)):
                if not self.tello.manual:  # each loop check whether is stop
                    if i == self.step:
                        if self.step == len(self.current_route) - 1:
                            print("Returning to Checkpoint 0. \n")

                        self.tello.send_route(self.current_route[self.step][1] + " " + str(self.current_route[self.step][2]))
                        time.sleep(4)  # delay to wait drone perform movement, then only update location
                        if not self.tello.manual:
                            self.tello.update_location(self.current_route[self.step][1], self.current_route[self.step][2])

                        self.tello.send_route(self.current_route[self.step][3] + " " + str(self.current_route[self.step][4]))
                        time.sleep(5)  # delay to wait drone perform movement, then only update location
                        if not self.tello.manual:
                            self.tello.update_location(self.current_route[self.step][3], self.current_route[self.step][4])

                        if not self.tello.manual:
                            # update checkpoint location if stop not trigger
                            self.checkpoint_x = self.tello.x
                            self.checkpoint_y = self.tello.y
                            self.checkpoint_angle = self.tello.angle
                            print("Arrived at Checkpoint: " + str(self.current_route[self.step][0]) + "\n")
                            self.step = self.step + 1

        if self.step == len(self.current_route):
            # complete sweep reset step to 0
            print("Completed route sweep and reset step to 0.")
            self.step = 0
