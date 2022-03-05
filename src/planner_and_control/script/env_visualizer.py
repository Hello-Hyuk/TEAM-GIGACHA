import rospy

from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler

from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32, PoseStamped
from nav_msgs.msg import Odometry, Path
from planner_and_control.msg import Local
from planner_and_control.msg import Path as customPath

class environmentVisualizer:
    def __init__(self):
        
        # init node
        rospy.init_node("Environment_Visualizer", anonymous=False)
        
        # Subscriber
        rospy.Subscriber('/pose', Local, self.pose_callback)
        rospy.Subscriber('/global_path', customPath, self.globalpath_callback)
        rospy.Subscriber('/local_path', customPath, self.localpath_callback)
        
        # Publisher
        # self.vis_global_path_pub = rospy.Publisher("/vis_global_path", PointCloud, queue_size=1) # using pointcloud
        self.vis_global_path_pub = rospy.Publisher("/vis_global_path", Path, queue_size=1) # using path
        self.vis_local_path_pub = rospy.Publisher("/vis_local_path", Path, queue_size=1) # using path
        
        self.vis_trajectory_pub = rospy.Publisher("/vis_trajectory", PointCloud, queue_size=1)
        self.vis_pose_pub = rospy.Publisher("/vis_pose", Odometry, queue_size=1)
        

        # self.vis_global_path = PointCloud() # using pointcloud
        self.vis_global_path = Path() # using path
        self.vis_global_path.header.frame_id = "map"
        
        self.vis_local_path = Path() # using path
        self.vis_local_path.header.frame_id = "map"

        self.vis_local_path = Path() # using path
        self.vis_local_path.header.frame_id = "map"
        
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

        # car heading
        heading = PoseStamped()
        heading.header.pose = msg.heading
        self.vis_pose.pose.pose.orientation.w = heading.header.pose
        
    def globalpath_callback(self, msg):
        global_path = Path()
        for i in range(len(msg.x)):
            read_pose=PoseStamped()
            read_pose.pose.position.x = msg.x[i]
            read_pose.pose.position.y = msg.y[i]
            read_pose.pose.position.z = 0
            read_pose.pose.orientation.x=0
            read_pose.pose.orientation.y=0
            read_pose.pose.orientation.z=0
            read_pose.pose.orientation.w=1
            global_path.poses.append(read_pose)  
        self.vis_global_path.poses = global_path.poses
        
        # global_path = PointCloud()
        # for i in range(len(msg.x)):
        #     gpoints = Point32()
        #     gpoints.x = msg.x[i]
        #     gpoints.y = msg.y[i]
        #     gpoints.z = 0
        #     global_path.points.append(gpoints)
        # self.vis_global_path.points = global_path.points
        
    def localpath_callback(self, msg):
        local_path = Path()
        for i in range(len(msg.x)):
            read_pose=PoseStamped()
            read_pose.pose.position.x = msg.x[i]
            read_pose.pose.position.y = msg.y[i]
            read_pose.pose.position.z = 0
            read_pose.pose.orientation.x=0
            read_pose.pose.orientation.y=0
            read_pose.pose.orientation.z=0
            read_pose.pose.orientation.w=1
            local_path.poses.append(read_pose)  
        self.vis_local_path.poses = local_path.poses

    def run(self):
        print(f"Publishing maps for visualization")
        self.vis_global_path.header.stamp = rospy.Time.now()
        self.vis_global_path_pub.publish(self.vis_global_path)
        
        self.vis_local_path.header.stamp = rospy.Time.now()
        self.vis_local_path_pub.publish(self.vis_local_path)

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
