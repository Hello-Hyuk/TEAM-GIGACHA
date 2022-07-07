import rospy
from planner_and_control.msg import Perception
from visualization_msgs.msg import MarkerArray, Marker

class Perception_():
   def __init__(self):

      rospy.Subscriber("/input", Perception, self.input_callback)
      rospy.Subscriber("/lidar_topic", MarkerArray, self.lidar_callback)

      self.signx = []
      self.signy = []
      self.objx = [100, 113]
      self.objy = [190, 216]
      self.objr = []
      self.objw = [1, 1]
      self.objh = []
      self.tred = False
      self.tyellow = False
      self.tleft = False
      self.tgreen = False
      self.signname = "AEB"

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
      tmp_objx = []
      tmp_objy = []
      tmp_objw = []
      tmp_objh = []

      for i in range(len(msg.markers)):
         tmp_objx.append(msg.markers[i].pose.position.x)
         tmp_objy.append(msg.markers[i].pose.position.y)
         tmp_objw.append(msg.markers[i].scale.x)
         tmp_objh.append(msg.markers[i].scale.y)
      
      self.objx = tmp_objx
      self.objy = tmp_objy
      self.objw = tmp_objw
      self.objh = tmp_objh
      