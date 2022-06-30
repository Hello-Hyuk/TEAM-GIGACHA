from .ego import Ego
from .perception import Perception_
from .path import Path
from .plan import plan

class Shared:
    def __init__(self):
        self.ego = Ego()
        self.perception = Perception_()
        self.state = ''
        self.global_path = Path()
        self.local_path = []
        self.local_path_num = 4
        self.plan = plan()

        for i in range(9):
            lattice = Path()
            self.local_path.append(lattice)

    # def run(self):
    #     while 1:
    #         pass