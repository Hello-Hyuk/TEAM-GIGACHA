# -*- coding: utf-8 -*-

import rospy
import rospkg
from nav_msgs.msg import Path,Odometry
from geometry_msgs.msg import PoseStamped,Point
from std_msgs.msg import Float64,Int16,Float32MultiArray
import numpy as np
from math import cos,sin,sqrt,pow,atan2,pi
import tf



def LatticePlanner(ref_path,global_vaild_object,vehicle_status,vehicle_speed,current_lane):
    out_path=[]
    selected_lane=-1
    lattic_current_lane=current_lane
    look_distance=int(vehicle_speed*3.6*0.8*2)
    print(f"look_distance : {look_distance}")

    if look_distance < 20 :
        look_distance=20     
    if look_distance > 90 :
        look_distance=90  
    if len(ref_path)>look_distance :
        global_ref_start_point=(ref_path.x[0],ref_path.y[0])
        global_ref_start_next_point=(ref_path.x[1],ref_path.y[1])
        global_ref_end_point=(ref_path.x[look_distance],ref_path.y[look_distance])
        
        theta=atan2(global_ref_start_next_point[1]-global_ref_start_point[1],global_ref_start_next_point[0]-global_ref_start_point[0])
        translation=[global_ref_start_point[0],global_ref_start_point[1]]

        t=np.array([[cos(theta), -sin(theta),translation[0]],[sin(theta),cos(theta),translation[1]],[0,0,1]])
        det_t=np.array([[t[0][0],t[1][0],-(t[0][0]*translation[0]+t[1][0]*translation[1])   ],[t[0][1],t[1][1],-(t[0][1]*translation[0]+t[1][1]*translation[1])   ],[0,0,1]])



        world_end_point=np.array([[global_ref_end_point[0]],[global_ref_end_point[1]],[1]])
        local_end_point=det_t.dot(world_end_point)
        world_ego_vehicle_position=np.array([[vehicle_status[0]],[vehicle_status[1]],[1]])
        local_ego_vehicle_position=det_t.dot(world_ego_vehicle_position)
        lane_off_set=[1.2,0]
        local_lattice_points=[]
        for i in range(len(lane_off_set)):
            local_lattice_points.append([local_end_point[0][0],local_end_point[1][0]+lane_off_set[i],1])
            


        for end_point in local_lattice_points :
            lattice_path=Path()
            lattice_path.header.frame_id='map'
            x=[]
            y=[]
            x_interval=0.5
            xs=0
            xf=end_point[0]
            ps=local_ego_vehicle_position[1][0]

            pf=end_point[1]
            x_num=xf/x_interval

            for i in range(xs,int(x_num)) : 
                x.append(i*x_interval)
            
            a=[0.0,0.0,0.0,0.0]
            a[0]=ps
            a[1]=0
            a[2]=3.0*(pf-ps)/(xf*xf)
            a[3]=-2.0*(pf-ps)/(xf*xf*xf)

            for i in x:
                result=a[3]*i*i*i+a[2]*i*i+a[1]*i+a[0]
                y.append(result)


            for i in range(0,len(y)) :
                local_result=np.array([[x[i]],[y[i]],[1]])
                global_result=t.dot(local_result)

                read_pose=PoseStamped()
                read_pose.pose.position.x=global_result[0][0]
                read_pose.pose.position.y=global_result[1][0]
                read_pose.pose.position.z=0
                read_pose.pose.orientation.x=0
                read_pose.pose.orientation.y=0
                read_pose.pose.orientation.z=0
                read_pose.pose.orientation.w=1
                lattice_path.poses.append(read_pose)

            out_path.append(lattice_path)
        
        add_point_size=int(vehicle_speed*2*3.6)
        print('add point',add_point_size)
        if add_point_size>len(ref_path)-2:
            add_point_size=len(ref_path)
        elif add_point_size<10 :
            add_point_size=10
        
        
         
        for i in range(look_distance,add_point_size):
            if i+1 < len(ref_path):
                tmp_theta=atan2(ref_path.y[i+1]-ref_path.y[i],ref_path.x[i+1]-ref_path.x[i])
                
                tmp_translation=[ref_path.x[i],ref_path.y[i]]
                tmp_t=np.array([[cos(tmp_theta), -sin(tmp_theta),tmp_translation[0]],[sin(tmp_theta),cos(tmp_theta),tmp_translation[1]],[0,0,1]])
                tmp_det_t=np.array([[tmp_t[0][0],tmp_t[1][0],-(tmp_t[0][0]*tmp_translation[0]+tmp_t[1][0]*tmp_translation[1])   ],[tmp_t[0][1],tmp_t[1][1],-(tmp_t[0][1]*tmp_translation[0]+tmp_t[1][1]*tmp_translation[1])   ],[0,0,1]])

                for lane_num in range(len(lane_off_set)) :
                    local_result=np.array([[0],[lane_off_set[lane_num]],[1]])
                    global_result=tmp_t.dot(local_result)

                    read_pose=PoseStamped()
                    read_pose.pose.position.x=global_result[0][0]
                    read_pose.pose.position.y=global_result[1][0]
                    read_pose.pose.position.z=0
                    read_pose.pose.orientation.x=0
                    read_pose.pose.orientation.y=0
                    read_pose.pose.orientation.z=0
                    read_pose.pose.orientation.w=1
                    out_path[lane_num].poses.append(read_pose)

        lane_weight=[5,0] #reference path 
        collision_bool=[False,False]

        if len(global_vaild_object)>0:

            for path_num in range(len(out_path)) :
                        
                for path_pos in out_path[path_num].poses :

                    dis= sqrt(pow(global_vaild_object.x,2)+pow(global_vaild_object.y,2))
   
                    if dis<7:
                        collision_bool[path_num]=True
                        lane_weight[path_num]=lane_weight[path_num]+100
                        break
            
        
        else :
            print("No Obstacle")
    
        selected_lane=lane_weight.index(min(lane_weight))
        print(lane_weight,selected_lane)
        all_lane_collision=True
        
    else :
        print("NO Reference Path")
        selected_lane=-1    

    return out_path,selected_lane
