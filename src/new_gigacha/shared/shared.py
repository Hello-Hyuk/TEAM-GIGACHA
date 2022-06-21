from .ego import Ego
from .perception import Perception
from .path import Path

class Shared:
    def __init__(self):
        self.ego = Ego()
        self.perception = Perception()
        self.global_path = Path()
        self.local_path = []

        for i in range(9):
            lattice = Path()
            self.local_path.append(lattice)
