from math import hypot, cos, sin, degrees, atan2, radians, pi, sqrt

class LatController():
    def __init__(self, eg, sh, lattice, pl, park):
 
        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = park
        self.lattice_path = lattice

        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):
        while(1):
            try:
                if self.parking.on == "on":
                    self.parking_run()
                elif self.parking.on == "forced":
                    self.parking_run2()
                elif self.parking.on == "U_turn":
                    self.U_turn()
                elif self.parking.on == "off":
                    self.steer, speed = self.pure_pursuit()

                return self.steer, speed

            except IndexError:
                print("++++++++lat_controller+++++++++")
    
    # todo : lat controller
    def pure_pursuit(self):
        steer = 0
        speed = 0
        
        

        return steer, speed

    def parking_run(self):
        if self.parking.direction == 0:
            self.path = self.parking.forward_path
            lookahead = 5
        else:
            self.path = self.parking.backward_path
            lookahead = 5
        # if not self.parking.inflection_on:
        target_index = lookahead + self.parking.index
        # else:
        #     target_index = len(self.parking.backward_path.x) - 1

        target_x, target_y = self.path.x[target_index], self.path.y[target_index]
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

        heading = self.ego.heading
        ###### Back Driving ######
        if self.ego.target_gear == 2:
            heading += 180
            heading %= 360
        ##########################

        alpha = heading - tmp
        angle = atan2(2.0 * self.WB *
                      sin(radians(alpha)) / lookahead, 1.0)

        ###### Back Driving ######
        if self.ego.target_gear == 2:
            angle = -1.5*angle
        ##########################

        if degrees(angle) < 3.5 and degrees(angle) > -3.5:
            angle = 0

        self.steer = max(min(degrees(angle), 27.0), -27.0)

    def parking_run2(self):
        self.steer = self.ego.target_steer