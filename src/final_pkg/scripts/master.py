import threading
import rospy
import argparse
# from local_pkg.msg import Guii
from shared.shared import Shared
from localizer.localizer import Localizer
from planner.mission_planner import MissionPlanner
from planner.behavior_planner import BehaviorPlanner
from planner.motion_planner import MotionPlanner
from controller.controller import Controller
from utils.sig_int_handler import ActivateSignalInterruptHandler
from utils.env_visualizer import Visualizer
# 여러 폴더에서 필요한 파일들 import

from time import sleep

class Master(threading.Thread): # 마스터 클래스로, 메인 스레드로 작동함
    def __init__(self, args, ui_rate): # master class의 argument, rate를 설정할 수 있게 해주는 init 함수
        super().__init__()
        self.args = args
        self.period = 1.0 / ui_rate

        rospy.init_node('master', anonymous=False)

        self.dead_index = 0

    def run(self): # 서브 스레드 생성 함수
        self.shared = Shared() # 공유 메모리

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
            # 디버깅 시 터미널창에서 프린트하여 사용하는 것들

            print('index :', self.shared.ego.index)
            print('heading :', self.shared.ego.heading)
            print('Mission_State : {}'.format(self.shared.plan.state))
            print('Behavior_Decision : {}'.format(self.shared.plan.behavior_decision))
            # print('speed : ', self.shared.ego.input_speed)
            # print("red : ", self.shared.perception.tred, ", yellow : ", self.shared.perception.tyellow, ", green : ", self.shared.perception.tgreen, ", left : ", self.shared.perception.tleft)
            # # # # print('Motion_Selected lane : {}'.format(self.shared.selected_lane))
            # print('Speed : {}, Steer : {:.2f}'.format(self.shared.ego.input_speed, self.shared.ego.input_steer))
            # print('Current Speed : {},'.format(self.shared.ego.speed))
            # print(self.shared.ego.dis)

            self.checker_all()

            sleep(self.period)

    def init_thread(self, module): # 클래스를 스레드로 사용할 수 있게 해주는 함수
        module.daemon = True # 메인 스레드가 종료되면 함께 종료됨
        module.start()

    def checker_all(self): # 여러 스레드가 종료되었는지 체크하는 함수
        self.thread_checker(self.localizer)
        self.thread_checker(self.mission_planner)    
        self.thread_checker(self.behavior_planner)
        self.thread_checker(self.motion_planner)
        self.thread_checker(self.controller)
        self.thread_checker(self.visualizer)

    def thread_checker(self, module): # 스레드가 종료되었는지 체크하는 함수
        if not module.is_alive():
            print(type(module).__name__, "is dead.. at : ", self.dead_index)
            if self.dead_index == 0:
                self.dead_index = self.shared.ego.index


if __name__ == "__main__": 
    # CLI에서 map 옵션을 줄 수 있게 설정
    argparser = argparse.ArgumentParser(
        description="GIGACHA"
    )
    argparser.add_argument(
        '--map',
        default='kcity_simul/final_map',
        help='kcity_simul/final_map, Siheung/delivery2, Siheung/sibaedal'
    )
    
    ActivateSignalInterruptHandler()
    args = argparser.parse_args()
    master = Master(args, ui_rate=10)
    master.start() # master 클래스에 정의된 run 메서드 호출하며 실행됨
