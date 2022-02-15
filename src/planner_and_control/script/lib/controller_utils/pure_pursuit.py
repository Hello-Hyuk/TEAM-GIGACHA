from math import hypot, cos, sin, degrees, atan2, radians, pi

class PurePursuit:
    def __init__(self, ego, trajectory):
        self.WB = 1.04 # wheel base
        self.k = 0.3 #1.5
        self.lookahead_default = 4.0 #look-ahead default

        self.ego = ego

        self.path = trajectory

    def run(self):

        if self.ego.mode == "driving":
            lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6) # look-ahead
        else :
            lookahead = 0.5
            
        target_index = int(self.ego.index + lookahead*10)
        target_x, target_y = path.x[target_index], path.y[target_index]
        print(f"target_index : {target_index}")
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

        # if self.ego.mode == "backward" :
        #     self.ego.heading = (self.ego.heading + 180) % 360        
    
        alpha = self.ego.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)


        print(f"tmp : {tmp}")
        print(f"heading : {self.ego.heading}")

        # if self.ego.mode == "backward" :
        #     angle = -angle

        return max(min(degrees(angle), 27.0), -27.0)
     
    # def deaccel(self):

    #     if self.ego.mode == "driving":
    #         lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6) # look-ahead
    #     else :
    #         lookahead = 0.8

    #     target_index_v = int(self.ego.index + lookahead*25)
    #     target_x_v, target_y_v = path.x[target_index_v], path.y[target_index_v]
    #     curve_check = abs (self.ego.heading - degrees(atan2(target_y_v - self.ego.y, target_x_v - self.ego.x)) % 360  )
    #     return curve_check