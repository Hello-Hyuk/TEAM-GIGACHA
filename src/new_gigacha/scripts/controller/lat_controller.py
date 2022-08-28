import threading
from time import sleep
from math import hypot, cos, sin, degrees, atan2, radians, pi


class LatController(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego
        self.plan = parent.shared.plan
        self.parking = parent.shared.park

        self.lattice_path = parent.shared.lattice_path

        self.WB = 1.04  # wheel base
        self.k = 0.15  # 1.5
        self.lookahead_default = 4  # look-ahead default

    def run(self):
        while True:
            try:
                if self.parking.on:
                    self.parking_run()
                else:
                    self.path = self.lattice_path[self.shared.selected_lane]
                    # print(len(self.lattice_path), "\n", self.shared.selected_lane)
                    # self.path = self.shared.global_path
                    lookahead = min(self.k * self.ego.speed +
                                    self.lookahead_default, 6)
                    # target_index = len(self.path.x) - 30

                    # lookahead = min(self.k * self.ego.speed + self.lookahead_default, 7)
                    target_index = int(lookahead * 10)

                    target_x, target_y = self.path.x[target_index], self.path.y[target_index]
                    tmp = degrees(atan2(target_y - self.ego.y,
                                        target_x - self.ego.x)) % 360

                    # heading = self.ego.heading*1
                    # heading -= 180
                    # heading %= 360

                    alpha = self.ego.heading - tmp
                    angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)
                    # angle = -1.5*angle

                    if degrees(angle) < 0.5 and degrees(angle) > -0.5:
                        angle = 0

                    self.ego.input_steer = max(
                        min(degrees(angle), 27.0), -27.0)
                    # self.ego.input_steer = -27.0
            except IndexError:
                print("++++++++lat_controller+++++++++")

            sleep(self.period)

    def parking_run(self):
        if self.parking.direction == 0:
            self.path = self.parking.forward_path
            lookahead = 5
        else:
            self.path = self.parking.backward_path
            lookahead = 5

        target_index = lookahead + self.parking.index

        target_x, target_y = self.path.x[target_index], self.path.y[target_index]
        tmp = degrees(atan2(target_y - self.ego.y,
                            target_x - self.ego.x)) % 360

        heading = self.ego.heading
        ###### Back Driving ######
        if self.ego.input_gear == 2:
            heading += 180
            heading %= 360
        ##########################

        alpha = heading - tmp
        angle = atan2(2.0 * self.WB *
                      sin(radians(alpha)) / lookahead, 1.0)

        ###### Back Driving ######
        if self.ego.input_gear == 2:
            angle = -2.5*angle
        ##########################

        if degrees(angle) < 3.5 and degrees(angle) > -3.5:
            angle = 0

        self.ego.input_steer = max(min(degrees(angle), 27.0), -27.0)
