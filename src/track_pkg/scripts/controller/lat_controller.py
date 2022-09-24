from math import hypot, cos, sin, degrees, atan2, radians, pi

class LatController():
    def __init__(self, pc, sh):
 
        self.perception = pc
        self.shared = sh

        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):
        while True:
            try:
                if self.perception.percep_state == "r_turn":
                    self.forced_angle1()
                elif self.perception.percep_state == "l_turn":
                    self.forced_angle2()
                elif self.shared.state == "2nd":
                    self.second_driving()
                else:
                    target_x, target_y = self.perception.point_x, self.perception.point_y
                    tmp = degrees(atan2(target_y, target_x)) % 360
                    distance = hypot(target_x, target_y)
                    alpha = -tmp
                    angle = atan2(2.0 * self.WB * sin(radians(alpha)) / distance, 1.0)

                    if degrees(angle) < 1 and degrees(angle) > -1:
                        angle = 0

                    self.steer = max(min(degrees(angle), 27.0), -27.0)
                
                return self.steer

            except ZeroDivisionError & IndexError:
                print("+++++++++lat_control++++++++")

    def forced_angle1(self):
        self.steer = 27

    def forced_angle2(self):
        self.steer = -27

    def second_driving(self):
        self.path = self.global_path
        # lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6)
        lookahead = 3
        target_index = lookahead*10 + self.ego.index
        
        target_x, target_y = self.path.x[target_index], self.path.y[target_index]

        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360
        
        alpha = self.ego.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)

        if degrees(angle) < 1 and degrees(angle) > -1:
            angle = 0

        self.steer = max(min(degrees(angle), 27.0), -27.0)        