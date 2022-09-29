class LonController():
    def __init__(self, eg, sh):
        self.ego = eg
        self.shared = sh
        self.speed = 0

    def run(self): 
        if self.shared.state == "2nd":
            if self.ego.input_steer > 7:
                self.speed = 6
            else:
                self.speed = 10
        else:
            if self.ego.input_steer > 7:
                self.speed = 5
            else:
                self.speed = 5

        return self.speed