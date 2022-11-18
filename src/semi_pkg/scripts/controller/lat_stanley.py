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
        self.steer = 0

    def normalize(self, angle):
        while angle > pi:
            angle -= 2.0 * pi

        while angle < -pi:
            angle += 2.0 * pi

        return angle

    def make_yaw(self, path, yaw):
        for i in range(len(path.x)-30):
            yaw.append(atan2(path.y[i+1]-path.y[i],path.x[i+1]-path.x[i]))

    def run(self):
        while True:
            if self.parking.on == "on":
                self.parking_run()
            elif self.parking.on == "forced":
                self.parking_run2()
            elif self.parking.on == "off":
                self.yaw=[]
                self.path = self.lattice_path[self.shared.selected_lane]
                self.make_yaw(self.path, self.yaw)

                k_s = 0.0

                front_x = self.ego.x
                front_y = self.ego.y

                map_x = self.path.x[0]
                map_y = self.path.y[0]
                map_yaw = self.yaw[0]

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
                # print("-----------============----------")

                # print("map yaw :", map_yaw)
                # print("heading : ", radians(self.ego.heading))
                # print("yaw_term : ",degrees(yaw_term))
                # print("cte_term : ", degrees(cte_term))
                # print("steer : ",steer)

                # if steer < 3 and steer > -3:
                #     steer = 0

                self.steer = max(min(steer, 27.0), -27.0)
                # print("self.steer : ",self.steer)

            return self.steer

    def parking_run(self):
        if self.parking.direction == 0:
            self.path = self.parking.forward_path
            if len(self.forward_yaw) == 0:
                self.make_yaw(self.path, self.forward_yaw)
            yaw = self.forward_yaw
        else:
            self.path = self.parking.backward_path
            if len(self.backward_yaw) == 0:
                self.make_yaw(self.path, self.backward_yaw)
            yaw = self.backward_yaw
        k_s = 3.0

        front_x = self.ego.x
        front_y = self.ego.y

        map_x = self.path.x[self.parking.index]
        map_y = self.path.y[self.parking.index]
        map_yaw = yaw[self.parking.index]

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
        
        if steer < 3.5 and steer > -3.5:
            steer = 0

        self.steer = max(min(steer, 27.0), -27.0)

    def parking_run2(self):
        self.steer = self.ego.target_steer