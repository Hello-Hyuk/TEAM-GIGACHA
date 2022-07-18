from math import hypot, cos, sin, degrees, atan2, radians, pi

class LatController():
    def __init__(self, eg, path, select):
 
        self.ego = eg
        self.tracking_path = path
        self.selected_lane = select
 
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):

        self.path = self.tracking_path[self.selected_lane]
        lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6)
        target_index = len(self.path.x) - 1

        # lookahead = min(self.k * self.ego.speed + self.lookahead_default, 7)
        # target_index = lookahead * 10
        
        target_x, target_y = self.path.x[target_index], self.path.y[target_index]
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360
        
        alpha = self.ego.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)

        if degrees(angle) < 1 and degrees(angle) > -1:
            angle = 0

        return max(min(degrees(angle), 27.0), -27.0)