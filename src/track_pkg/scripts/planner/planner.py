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


    def makePath(self):

        
        self.perception.left_obs.sort(key = lambda x : x[2])
        self.perception.right_obs.sort(key= lambda x : x[2])

        # 왼쪽에서 인식한 러버콘수가 2개초과이면 2개만 남긴다 그 뒤 오른쪽에서 인식한 러버콘 수가 2개 초과이면 2개만 남긴다.

        if len(self.perception.left_obs) > 2:
            self.perception.left_obs = self.perception.left_obs[0:2]   

        if len(self.perception.right_obs) > 2:
            self.perception.right_obs=self.perception.right_obs[0:2]

        # 해당 러버콘 수에 따라 분기문을 나눈다. -> 0개 1개일땐 pass, 2개 일땐 secondCOM, 3개,4개 일땐 fouthCOM 사용
        if len(self.perception.left_obs)+len(self.perception.right_obs) == 0:
            self.ego.percep_state =""

            pass

        elif len(self.perception.left_obs)+len(self.perception.right_obs) == 1:
            self.firstCOM(self.perception.left_obs, self.perception.right_obs)
            self.ego.percep_state =""



        elif len(self.perception.left_obs)+len(self.perception.right_obs) == 2:
            self.secondCOM(self.perception.left_obs, self.perception.right_obs)


        else:
            #self.cal_circul(self.perception.left_obs, self.perception.right_obs)
            self.fouthCOM(self.perception.left_obs, self.perception.right_obs)

    def firstCOM(self, left_points, right_points):
        
        if len(left_points) == 1:
            self.ego.percep_state = "y_turn"
        if len(right_points) == 1:
            self.ego.percep_state = "b_turn"
      
    def secondCOM(self, left_points, right_points):
            
        if len(left_points) == 2:
            self.ego.percep_state = "y_turn"

        elif len(right_points) == 2:
            self.ego.percep_state = "b_turn"

        
        
        else:
            self.ego.point_x = (left_points[0][0] + right_points[0][0]) / 2
            self.ego.point_y = (left_points[0][1] + right_points[0][1]) / 2



    def fouthCOM(self, left_points,right_points):
        self.ego.percep_state =""
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


        self.ego.point_x=(lpointx+rpointx)/(len(left_points)+len(right_points))
        self.ego.point_y=(lpointy+rpointy)/(len(left_points)+len(right_points))
        # print("4self.ego.point_x : ",self.ego.point_x)
        # print("4self.ego.point_y : ",self.ego.point_y)

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
