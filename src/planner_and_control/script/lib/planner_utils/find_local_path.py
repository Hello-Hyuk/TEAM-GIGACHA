from planner_and_control.msg import Path
from math import cos,sin,sqrt,pow,atan2,pi



def findLocalPath(path,ego):
    out_path=Path()
    current_x=ego.x
    current_y=ego.y
    current_waypoint=0
    min_dis=float('inf')

    for i in range(len(path.x)) :
        dx=current_x - path.x[i]
        dy=current_y - path.x[i]
        dis=sqrt(dx*dx + dy*dy)
        if dis < min_dis :
            min_dis=dis
            current_waypoint=i


    if current_waypoint+50 > len(path.x) :
        last_local_waypoint= len(path.x)
    else :
        last_local_waypoint=current_waypoint+50



    #out_path.header.frame_id='map'
    for i in range(current_waypoint,last_local_waypoint) :
        tmp_pose=Path()
        tmp_pose.x=path.x[i]
        tmp_pose.y=path.y[i]
        out_path.poses.append(tmp_pose)

    return out_path
