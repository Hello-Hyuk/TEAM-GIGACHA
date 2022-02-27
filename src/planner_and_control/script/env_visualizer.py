import rospy

from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.read_global_path import read_global_path
from lib.controller_utils.state import State

from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
from nav_msgs.msg import Odometry
from planner_and_control.msg import Local
from planner_and_control.msg import Path

class environmentVisualizer:
    def __init__(self):
        
        # init node
        rospy.init_node("Environment_Visualizer", anonymous=False)
        
        # Subscriber
        rospy.Subscriber('/pose', Local, self.pose_callback)
        rospy.Subscriber('/trajectory', Path, self.globalpath_callback)
        
        # Publisher
        self.vis_global_path_pub = rospy.Publisher("/vis_global_path", PointCloud, queue_size=1)
        self.vis_trajectory_pub = rospy.Publisher("/vis_trajectory", PointCloud, queue_size=1)
        self.vis_pose_pub = rospy.Publisher("/vis_pose", Odometry, queue_size=1)

        self.vis_global_path = PointCloud()
        self.vis_global_path.header.frame_id = "map"
        
        self.vis_trajectory = PointCloud()
        self.vis_trajectory.header.frame_id = "map"
        
        self.vis_pose = Odometry()
        self.vis_pose.header.frame_id = "map"

        # self.obsmap_pub = rospy.Publisher("/vis_map", PointCloud, queue_size=1)
        # self.obsmap = PointCloud()
        # self.obsmap.header.frame_id = "map"
    

        # self.local_path_pub = rospy.Publisher("/vis_local_path", PointCloud, queue_size=1)
        # self.obs_pub = rospy.Publisher("/vis_obs_pub", PointCloud, queue_size=1)
        # self.target_pub = rospy.Publisher("/vis_target", PointCloud, queue_size=1)

        # self.vis_local_path = PointCloud()
        # self.vis_local_path.header.frame_id = "map"


        # self.obs = PointCloud()
        # self.obs.header.frame_id = "map"

        # self.target = PointCloud()
        # self.target.header.frame_id = "map"
        
    def pose_callback(self, msg):
        ppoint = Point32()
        ppoint.x = msg.x
        ppoint.y = msg.y
        ppoint.z = 0
        self.vis_pose.pose.pose.position.x = ppoint.x
        self.vis_pose.pose.pose.position.y = ppoint.y
        # self.vis_trajectory.header.stamp = rospy.Time.now()
        self.vis_trajectory.points.append(ppoint)
        
    def globalpath_callback(self, msg):
        global_path = PointCloud()
        for i in range(len(msg.x)):
            gpoints = Point32()
            gpoints.x = msg.x
            gpoints.y = msg.y
            gpoints.z = 0
            global_path.points.append(gpoints)
        self.vis_global_path.points = global_path.points

    def run(self):
        print(f"Publishing maps for visualization")
        self.vis_global_path.header.stamp = rospy.Time.now()
        self.vis_global_path_pub.publish(self.vis_global_path)
        
        self.vis_global_path.header.stamp = rospy.Time.now()
        self.vis_trajectory_pub.publish(self.vis_trajectory)

        self.vis_pose.header.stamp = rospy.Time.now()
        self.vis_pose_pub.publish(self.vis_pose)
        
        # self.obsmap.points = self.ego.obs_map.points
        # self.obsmap.header.stamp = rospy.Time.now()
        # self.obsmap_pub.publish(self.obsmap)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    vv = environmentVisualizer()
    rate = rospy.Rate(10)
    while True:
        vv.run()
        rate.sleep()
