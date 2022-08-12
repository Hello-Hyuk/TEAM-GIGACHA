import threading
import rospy
# from planner_and_control.msg import Perception
from visualization_msgs.msg import MarkerArray, Marker
from std_msgs.msg import Int32, Int64
from vision_msgs.msg import Detection2DArray
# from planner_and_control.msg import Perception

class Perception_():
   def __init__(self):
      self.id_check = False

      # rospy.Subscriber("/input", Perception, self.input_callback)
      rospy.Subscriber("/obstacles_markers", MarkerArray, self.lidar_callback)
      rospy.Subscriber("/sign", Detection2DArray, self.sign_callback)
      rospy.Subscriber("/traffic", Detection2DArray, self.traffic_callback)
      rospy.Subscriber("/Parking_num", Int32, self.parking_callback)
      # rospy.Subscriber("/bbox1", Detection2DArray, self.camera_callback)

      self.signx = 0
      self.signy = 0
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
      self.lidar_lock = threading.Lock()
      self.signname = "driving"
      self.parking_num = ""
      self.target = 0


      #for input_callback
      self.B_signs = {"B1": 0, "B2": 0, "B3":0}
      self.B_x = {"B1":0, "B2":0, "B3":0}
      self.B_y = {"B1":0, "B2":0, "B3":0}

   def input_callback(self, msg):
      #first
      if msg.A_target == 0:
         self.target = 1
      elif msg.A_target == 1:
         self.target = 2
      elif msg.A_target == 2:
         self.target = 3
      self.signx = msg.A_objx
      self.signy = msg.A_objy
      #second
      count = 0
      for i in self.B_signs.keys():
         self.B_signs[i] = msg.B_bbox_size[count]
         self.B_x[i] = msg.B_target_x[count]
         self.B_y[i] = msg.B_target_y[count]
         count = count+1

   def lidar_callback(self, msg):
      if len(msg.markers) != 0:
         self.tmp_lidar_lock.acquire()
         tmp_objx = []
         tmp_objy = []
         tmp_objw = []
         tmp_objh = []
         for i in range(len(msg.markers)):
            tmp_objx.append(msg.markers[i].pose.position.x+0.8)
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

      
   def sign_callback(self, msg):
      print("msg.detection[i].results[0].id")
      for i in range(len(msg.detections)):
         if msg.detections[i].results[0].id == 0:
            self.signname = "delivery"   #A1
            self.target = "B1"
         elif msg.detections[i].results[0].id == 1:
            self.signname = "delivery" #A2
            self.target = "B2"
         elif msg.detections[i].results[0].id == 2:
            self.signname = "delivery" #A3
            self.target = "B3"
         elif msg.detections[i].results[0].id == 3:
            self.signname = "AEB" #B1
         elif msg.detections[i].results[0].id == 4:
            self.signname = "non_traffic_right" #B2
         elif msg.detections[i].results[0].id == 5:
            self.signname = "parking"  #B3

   def traffic_callback(self, msg):
      print("===========================================")
      if msg.detection[i].results[0].id == 0 or msg.detection[i].results[0].id == 1:
         self.tred = True
         self.tyellow = False
         self.tleft = False
         self.tgreen = False
      elif msg.detection[i].results[0].id == 2 or msg.detection[i].results[0].id == 3:
         self.tred = False
         self.tyellow = True
         self.tleft = False
         self.tgreen = False
      elif msg.detection[i].results[0].id == 4 or msg.detection[i].results[0].id == 5:
         self.tred = False
         self.tyellow = False
         self.tleft = False
         self.tgreen = True
      elif msg.detection[i].results[0].id == 6:
         self.tred = True
         self.tyellow = False
         self.tleft = True
         self.tgreen = False
      elif msg.detection[i].results[0].id == 7:
         self.tred = False
         self.tyellow = False
         self.tleft = True
         self.tgreen = True

   def parking_callback(self, msg):
      self.parking_num = msg.data
