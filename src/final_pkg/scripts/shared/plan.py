from .path import Path

class Plan(): # planner에서 사용되는 state, behavior_decision을 담고 있는 클래스
    def __init__(self):
        self.state = " "
        self.behavior_decision = " "