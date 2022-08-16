
class PI:
    
    def __init__(self, eg):
        self.ego = eg
        self.P = 0
        self.I = 0
        self.error_sum = 0.0
        self.dt = 1.0 / 10.0
        self.target_ex = 0

    def pi(self):

        error = self.ego.data.target_speed - self.ego.data.speed
        self.error_sum += error

        self.speed = min(self.ego.data.target_speed - 1 , self.P*error + self.I*self.error_sum*self.dt)

    def decel(self):
        self.P = 1
        self.I = 1
        self.pi()

        print(f"pi speed : {self.speed}")
        return self.speed

    # def accel(self):
    #     self.P = 5
    #     self.I = 0.5
    #     self.D = 1
    #     self.pid()

    #     return self.speed