import threading
import rospy
import argparse
import serial
from shared.shared import Shared
from localizer.localizer import Localizer
from planner.mission_planner import MissionPlanner
from planner.behavior_planner import BehaviorPlanner
from planner.motion_planner import MotionPlanner
from controller.lat_controller import LatController
from controller.lon_controller import LonController
from utils.serial_reader import SerialReader
from utils.serial_writer import SerialWriter
from utils.sig_int_handler import ActivateSignalInterruptHandler
from utils.env_visualizer import Visualizer

from time import sleep


class Master(threading.Thread):
    def __init__(self, args, ui_rate):
        super().__init__()
        self.args = args
        self.period = 1.0 / ui_rate

        # self.ser = serial.Serial("/dev/ttyUSB0", 115200)  # Simulation
        self.ser = serial.Serial("/dev/erp42", 115200) # Real World

        rospy.init_node('master', anonymous=False)

    def run(self):
        self.shared = Shared()

        self.localizer = Localizer(self, rate=10)
        self.init_thread(self.localizer)

        # self.DR = DR(self, rate = 50)
        # self.init_thread(self.DR)

        self.mission_planner = MissionPlanner(self, rate=10)
        self.init_thread(self.mission_planner)

        self.behavior_planner = BehaviorPlanner(self, rate=10)
        self.init_thread(self.behavior_planner)

        self.motion_planner = MotionPlanner(self, rate=20)
        self.init_thread(self.motion_planner)

        self.lat_controller = LatController(self, rate=20)
        self.init_thread(self.lat_controller)

        self.lon_controller = LonController(self, rate=3)
        self.init_thread(self.lon_controller)

        self.serial_reader = SerialReader(self, rate=20)
        self.init_thread(self.serial_reader)

        self.serial_writer = SerialWriter(self, rate=10)
        self.init_thread(self.serial_writer)

        self.visualizer = Visualizer(self, rate=10)
        self.init_thread(self.visualizer)

        while True:
            # print('Localization : x : {0}, y : {1}, index : {2}, heading : {3}'\
            #     .format(self.shared.ego.x, self.shared.ego.y, self.shared.ego.index, self.shared.ego.heading))
            # print('Mission : State : {}'.format(self.shared.plan.state))
            # print('Behavior : Decision : {}'.format(self.shared.plan.behavior_decision))
            # print('Motion : Selected lane : {}'.format(self.shared.selected_lane))
            # print('Controller : Speed : {}, Steer : {}'.format(self.shared.ego.input_speed, self.shared.ego.input_steer))
            # print("tmp :" , self.shared.perception.tmp_objx, self.shared.perception.tmp_objy, self.shared.perception.objw)
            print("tmp :" ,len(self.shared.perception.tmp_objx))
            print("real :" ,len(self.shared.perception.objx))
            # print("real :" , self.shared.perception.objx, self.shared.perception.objy)
            sleep(self.period)

    def init_thread(self, module):
        module.daemon = True
        module.start()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="GIGACHA"
    )
    argparser.add_argument(
        '--map',
        default='yonghyeon/Yonghyeon',
        help='kcity/map1, songdo/map2, yonghyeon'
    )

    ActivateSignalInterruptHandler()
    args = argparser.parse_args()
    master = Master(args, ui_rate=10)
    master.start()
