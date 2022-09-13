import threading
import rospy
import argparse
from local_pkg.msg import Master
from shared.shared import Shared
from localizer.localizer import Localizer
from planner.mission_planner import MissionPlanner
from planner.behavior_planner import BehaviorPlanner
from planner.motion_planner import MotionPlanner
from controller.controller import Controller
from utils.sig_int_handler import ActivateSignalInterruptHandler
from utils.env_visualizer import Visualizer

from time import sleep

class Master(threading.Thread):
    def __init__(self, args, ui_rate):
        super().__init__()
        self.args = args
        self.period = 1.0 / ui_rate

        rospy.init_node('master', anonymous=False)
        self.pub = rospy.Publisher("/from_master", Master, queue_size = 1)
        # self.status = Master()

    def run(self):
        self.shared = Shared()

        self.localizer = Localizer(self, rate=50)
        self.init_thread(self.localizer)

        self.mission_planner = MissionPlanner(self, rate=10)
        self.init_thread(self.mission_planner)

        self.behavior_planner = BehaviorPlanner(self, rate=10)
        self.init_thread(self.behavior_planner)

        self.motion_planner = MotionPlanner(self, rate=20)
        self.init_thread(self.motion_planner)

        self.controller = Controller(self, rate=20)
        self.init_thread(self.controller)

        self.visualizer = Visualizer(self, rate=10)
        self.init_thread(self.visualizer)

        while True:
            # print("---------------------")
            # self.checker_all()
            # # print('Localization')
            print('x : {0:.2f}, y : {1:.2f}, index : {2}, \nheading : {3:.2f}'\
               .format(self.shared.ego.x, self.shared.ego.y, self.shared.ego.index, self.shared.ego.heading))
            print('Mission_State : {}'.format(self.shared.plan.state))
            print('Behavior_Decision : {}'.format(self.shared.plan.behavior_decision))
            # print('Motion_Selected lane : {}'.format(self.shared.selected_lane))
            # print('Controller')
            # print('Speed : {}, Steer : {:.2f}'.format(self.shared.ego.input_speed, self.shared.ego.input_steer))
            # print('Speed : {},'.format(self.shared.ego.speed))
            # print(self.shared.perception.signname)
            # print("tmp :" , self.shared.perception.tmp_objx, self.shared.perception.tmp_objy, self.shared.perception.objw)
            # print("tmp :" ,len(self.shared.perception.tmp_objx))
            # print("real :" ,len(self.shared.perception.objx))
            # print("real :" , self.shared.perception.objx, self.shared.perception.objy)
            ##print('self.shared.park.index : ',self.shared.park.index)
            ##print("parking on : ", self.shared.park.on)
            # print("hello")

            # self.status.mission = self.shared.plan.state
            # self.status.behavior = self.shared.plan.behavior_decision
            # self.status.index = self.shared.ego.index
            # self.status.localizer = self.thread_checker_(self.localizer)
            # self.status.mission_pln = self.thread_checker_(self.mission_planner)
            # self.status.behavior_pln = self.thread_checker_(self.behavior_planner)
            # self.status.motion_pln = self.thread_checker_(self.motion_planner)
            # self.status.lat_con = self.thread_checker_(self.lat_controller)
            # self.status.lon_con = self.thread_checker_(self.lon_controller)

            # self.pub.publish(self.status)

            sleep(self.period)

    def init_thread(self, module):
        module.daemon = True
        module.start()

    def checker_all(self):
        self.thread_checker(self.localizer)
        self.thread_checker(self.mission_planner)    
        self.thread_checker(self.behavior_planner)
        self.thread_checker(self.motion_planner)
        self.thread_checker(self.lat_controller)
        self.thread_checker(self.lon_controller)
        self.thread_checker(self.visualizer)

    def thread_checker(self, module):
        if not module.is_alive():
            print(type(module).__name__, "is dead..")

    def thread_checker_(self, module):
        return module.is_alive()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="GIGACHA"
    )
    argparser.add_argument(
        '--map',
        default='kcity_simul/final_map',
        help='kcity/map1, songdo/map2, yonghyeon/Yonghyeon, kcity_simul/left_lane, kcity_simul/right_lane, kcity_simul/final, inha_parking/gpp'
    )

    ActivateSignalInterruptHandler()
    args = argparser.parse_args()
    master = Master(args, ui_rate=10)
    master.start()
