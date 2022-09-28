class LonController():
    def __init__(self, eg, sh):
        self.ego = eg
        self.shared = sh

    def run(self): 
        if self.shared.state == "2nd":
            self.speed = 10
        else:
            self.speed = 7

        return self.speed