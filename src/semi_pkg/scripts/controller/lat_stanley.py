from math import hypot, cos, sin, degrees, atan2, radians, pi
import numpy as np

class Stanley():
    def __init__(self, eg, sh, lattice, pl, park):
 
        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = park
        self.lattice_path = lattice

        self.forward_yaw = []
        self.backward_yaw = []
        self.yaw = []

        self.k = -0.8 # CTR parameter
        self.direction = 1

    def normalize(self, angle):
        while angle > pi:
            angle -= 2.0 * pi

        while angle < -pi:
            angle += 2.0 * pi

        return angle

    def make_yaw(self, path, yaw):
        for i in range(len(path.x)-1):
            yaw.append(atan2(path.y[i+1]-path.y[i],path.x[i+1]-path.x[i]))

    def run(self):
        while True:
            try:
                if self.parking.on == "on":
                    self.parking_run()
                elif self.parking.on == "forced":
                    self.parking_run2()
                elif self.parking.on == "off":
                    self.path = self.lattice_path[self.shared.selected_lane]
                    self.make_yaw(self.path, self.yaw)

                    k_s = 0

                    front_x = self.ego.x
                    front_y = self.ego.y

                    map_x = self.path[self.ego.index]
                    map_y = self.path[self.ego.index]
                    map_yaw = self.yaw[self.ego.index]

                    dx = map_x - front_x
                    dy = map_y - front_y

                    perp_vec = [self.direction*cos(radians(self.ego.heading)+pi/2), self.direction*sin(radians(self.ego.heading)+pi/2)]
                    cte = np.dot([dx, dy], perp_vec)

                    final_yaw = -(map_yaw - radians(self.ego.heading))
                    # control law
                    yaw_term = self.normalize(final_yaw)
                    # cte_term = atan2(self.k*cte, self.state.speed)
                    cte_term = atan2(self.k*cte, self.ego.speed + k_s)

                    # steering
                    steer = degrees(yaw_term + cte_term)

                    if degrees(steer) < 0.5 and degrees(steer) > -0.5:
                        steer = 0

                    self.steer = max(min(degrees(steer), 27.0), -27.0)

                return self.steer

            except IndexError:
                print("++++++++lat_controller+++++++++")

    def parking_run(self):
        if self.parking.direction == 0:
            self.path = self.parking.forward_path
            self.make_yaw(self.path, self.forward_yaw)
            k_s = 3.0

            front_x = self.ego.x
            front_y = self.ego.y

            map_x = self.path[self.parking.index]
            map_y = self.path[self.parking.index]
            map_yaw = self.yaw[self.parking.index]

            dx = map_x - front_x
            dy = map_y - front_y

            perp_vec = [self.direction*cos(radians(self.ego.heading)+pi/2), self.direction*sin(radians(self.ego.heading)+pi/2)]
            cte = np.dot([dx, dy], perp_vec)

            final_yaw = -(map_yaw - radians(self.ego.heading))
            # control law
            yaw_term = self.normalize(final_yaw)
            # cte_term = atan2(self.k*cte, self.state.speed)
            cte_term = atan2(self.k*cte, self.ego.speed + k_s)

            # steering
            steer = degrees(yaw_term + cte_term)
        else:
            self.path = self.parking.backward_path
            self.make_yaw(self.path, self.backward_yaw)
            self.direction = -1
        
            k_s = 3.0

            front_x = self.ego.x
            front_y = self.ego.y

            map_x = self.path[self.parking.index]
            map_y = self.path[self.parking.index]
            map_yaw = self.yaw[self.parking.index]

            dx = map_x - front_x
            dy = map_y - front_y

            perp_vec = [self.direction*cos(radians(self.ego.heading)+pi/2), self.direction*sin(radians(self.ego.heading)+pi/2)]
            cte = np.dot([dx, dy], perp_vec)

            final_yaw = -(map_yaw - radians(self.ego.heading))
            # control law
            yaw_term = self.normalize(final_yaw)
            # cte_term = atan2(self.k*cte, self.state.speed)
            cte_term = atan2(self.k*cte, self.ego.speed + k_s)

            # steering
            steer = degrees(yaw_term + cte_term)

        # heading = self.ego.heading
        # ###### Back Driving ######
        # if self.ego.target_gear == 2:
        #     heading += 180
        #     heading %= 360
        # ##########################

        # ###### Back Driving ######
        # if self.ego.target_gear == 2:
        #     steer = -1.5*steer
        # ##########################

        if degrees(steer) < 3.5 and degrees(steer) > -3.5:
            steer = 0

        self.steer = max(min(degrees(steer), 27.0), -27.0)

    def parking_run2(self):
        self.steer = self.ego.target_steer