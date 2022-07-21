import threading
import rospy
from planner_and_control.msg import Perception
from visualization_msgs.msg import MarkerArray, Marker
from vision_msgs.msg import Detection2DArray

class Perception_():
   def __init__(self):
      self.id_check = False

      #rospy.Subscriber("/input", Perception, self.input_callback)
      rospy.Subscriber("/obstacles_markers", MarkerArray, self.lidar_callback)
      rospy.Subscriber("/sign", Detection2DArray, self.sign_callback)
      rospy.Subscriber("/traffic", Detection2DArray, self.traffic_callback)

      self.signx = []
      self.signy = []
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
      # self.signname = "static_obstacle"
      self.signname = "go"
      self.tmp_lidar_lock = threading.Lock()
      self.lidar_lock = threading.Lock()


   def input_callback(self, msg):
      self.signx = msg.signx
      self.signy = msg.signy
      self.objx = msg.objx
      self.objy = msg.objy
      self.objr = msg.objr
      self.tred = msg.tred
      self.tyellow = msg.tyellow
      self.tleft = msg.tleft
      self.tgreen = msg.tgreen
      self.signname = msg.signname

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
      for i in range(len(msg.detections)):
         if msg.detections[i].results[0].id == 3:
            self.signname = "turn_left_traffic_light"   #A1
         elif msg.detections[i].results[0].id == 1:
            self.signname = "turn_right_traffic_light" #A2
         elif msg.detections[i].results[0].id == 2:
            self.signname = "static_obstacle" #A3
         elif msg.detections[i].results[0].id == 0:
            self.signname = "AEB" #B1
         elif msg.detections[i].results[0].id == 4:
            self.signname = "non_traffic_right" #B2
         # elif msg.detections[i].results[0].id == 5:
         #    self.signname = "parking"  #B3

   def traffic_callback(self, msg):
      for i in range(len(msg.detections)):
         if msg.detections[i].results[0].id == 6 or msg.detections[i].results[0].id == 7:
            self.tred = True
            self.tyellow = False
            self.tleft = False
            self.tgreen = False
         elif msg.detections[i].results[0].id == 8 or msg.detections[i].results[0].id == 9:
            self.tred = False
            self.tyellow = True
            self.tleft = False
            self.tgreen = False
         elif msg.detections[i].results[0].id == 10 or msg.detections[i].results[0].id == 11:
            self.tred = False
            self.tyellow = False
            self.tleft = False
            self.tgreen = True
         elif msg.detections[i].results[0].id == 12:
            self.tred = True
            self.tyellow = False
            self.tleft = True
            self.tgreen = False
         elif msg.detections[i].results[0].id == 13:
            self.tred = False
            self.tyellow = False
            self.tleft = True
            self.tgreen = True