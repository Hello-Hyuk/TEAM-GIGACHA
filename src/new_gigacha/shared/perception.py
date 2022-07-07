import rospy
from planner_and_control.msg import Perception

class Perception_():
   def __init__(self):

      rospy.Subscriber("/input", Perception, self.input_callback)

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
      self.signname = "static_obstacle"

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