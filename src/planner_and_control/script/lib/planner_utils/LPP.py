# -*- coding: utf-8 -*-

import rospy
import rospkg
from nav_msgs.msg import Path,Odometry
from geometry_msgs.msg import PoseStamped,Point
from std_msgs.msg import Float64,Int16,Float32MultiArray
import numpy as np
from math import cos,sin,sqrt,pow,atan2,pi
import tf


def LatticePlanner(ref_local_path, ego_status):
    out_path=[]
    
    #look_distance=int(ego_speed*3.6*0.8*2)
    look_distance = 5
    ego_x = ego_status[0]
    ego_y = ego_status[1]
    ego_speed = ego_status[2]

    #print(f"look_distance : {look_distance}")
    #print(f"ref_local_path.ego_x:{ref_local_path.ego_x}")
    #print(f"ego_status:{ego_status}")


    if look_distance < 2 :
        look_distance=2     
    if look_distance > 9 :
        look_distance=9  

    if len(ref_local_path.ego_x) > look_distance :
        global_ref_start_point = (ref_local_path.ego_x[0],ref_local_path.y[0])
        global_ref_start_neego_xt_point = (ref_local_path.ego_x[1],ref_local_path.y[1])
        global_ref_end_point = (ref_local_path.ego_x[look_distance],ref_local_path.y[look_distance])
        
        theta = atan2(global_ref_start_neego_xt_point[1]-global_ref_start_point[1],global_ref_start_neego_xt_point[0]-global_ref_start_point[0])
        translation = [global_ref_start_point[0],global_ref_start_point[1]]

        t = np.array([[cos(theta), -sin(theta),translation[0]],[sin(theta),cos(theta),translation[1]],[0,0,1]])
        det_t = np.array([[t[0][0],t[1][0],-(t[0][0]*translation[0]+t[1][0]*translation[1])   ],[t[0][1],t[1][1],-(t[0][1]*translation[0]+t[1][1]*translation[1])   ],[0,0,1]])



        world_end_point = np.array([[global_ref_end_point[0]],[global_ref_end_point[1]],[1]])
        local_end_point = det_t.dot(world_end_point)
        world_ego_vehicle_position = np.array([[ego_status[0]],[ego_status[1]],[1]])
        local_ego_vehicle_position = det_t.dot(world_ego_vehicle_position)
        lane_off_set = [1.2 , 1, 0, 1, 1.2]
        local_lattice_points = []
        for i in range(len(lane_off_set)):
            local_lattice_points.append([local_end_point[0][0],local_end_point[1][0]+lane_off_set[i],1])
            


        for end_point in local_lattice_points :
            lattice_path = Path()
            lattice_path.header.frame_id = 'map'
            ego_x = []
            y = []
            ego_x_interval = 0.5
            ego_xs = 0
            ego_xf = end_point[0]
            ps = local_ego_vehicle_position[1][0]

            pf = end_point[1]
            ego_x_num = ego_xf/ego_x_interval

            for i in range(ego_xs,int(ego_x_num)) : 
                ego_x.append(i*ego_x_interval)
            
            a = [0.0,0.0,0.0,0.0]
            a[0] = ps
            a[1] = 0
            a[2] = 3.0*(pf-ps)/(ego_xf*ego_xf)
            a[3] = -2.0*(pf-ps)/(ego_xf*ego_xf*ego_xf)

            for i in ego_x:
                result = a[3]*i*i*i+a[2]*i*i+a[1]*i+a[0]
                y.append(result)


            for i in range(0,len(y)) :
                local_result = np.array([[ego_x[i]],[y[i]],[1]])
                global_result = t.dot(local_result)

                read_pose = PoseStamped()
                read_pose.pose.position.ego_x = global_result[0][0]
                read_pose.pose.position.y = global_result[1][0]
                read_pose.pose.position.z = 0
                read_pose.pose.orientation.ego_x = 0
                read_pose.pose.orientation.y = 0
                read_pose.pose.orientation.z = 0
                read_pose.pose.orientation.w = 1
                lattice_path.poses.append(read_pose)

            out_path.append(lattice_path)
        
        add_point_size = int(ego_speed*2*3.6)
        #print('add point',add_point_size)
        if add_point_size > len(ref_local_path.ego_x)-2:
            add_point_size = len(ref_local_path.ego_x)
        elif add_point_size < 10 :
            add_point_size = 10
        
        
         
        for i in range(look_distance,add_point_size):
            if i+1 < len(ref_local_path.ego_x):
                tmp_theta = atan2(ref_local_path.y[i+1]-ref_local_path.y[i],ref_local_path.ego_x[i+1]-ref_local_path.ego_x[i])
                
                tmp_translation = [ref_local_path.ego_x[i],ref_local_path.y[i]]
                tmp_t = np.array([[cos(tmp_theta), -sin(tmp_theta),tmp_translation[0]],[sin(tmp_theta),cos(tmp_theta),tmp_translation[1]],[0,0,1]])
                tmp_det_t = np.array([[tmp_t[0][0],tmp_t[1][0],-(tmp_t[0][0]*tmp_translation[0]+tmp_t[1][0]*tmp_translation[1])   ],[tmp_t[0][1],tmp_t[1][1],-(tmp_t[0][1]*tmp_translation[0]+tmp_t[1][1]*tmp_translation[1])   ],[0,0,1]])

                for lane_num in range(len(lane_off_set)) :
                    local_result = np.array([[0],[lane_off_set[lane_num]],[1]])
                    global_result = tmp_t.dot(local_result)

                    read_pose=PoseStamped()
                    read_pose.pose.position.ego_x = global_result[0][0]
                    read_pose.pose.position.y = global_result[1][0]
                    read_pose.pose.position.z = 0
                    read_pose.pose.orientation.ego_x = 0
                    read_pose.pose.orientation.y = 0
                    read_pose.pose.orientation.z = 0
                    read_pose.pose.orientation.w = 1
                    out_path[lane_num].poses.append(read_pose)  

    return out_path
