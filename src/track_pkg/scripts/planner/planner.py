#!/usr/bin/env python3
import threading
from math import hypot
from time import sleep
from std_msgs.msg import String
from math import pi, cos, sin
from visualization_msgs.msg import MarkerArray, Marker
import rospy

class Planner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.global_path = self.shared.global_path

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.state = self.shared.state
        self.total_obs = []


    def makePath(self):        
        self.perception.left_obs.sort(key = lambda x : x[2])
        self.perception.right_obs.sort(key= lambda x : x[2])


        # 왼쪽에서 인식한 러버콘수가 2개초과이면 2개만 남긴다 그 뒤 오른쪽에서 인식한 러버콘 수가 2개 초과이면 2개만 남긴다.
        if len(self.perception.left_obs) > 2:
            self.perception.left_obs = self.perception.left_obs[0:2]   

        if len(self.perception.right_obs) > 2:
            self.perception.right_obs=self.perception.right_obs[0:2]
        
        # concat all obstacle
        self.total_obs = self.perception.left_obs + self.perception.right_obs

        # (2,2), (2,1), (1,2), (1,1) case
        if len(self.perception.left_obs) != 0 and len(self.perception.right_obs) != 0:
            self.makeCOM(self.perception.left_obs, self.perception.right_obs)
        # (2,0), (1,0), (0,1), (0,2)
        elif len(self.perception.left_obs) == 0 or len(self.perception.right_obs) == 0:
            self.makeFakeCOM(self.perception.left_obs, self.perception.right_obs)
        else:   # (0, 0) case
            pass






    def makeCOM(self, left_points, right_points):
        lpointx=0
        lpointy=0
        rpointx=0
        rpointy=0

        for point in left_points:
            lpointx+=point[0]
            lpointy+=point[1]

        for point in right_points:
            rpointx+=point[0]
            rpointy+=point[1]

        try:
            self.ego.point_x=(lpointx+rpointx)/(len(left_points)+len(right_points))
            self.ego.point_y=(lpointy+rpointy)/(len(left_points)+len(right_points))
        except ZeroDivisionError:
            pass
    
    # (2,0), (1,0), (0,2), (0,1) case
    def makeFakeCOM(self, left_points, right_points):
        fake_point_list = []
        # right case
        if len(left_points) == 0:
            for rpoint in right_points:
                fake_point_list.append([rpoint[0], rpoint[1]+4.5, rpoint[2], rpoint[3]])
            self.makeCOM(fake_point_list, right_points)
        # left case
        elif len(right_points) == 0:
            for lpoint in left_points:
                fake_point_list.append([lpoint[0], lpoint[1]-4.5, lpoint[2], lpoint[3]])
            self.makeCOM(left_points, fake_point_list)
        else:
            rospy.loginfo("Failed to classificate in FakeCOM")

    # def cal_circul(self, left_points, right_points):

    #      x_list=[]
    #      y_list=[]
    #      #points=[[0, 0, 0, 0]]

    #      for point in left_points:
    #          points.append(point)

    #      for point in right_points:
    #          points.append(point)

    #      for point in points:
    #          x = point[0]
    #          y = point[1]
    #          x_list.append([-2*x,-2*y,1])
    #          y_list.append(-(x*x)-(y*y))
            
    #      print(points)
    #      x_matrix=np.array(x_list)
    #      y_matrix=np.array(y_list)
    #      x_trans=x_matrix.T
                
    #      a_matrix=np.linalg.inv(x_trans.dot(x_matrix)).dot(x_trans).dot(y_matrix)
    #      a=a_matrix[0]
    #      b=a_matrix[1]
    #      c=a_matrix[2]
    #      r=sqrt(a*a+b*b-c)

    #      #아쉬운점은 여기에 딱 하나 rules based가 추가되었는데 이유는 r이 5보다 클 경우 gui상에서 직선 구간임이 자명하지만 이를 pass로 처리해주지 않으면 원의 중점이
    #      #코스 밖에 생성되기도 하기에 이를 방지하기 위한 rules_based이다.
    #      if r>5:
    #          print("r>5",r)

    #      else:
    #          print("r<5",r)
    #          ego.point_x = a
    #          ego.point_y = b


    def run(self):
        while True:
            # try:
            self.makePath()
        
            # except IndexError:
                # print("+++++++++Planner++++++++")
            
            sleep(self.period)
