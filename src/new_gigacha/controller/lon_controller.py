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
 





"""
def pid(a,b)
이 함수는 속도a에서 속도b로 가는동안 속도에 관한 pid제어를 하는 함수입니다.

a와 b는 속도에 관한 파라미터로 float형으로 입력되어야합니다.

최종적으로 목표 속도 b를 리턴합니다.


"""
    def pid(self,ego_vel,target_vel):
        self.error=target_vel-ego_vel
        self.error_sum+=self.error
        
        output=self.P*error + self.I*self.error_sum*self.dt + self.D*(self.error-self.pre_error)/self.dt

        out_vel=target_vel+output



        return out_vel




"""
def curve_based_velocity(a,b)
이 함수는 글로벌 패스 a를 가져와서 (-b,b)범위의 인덱스에 곡선 구간 속도제어를 도입합니다.
a의 역할은 해당 계산을 수행할시 a의 x,y값을 사용합니다.


최종적으로  out_vel_plan 이라는 속도값이 담긴 list를 리턴합니다.


"""

    def curve_based_velocity(self,global_path,point_num):
        out_vel_plan=[]
        for i in range(0,point_num):
            out_vel_plan.append(self.car_max_speed)

        for i in range(point_num,len(global_path.poses)-point_num):
            x_list=[]
            y_list=[]
            for box in  range(-point_num,point_num):
                x=global_path.poses[i+box].pose.position.x
                y=global_path.poses[i+box].pose.position.y
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

                vel_profile=self.curveBasedVelocity(self.global_path,30)

                self.ego.input_speed = self.pid(self.ego.speed, vel_profile[self.ego.index])
            
            except IndexError:
                print("+++++++++++++++++")

            sleep(self.period)