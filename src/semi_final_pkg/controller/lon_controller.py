class LonController():
    def __init__(self, eg):
        self.ego = eg

    def run(self): 
        self.speed = self.ego.target_speed

        return self.speed