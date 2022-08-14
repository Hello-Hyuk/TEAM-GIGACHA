#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from math import sqrt
import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import MarkerArray, Marker
import itertools as it

class path_maker:
    def __init__(self):
        # make node
        rospy.init_node("narrow_path_maker", anonymous=False)

        #subscriber
        rospy.Subscriber("obstacles_markers", MarkerArray, self.makePath)
        # publisher
        self.pub = rospy.Publisher('target_point', Point, queue_size=10)
        self.vis_pub = rospy.Publisher('target_point_vis', Marker, queue_size=10)

        # lookahead point
        self.left_obs = []
        self.right_obs = []
        self.obstacles = []
        self.obstacles_right=[]
        self.obstacles_left=[]
        self.nearest_obstacles = []
        self.target_point = Point()
        # visualize용 메세지
        self.target_point_vis = Marker()

        rospy.spin()


    def calc_distance(self, obs_x, obs_y):
        p1 = [0, 0]
        p2 = [obs_x, obs_y]
        dis = sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p1, p2)))
        return dis

    def makeVisual(self, target):
        self.target_point_vis.header.frame_id = "velodyne"
        self.target_point_vis.header.stamp = rospy.Time()
        self.target_point_vis.ns = "name space"
        self.target_point_vis.id = 0
        self.target_point_vis.type = 8
        self.target_point_vis.action = 0
        self.target_point_vis.pose.position.x = 0
        self.target_point_vis.pose.position.y = 0
        self.target_point_vis.pose.position.z = 0
        self.target_point_vis.pose.orientation.x = 0.0
        self.target_point_vis.pose.orientation.y = 0.0
        self.target_point_vis.pose.orientation.z = 0.0
        self.target_point_vis.pose.orientation.w = 1.0
        self.target_point_vis.scale.x = 0.5
        self.target_point_vis.scale.y = 0.5
        self.target_point_vis.scale.z = 0.5
        self.target_point_vis.color.r = 255
        self.target_point_vis.color.g = 0
        self.target_point_vis.color.b = 0
        self.target_point_vis.color.a = 0.7
        self.target_point_vis.lifetime = rospy.Duration(0.1)
        self.target_point_vis.points.append(target) # 이거로 계속 누적되면 이거를 이용해서 loop closure나 경로 점 모두 보기 가능할수도
    
    def left_right_classification(self, points):
        tmp_left_obs = []
        tmp_right_obs = []
        for point in points:
            if point[1] >= 0:
                tmp_left_obs.append(point)
            else:
                tmp_right_obs.append(point)
        return (tmp_left_obs, tmp_right_obs)


    # 하나의 점만 검출될 경우
    # 이전 스티어링 값 유지
    def singleCOM(self, points):
        pass



#method1
    # def makeCOM(self, points):
    #     x_sum = 0
    #     y_sum = 0
    #     tmp1=0
    #     tmp2=0

    #     for point in points:

    #         if point[1]<0:
    #             tmp1=tmp1+1
    #             if tmp1>=3:
    #                 pass

    #             else:
    #                 x_sum = x_sum + point[0]
    #                 y_sum = y_sum + point[1]


    #         elif point[1]>0:
    #             tmp2=tmp2+1
    #             if tmp2>=3:
    #                 pass

    #             else:
    #                 x_sum = x_sum + point[0]
    #                 y_sum = y_sum + point[1]    

    #     self.target_point.x = x_sum / len(points)
    #     self.target_point.y = y_sum / len(points)


# method2
    def makeCOM(self, points):
        x_sum = 0
        y_sum = 0
        tmp1=0
        tmp2=0
        point_L=0
        point_R=0



        for point in points:

            if point[1]<0:
                point_L=point
                point_R=0

            if point[1]>0:
                point_R=point
                point_L=0
    
            if point[1]<0:
                tmp1=tmp1+1
                if tmp1>=3:
                    x_sum = x_sum + point_L[0]+3*point_R[0]
                    y_sum = y_sum + point_L[1]+3*point_R[0]


                    

                else:
                    x_sum = x_sum + point_L[0]+point_R[0]
                    y_sum = y_sum + point_L[0]+point_R[0]


            elif point[1]>0:
                tmp2=tmp2+1
                if tmp2>=3:
                    x_sum = x_sum + 3*point_L[0]+point_R[0]
                    y_sum = y_sum + 3*point_L[1]+point_R[0]


                else:
                    x_sum = x_sum + point_L[0]+point_R[0]
                    y_sum = y_sum + point_L[0]+point_R[0]






        self.target_point.x = x_sum / len(points)
        self.target_point.y = y_sum / len(points)




    def makePath(self, msg):
        # print(type(msg))
        # 각 장애물의 중앙점 따로 저장-> obstacles의 중앙점, 거리 값 같이 계산
        
        for obs in msg.markers:
            tmp_obs_dis = self.calc_distance(obs.pose.position.x, obs.pose.position.y)
            self.obstacles.append([round(obs.pose.position.x, 2), round(obs.pose.position.y, 2), round(tmp_obs_dis, 2)])
        
        # 점 정렬 & 4개 점 filtering
        self.obstacles.sort(key = lambda x : x[2])
        if len(self.obstacles) > 4:
            self.obstacles = self.obstacles[0:4]    # 가장 거리가 짧은 4개의 점만 추출


        if len(self.obstacles) == 0:
            pass
        elif len(self.obstacles) == 1:
            self.singleCOM(self.obstacles)
        else:

            self.makeCOM(self.obstacles)
        print("self.obstacles",self.obstacles)
   

    # def makePath(self, msg):
    #     # print(type(msg))
    #     # 각 장애물의 중앙점 따로 저장-> obstacles의 중앙점, 거리 값 같이 계산
        
    #     for obs in msg.markers:
    #         tmp_obs_dis = self.calc_distance(obs.pose.position.x, obs.pose.position.y)
    #         self.obstacles.append([round(obs.pose.position.x, 2), round(obs.pose.position.y, 2), round(tmp_obs_dis, 2)])
        
    #     # 점 정렬 & 4개 점 filtering
    #     self.obstacles.sort(key = lambda x : x[2])
    #     if len(self.obstacles) > 4:
    #         self.obstacles = self.obstacles[0:4]    # 가장 거리가 짧은 4개의 점만 추출


    #     if len(self.obstacles) == 0:
    #         pass
    #     elif len(self.obstacles) == 1:
    #         self.singleCOM(self.obstacles)
    #     else:
    #         self.makeCOM(self.obstacles)
    #     print("self.obstacles",self.obstacles)    

        self.makeVisual(self.target_point)
        self.vis_pub.publish(self.target_point_vis)
        self.pub.publish(self.target_point)
        self.obstacles.clear()
        self.target_point_vis.points.clear()
        

if __name__ == "__main__":
    print("PATH_MAKER_ON")
    path_maker()
