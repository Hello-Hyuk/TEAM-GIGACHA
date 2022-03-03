from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from math import cos,sin,sqrt,pow,atan2,pi



def findLocalPath(path,ego):
    out_path=Path()
    current_x=ego.x
    current_y=ego.y
    current_waypoint=0
    min_dis=float('inf')

    for i in range(len(path.x)) :
        dx=current_x - path.x[i]
        dy=current_y - path.y[i]
        dis=sqrt(dx*dx + dy*dy)
        if dis < min_dis :
            min_dis=dis
            current_waypoint=i

    print(min_dis)

    if current_waypoint+50 > len(path.x) :
        last_local_waypoint= len(path.x)
    else :
        last_local_waypoint=current_waypoint+50


    #out_path.header.frame_id='map'
    for i in range(current_waypoint,last_local_waypoint) :
        # tmp_pose=Path()
        # tmp_pose.x=path.x[i]
        # tmp_pose.poses[i].pose.position.y=path.y[i]

        read_pose=PoseStamped()

        read_pose.pose.position.x = path.x[i]
        read_pose.pose.position.y = path.y[i]
        read_pose.pose.position.z = 0
        read_pose.pose.orientation.x=0
        read_pose.pose.orientation.y=0
        read_pose.pose.orientation.z=0
        read_pose.pose.orientation.w=1

        # for i in range(len(msg.x)):
        #     read_pose=PoseStamped()
        #     read_pose.pose.position.x = msg.x[i]
        #     read_pose.pose.position.y = msg.y[i]
        #     read_pose.pose.position.z = 0
        #     read_pose.pose.orientation.x=0
        #     read_pose.pose.orientation.y=0
        #     read_pose.pose.orientation.z=0
        #     read_pose.pose.orientation.w=1

        # global_path.poses.append(read_pose)  

        out_path.poses.append(read_pose)

    return out_path
