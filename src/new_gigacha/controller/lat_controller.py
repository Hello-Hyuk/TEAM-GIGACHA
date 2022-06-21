from math import hypot, cos, sin, degrees, atan2, radians, pi

class LatController(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.ego = parent.shared.ego
        self.path = parent.shared.local_path[1] # need to fix

        self.WB = 1.04 # wheel base
        self.k = 0.3 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):
        while True:
            lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6)
            
            target_index = len(self.path.data.x) - 20
            
            target_x, target_y = self.path.x[target_index], self.path.y[target_index]
            tmp = degrees(atan2(target_y - self.ego.data.y, target_x - self.ego.data.x)) % 360
            
            alpha = self.ego.heading - tmp
            angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)

            if degrees(angle) < 0.5 and degrees(angle) > -0.5:
                angle = 0

            return max(min(degrees(angle), 27.0), -27.0)