import rospy
from planner_and_control.msg import Perception
from visualization_msgs.msg import MarkerArray, Marker

class Perception_():
   def __init__(self):
      self.id_check = False

      rospy.Subscriber("/input", Perception, self.input_callback)


      self.objx = []
      self.objy = []
      self.objr = []

   def input_callback(self, msg):

      self.objx = msg.objx
      self.objy = msg.objy
      self.objr = msg.objr


#    def lidar_callback(self, msg):
#       self.tmp_objx = []
#       self.tmp_objy = []
#       self.objw = []
#       self.objh = []

#       if msg.markers[0].id == 0:
#          self.tmp_objx = []
#          self.tmp_objy = []
#          self.objw = []
#          self.objh = []

#       self.tmp_objy.append(msg.markers[0].pose.position.y)
#       self.tmp_objx.append(msg.markers[0].pose.position.x)
#       self.objh.append(msg.markers[0].scale.y)
#       self.objw.append(msg.markers[0].scale.x)

      # for i in range(len(msg.markers)):
      #    tmp_objx.append(msg.markers[i].pose.position.x)
      #    tmp_objy.append(msg.markers[i].pose.position.y)
      #    tmp_objw.append(msg.markers[i].scale.x)
      #    tmp_objh.append(msg.markers[i].scale.y)
      
      # self.tmp_objx = tmp_objx
      # self.tmp_objy = tmp_objy
      # self.objw = tmp_objw
      # self.objh = tmp_objh
      