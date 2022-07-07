import threading
from time import sleep
from math import hypot, cos, sin, degrees, atan2, radians, pi,sqrt
import numpy as np

class LonController(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego
        self.plan = parent.shared.plan


        self.lattice_path = parent.shared.lattice_path
        self.global_path = parent.shared.global_path
        

        self.P = 0
        self.I = 0
        self.D = 0
        self.error_sum = 0.0
        self.pre_error=0
        self.error=0
        self.dt = 1.0 / 10.0


        self.car_max_speed=10
        self.road_friction=0.15
 

    def curve_based_velocity(self,global_path,point_num):
        out_vel_plan=[]
        for i in range(0,point_num):
            out_vel_plan.append(self.car_max_speed)

        for i in range(point_num,len(global_path.poses)-point_num):
            x_list=[]
            y_list=[]
            for box in  range(-point_num,point_num):
                x=global_path.x[i+box]
                y=global_path.x[i+box]
                x_list.append([-2*x,-2*y,1])
                y_list.append(-(x*x)-(y*y))
                
            x_matrix=np.array(x_list)
            y_matrix=np.array(y_list)
            x_trans=x_matrix.T
                

            a_matrix=np.linalg.inv(x_trans.dot(x_matrix)).dot(x_trans).dot(y_matrix)
            a=a_matrix[0]
            b=a_matrix[1]
            c=a_matrix[2]
            r=sqrt(a*a+b*b-c)
            v_max=sqrt(r*9.8*self.road_friction)  #0.7
            if v_max>self.car_max_speed :
                v_max=self.car_max_speed
            out_vel_plan.append(v_max)

        for i in range(len(global_path.poses)-point_num,len(global_path.poses)):
            out_vel_plan.append(self.car_max_speed)
            
        return out_vel_plan



    def run(self): 
        while True:
            try:

                self.speed=self.curve_based_velocity(self.global_path,30)
                self.ego.input_speed=self.speed[self.ego.index]
               

            except IndexError:
                print("+++++++++++++++++")

            sleep(self.period)