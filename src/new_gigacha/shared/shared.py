from .ego import Ego
from .perception import Perception_
from .path import Path
from .plan import Plan

class Shared:
    def __init__(self):
        self.ego = Ego()
        self.perception = Perception_()
        self.state = ''
        self.global_path = Path()
        self.local_path = []
        self.local_path_num = 4
        self.plan = Plan()
        # self.state = " "
        # self.behavior_decision = " "
        # self.trajectory = Path()

        for i in range(9):
            lattice = Path()
            self.local_path.append(lattice)

    def run(self):
        pass