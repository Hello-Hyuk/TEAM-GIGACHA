#!/usr/bin/env python3
from socket import MsgFlag
import rospy
from lib.general_utils.read_global_path import read_global_path
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.planner_utils.LPP import LatticePlanner
from lib.planner_utils.find_local_path import findLocalPath
from lib.planner_utils.index_finder import IndexFinder
from std_msgs.msg import String
from nav_msgs.msg import Path
from planner_and_control.msg import Path as CustomPath
from planner_and_control.msg import Ego


class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)
        rospy.Subscriber('/behavior', String, self.behavior_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        # rospy.Subscriber('/obj',Path,self.obj_callback)

        self.pub = rospy.Publisher('/trajectory', CustomPath, queue_size = 1)

        self.ego = Ego()
        self.behavior = ''
        self.trajectory = CustomPath()
        self.trajectory_name = ""

        self.lattice_path = Path()

        self.ego_speed = 0
        self.ego_status = []
        self.current_lane = 0
        # self.obj= Path()
    
    def behavior_callback(self, msg):
        self.behavior = msg.data

    def ego_callback(self, msg):
        self.ego = msg
        self.ego_status = [self.ego.x, self.ego.y, self.ego.speed]

    # def obj_callback(self,msg):
    #     self.obj=msg
    #     self.obj.x=4
    #     self.obj.y=2

        
    def run(self):
        # trajectroy initalization
        self.trajectory = read_global_path('ex')

        # trajectroy devide
        self.local_path=findLocalPath(self.trajectory,self.ego)

        # find my local
        # self.current_waypoint=IndexFinder.run()

        # create lattice path(weight)
        # self.lattice_path,self.selected_lane = LatticePlanner(self.local_path, self.obj , self.ego_status, self.ego.speed, self.current_lane)
        self.lattice_path,self.selected_lane = LatticePlanner(self.local_path, self.ego_status, self.ego.speed)

        # select lane(path)

        if self.behavior == "go":
            self.trajectory_name = "global_path"

        if self.behavior == "obstacle avoidance":
            

            
            self.current_lane=self.selected_lane
            
            if self.selected_lane != -1: 
                self.local_path=self.lattice_path[self.selected_lane]
        
        print(f"motion_planner : {self.trajectory_name}")

        self.pub.publish(self.trajectory)

        lane_weight=[5, 1, 0, 1, 1] #reference path 
        collision_bool=[False, False, False, False, False]

        # if len(global_vaild_object)>0:
        if 1 > 0:

            for path_num in range(len(self.local_path)) :
                        
                for path_pos in self.local_path[path_num].poses :

                    #dis= sqrt(pow(global_vaild_object.x,2)+pow(global_vaild_object.y,2))
                    dis=3
   
                    if dis<7:
                        collision_bool[path_num]=True
                        lane_weight[path_num]=lane_weight[path_num]+100
                        print(f"Obstacle distance: {dis}")

                        break
            
        
        else :
            print("No Obstacle")
    
        selected_lane=lane_weight.index(min(lane_weight))
        print(lane_weight,selected_lane)
        all_lane_collision=True
        
    else :
        print("NO Reference Path")
        selected_lane=-1  

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mp = Motion_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mp.run()
        rate.sleep()