import threading
import rospy
from final_pkg.msg import Perception
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import Int32
from vision_msgs.msg import Detection2DArray
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import PoseArray

class Perception_():
   def __init__(self):
      # rospy.Subscriber("/input", Perception, self.input_callback)
      # rospy.Subscriber("/sign", Detection2DArray, self.sign_callback)
      rospy.Subscriber("/obstacles_markers", MarkerArray, self.lidar_callback)
      rospy.Subscriber("/traffic_bbox", Detection2DArray, self.traffic_callback)
      rospy.Subscriber("/Parking_num", Int32, self.parking_callback)
      # rospy.Subscriber("/target_points", PointCloud, self.delivery_callback)
      rospy.Subscriber("/pcd", PoseArray, self.delivery_callback)
      rospy.Subscriber("/sign_bbox", Detection2DArray, self.delivery_sign_callback)


      self.objx = []
      self.objy = []
      self.objw = []
      self.objh = []
      self.tmp_objx = []
      self.tmp_objy = []
      self.tmp_objw = []
      self.tmp_objh = []
      self.tred = False
      self.tyellow = False
      self.tleft = False
      self.tgreen = False
      self.tmp_lidar_lock = threading.Lock()
      self.delivery_lidar_lock = threading.Lock()
      self.lidar_lock = threading.Lock()
      self.signname = ""
      self.parking_num = ""
      self.target = 0

      #for input_callback
      self.signx = 0
      self.signy = 0
      self.B_x = [0,0,0]
      self.B_y = [0,0,0]
      self.first_sign = 0
      self.second_sign = 0
      self.third_sign = 0

      self.sign_num = 0

   # # with tracking
   # def delivery_callback(self, msg):
   #    # pickup
   #    print("===================PICKUP===================:{0}".format(len(msg.points)))
   #    if (len(msg.points) == 1):
   #       if msg.points[0].z == 0:
   #          self.target = 1
   #       elif msg.points[0].z == 1:
   #          self.target = 2
   #       elif msg.points[0].z == 2:
   #          self.target = 2
   #       self.signx = msg.points[0].x
   #       self.signy = msg.points[0].y
   #    elif (len(msg.points) == 3):
   #       for i in range(3):
   #          self.B_x[i] = msg.points[i].x
   #          self.B_y[i] = msg.points[i].y
   #       self.first_sign = msg.points[0].z
   #       self.second_sign = msg.points[1].z
   #       self.third_sign = msg.points[2].z

   # without tracking
   def delivery_callback(self, msg):
      # pickup
      # print("===================PICKUP===================:{0}".format(len(msg.poses)))

      self.delivery_lidar_lock.acquire()
      self.sign_num = len(msg.poses)
      if len(msg.poses) != 0:
         if int(msg.poses[0].orientation.w) == 0:
            self.target = 1
            self.signx = msg.poses[0].orientation.x
            self.signy = msg.poses[0].orientation.y
         elif int(msg.poses[0].orientation.w) == 1:
            self.target = 2
            self.signx = msg.poses[0].orientation.x
            self.signy = msg.poses[0].orientation.y
         elif int(msg.poses[0].orientation.w) == 2:
            self.target = 3
            self.signx = msg.poses[0].orientation.x
            self.signy = msg.poses[0].orientation.y

         for i in range(len(msg.poses)):
            if int(msg.poses[i].orientation.w) == 3:
               self.B_x[0] = msg.poses[i].orientation.x
               self.B_y[0] = msg.poses[i].orientation.y
         
            elif int(msg.poses[i].orientation.w) == 4:
               self.B_x[1] = msg.poses[i].orientation.x
               self.B_y[1] = msg.poses[i].orientation.y

            elif int(msg.poses[i].orientation.w) == 5:
               self.B_x[2] = msg.poses[i].orientation.x
               self.B_y[2] = msg.poses[i].orientation.y
      self.delivery_lidar_lock.release()
      # print('perception : ')
      # print(self.B_x[0], self.B_x[1], self.B_x[2] )
         # self.first_sign = int(msg.poses[0].orientation.w)
         # self.second_sign = int(msg.poses[1].orientation.w)
         # self.third_sign = int(msg.poses[2].orientation.w)

   def delivery_sign_callback(self, msg):
      pass
   #    if (len(msg.detections) == 3):
   #       self.first_sign = msg.detections[0].results[0].id
   #       self.second_sign = msg.detections[1].results[0].id
   #       self.third_sign = msg.detections[2].results[0].id

   
   def lidar_callback(self, msg):
      if len(msg.markers) != 0:
         self.tmp_lidar_lock.acquire()
         tmp_objx = []
         tmp_objy = []
         tmp_objw = []
         tmp_objh = []
         for i in range(len(msg.markers)):
            tmp_objx.append(msg.markers[i].pose.position.x + 1.15)
            tmp_objy.append(msg.markers[i].pose.position.y)
            tmp_objw.append(msg.markers[i].scale.y)
            tmp_objh.append(msg.markers[i].scale.x)
         self.tmp_objx = tmp_objx
         self.tmp_objy = tmp_objy
         self.tmp_objw = tmp_objw
         self.tmp_objh = tmp_objh
         self.tmp_lidar_lock.release()
      else:
         self.tmp_objx = []
         self.tmp_objy = []
         self.tmp_objw = []
         self.tmp_objh = []

   def traffic_callback(self, msg):
      if len(msg.detections) > 0:
         if msg.detections[0].results[0].id == 0 or msg.detections[0].results[0].id == 1:
            self.tred = True
            self.tyellow = False
            self.tleft = False
            self.tgreen = False
         elif msg.detections[0].results[0].id == 2 or msg.detections[0].results[0].id == 3:
            self.tred = False
            self.tyellow = True
            self.tleft = False
            self.tgreen = False
         elif msg.detections[0].results[0].id == 4 or msg.detections[0].results[0].id == 5:
            self.tred = False
            self.tyellow = False
            self.tleft = False
            self.tgreen = True
         elif msg.detections[0].results[0].id == 6:
            self.tred = True
            self.tyellow = False
            self.tleft = True
            self.tgreen = False
         elif msg.detections[0].results[0].id == 7:
            self.tred = False
            self.tyellow = False
            self.tleft = True
            self.tgreen = True

   def parking_callback(self, msg):
      self.parking_num = msg.data
      # self.parking_num = 4


   # def sign_callback(self, msg):
   #    for i in range(len(msg.detections)):
   #       if len(msg.detections) == 3 and  2 < msg.detections[i].results[0].id < 6:
   #          self.first_sign = msg.detections[0].results[0].id
   #          self.second_sign = msg.detections[1].results[0].id
   #          self.third_sign = msg.detections[2].results[0].id
            # print(self.first_sign, " ", self.second_sign, " ", self.third_sign)
         # if msg.detections[i].results[0].id == 0:
         #    self.signname = "static_obstacle_detected"   #A1
         #    # self.target = "B1"
         # elif msg.detections[i].results[0].id == 1:
         #    self.signname = "turn_left_traffic_light" #A2
         #    # self.target = "B2"
         # elif msg.detections[i].results[0].id == 2:
         #    self.signname = "turn_right_traffic_light" #A3
         #       # self.target = "B3"

      # if msg.detections[i].results[0].id == 0:
      #    self.signname = "static_obstacle_detected"   #A1
      #    # self.target = "B1"
      # elif msg.detections[i].results[0].id == 1:
      #    self.signname = "turn_left_traffic_light" #A2
      #    # self.target = "B2"
      # elif msg.detections[i].results[0].id == 2:
      #    self.signname = "turn_right_traffic_light" #A3
            # self.target = "B3"
      # elif msg.detections[i].results[0].id == 3:
      #    self.signname = "AEB" #B1
      # elif msg.detections[i].results[0].id == 4:
      #    self.signname = "non_traffic_right" #B2
      # elif msg.detections[i].results[0].id == 5:
      #     self.signname = "parking"  #B3*