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
        self.cut_path = Path()
        self.lattice_path = []
        self.selected_lane = 1
        self.plan = Plan()