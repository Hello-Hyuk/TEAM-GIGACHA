from math import hypot, cos, sin, degrees, atan2, radians, pi

class LatController():
    def __init__(self, eg):
 
        self.ego = eg
        # self.tracking_path = path
 
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):
        while True:
            try:
                # if self.plan.state == "1st":
                target_x, target_y = self.ego.point_x, self.ego.point_y
                
                tmp = degrees(atan2(target_y, target_x)) % 360
                distance = hypot(target_x, target_y)
                alpha = - tmp
                angle = atan2(2.0 * self.WB * sin(radians(alpha)) / distance, 1.0)

                return max(min(degrees(angle), 27.0), -27.0)

                # else:
                #     self.path = self.tracking_path
                #     lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6)
                #     target_index = int(self.ego.index + lookahead*10)
                    
                #     target_x, target_y = self.path.x[target_index], self.path.y[target_index]
                #     tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360
                    
                #     alpha = self.ego.heading - tmp
                #     angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)

                #     if degrees(angle) < 0.5 and degrees(angle) > -0.5:
                #         angle = 0

                #     self.ego.input_steer = max(min(degrees(angle), 27.0), -27.0)

            except ZeroDivisionError:
                print("+++++++++++++++++")