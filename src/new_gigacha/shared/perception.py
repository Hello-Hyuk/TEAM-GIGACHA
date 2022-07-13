import rospy
from planner_and_control.msg import Perception
from visualization_msgs.msg import MarkerArray, Marker
from vision_msgs.msg import Detection2DArray

class Perception_():
   def __init__(self):
      self.id_check = False

      rospy.Subscriber("/input", Perception, self.input_callback)
      rospy.Subscriber("/obstacles_markers", MarkerArray, self.lidar_callback)
      rospy.Subscriber("/bbox1", Detection2DArray, self.camera_callback)

      self.signx = []
      self.signy = []
      self.objx = []
      self.objy = []
      self.objw = []
      self.objh = []
      self.tmp_objx = []
      self.tmp_objy = []
      self.raw_objx = []
      self.raw_objy = []
      self.raw_objw = []
      self.raw_objh = []
      self.tred = False
      self.tyellow = False
      self.tleft = False
      self.tgreen = False
      self.signname = "go"

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
      
      if len(msg.markers) > 0:
         if msg.markers[0].id == 0:
            self.tmp_objx = []
            self.tmp_objy = []
            self.objw = []
            self.objh = []
            self.tmp_objx = self.raw_objx
            self.tmp_objy = self.raw_objy
            self.objw = self.raw_objw
            self.objh = self.raw_objh
            self.raw_objx = []
            self.raw_objy = []
            self.raw_objw = []
            self.raw_objh = []
            self.raw_objx.append(msg.markers[0].pose.position.x)
            self.raw_objy.append(msg.markers[0].pose.position.y)
            self.raw_objw.append(msg.markers[0].scale.x)
            self.raw_objh.append(msg.markers[0].scale.y)
         else:
            self.raw_objx.append(msg.markers[0].pose.position.x)
            self.raw_objy.append(msg.markers[0].pose.position.y)
            self.raw_objw.append(msg.markers[0].scale.x)
            self.raw_objh.append(msg.markers[0].scale.y)

      # for i in range(len(msg.markers)):
      #    tmp_objx.append(msg.markers[i].pose.position.x)
      #    tmp_objy.append(msg.markers[i].pose.position.y)
      #    tmp_objw.append(msg.markers[i].scale.x)
      #    tmp_objh.append(msg.markers[i].scale.y)
      
      # self.tmp_objx = tmp_objx
      # self.tmp_objy = tmp_objy
      # self.objw = tmp_objw
      # self.objh = tmp_objh
      
   def camera_callback(self, msg):
      for i in range(len(msg.detections)):
         if msg.detections[i].results[0].id < 6:
            if msg.detections[i].results[0].id == 0:
               self.signname = "turn_left_traffic_light"   #A1
            elif msg.detections[i].results[0].id == 1:
               self.signname = "turn_right_traffic_light" #A2
            elif msg.detections[i].results[0].id == 2:
               self.signname = "static_obstacle" #A3
            elif msg.detections[i].results[0].id == 3:
               self.signname = "AEB" #B1
            elif msg.detections[i].results[0].id == 4:
               self.signname = "non_traffic_right" #B2
            elif msg.detections[i].results[0].id == 5:
               self.signname = "parking"  #B3
         else:
            if msg.detection[i].results[0].id == 6 or msg.detection[i].results[0].id == 7:
               self.tred = True
               self.tyellow = False
               self.tleft = False
               self.tgreen = False
            elif msg.detection[i].results[0].id == 8 or msg.detection[i].results[0].id == 9:
               self.tred = False
               self.tyellow = True
               self.tleft = False
               self.tgreen = False
            elif msg.detection[i].results[0].id == 10 or msg.detection[i].results[0].id == 11:
               self.tred = False
               self.tyellow = False
               self.tleft = False
               self.tgreen = True
            elif msg.detection[i].results[0].id == 12:
               self.tred = True
               self.tyellow = False
               self.tleft = True
               self.tgreen = False
            elif msg.detection[i].results[0].id == 13:
               self.tred = False
               self.tyellow = False
               self.tleft = True
               self.tgreen = True