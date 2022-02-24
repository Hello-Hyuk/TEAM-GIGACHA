from planner_and_control.msg import Path
#from general_utils import Sensor_hub
class Ego:
    def __init__(self):
        #self.Sensor_hub= Sensor_hub
        self.x = 1
        self.y = 1
        self.heading = 1
        self.index = -1
        self.speed = -1
        self.steer = -1
        self.brake = -1
        self.gear = -1
        self.target_speed = 0.0
        self.path = Path()
        self.auto_manual = -1.0
