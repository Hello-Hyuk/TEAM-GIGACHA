#!/usr/bin/env python3
from socket import MsgFlag
import rospy
from math import sqrt
from lib.general_utils.read_global_path import read_global_path
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.planner_utils.LPP import path_maker
from lib.planner_utils.find_local_path import findLocalPath
from lib.planner_utils.index_finder import IndexFinder
from std_msgs.msg import String
from nav_msgs.msg import Path
from planner_and_control.msg import Path as CustomPath
from planner_and_control.msg import Ego
from planner_and_control.msg import Obj

class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)
        rospy.Subscriber('/behavior', String, self.behavior_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/obj', Obj, self.obj_callback)

        self.global_path_pub = rospy.Publisher('/global_path', CustomPath, queue_size = 1)
        self.local_path_pub = rospy.Publisher('/lattice_path', CustomPath, queue_size = 1)
        self.trajectory_pub = rospy.Publisher('/local_path', CustomPath, queue_size = 1)

        for i in range(1,6):
            globals()['lattice_path_{}_pub'.format(i)]=rospy.Publisher('lattice_path_{}'.format(i),Path,queue_size=1) 

        self.ego = Ego()
        self.behavior = ''

        self.global_path = CustomPath()
        
        self.generated_path = Path()

        self.trajectory_name = ""

        self.global_path = read_global_path('ex')

        self.ego_speed = 0
        # self.ego_status = []
        self.current_lane = 0
        self.obj = Obj()
        self.obj.x = 105.8
        self.obj.y = 203.8
    
    def behavior_callback(self, msg):
        self.behavior = msg.data
    def ego_callback(self, msg):
        self.ego = msg
        # self.ego_status = [self.ego.x, self.ego.y, self.ego.speed]

    def obj_callback(self, msg):
        self.obj = msg

    def run(self):
        self.local_path = findLocalPath(self.global_path,self.ego) # local path (50)
        self.generated_path = path_maker(self.local_path, self.ego) # lattice paths

        trajectory = CustomPath()

        if self.behavior == "go":
            self.trajectory_name = "global_path"

        if self.behavior == "obstacle avoidance":
            lane_weight = [25, 15, 0, 10, 20]
            # make distance by obstacle priority
            # make distance by global path _ gara
            # choose left _ gara
            dis = sqrt((self.ego.x - self.obj.x)**2 + (self.ego.y - self.obj.y)**2)

            print("dis : ",)
            if dis < 10:
                for i in range (len(self.generated_path)):
                    distance = sqrt((self.generated_path[i].poses[-1].pose.position.x - self.obj.x)**2 + (self.generated_path[i].poses[-1].pose.position.y - self.obj.y)**2)
                    lane_weight[i] += (1 / distance)
                lane_weight[2] = 100
                lane_weight[1] = 10000

            print(lane_weight)

            
            # make distance by road end
            # make distance by opposite lane

            self.selected_lane = lane_weight.index(min(lane_weight))

            print(self.selected_lane)

            if self.selected_lane != -1:
                self.local_path = self.generated_path[self.selected_lane]
                self.trajectory_name = self.selected_lane

        for i in range (len(self.local_path.poses)):
            trajectory.x.append(self.local_path.poses[i].pose.position.x)
            trajectory.y.append(self.local_path.poses[i].pose.position.y)
        
        print(f"motion_planner : {self.trajectory_name}, local_path")


        # global path
        self.global_path_pub.publish(self.global_path)

        if len(self.generated_path)==5:                    
            for i in range(1,6):
                globals()['lattice_path_{}_pub'.format(i)].publish(self.generated_path[i-1])

        # real path
        self.trajectory_pub.publish(trajectory)



        ###############################################

        # if len(global_vaild_object)>0:
        # if 1 > 0:
            # for path_num in range(len(self.local_path)) :
            #     #dis= sqrt(pow(global_vaild_object.x,2)+pow(global_vaild_object.y,2))
            #     dis = 3
            #     if dis < 7:
            #         self.collision_bool[path_num] = True
            #         self.lane_weight[path_num] = self.lane_weight[path_num]+100
            #         print(f"Obstacle distance: {dis}")
            #         break

        # else :
        #     print("No Obstacle")
    
        # print(self.lane_weight,selected_lane)
        # all_lane_collision = True
        
    # else :
    #     print("NO Reference Path")
    #     selected_lane=-1

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mp = Motion_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mp.run()
        rate.sleep()