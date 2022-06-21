from planner_and_control.msg import Perception

class Perception():
   def __init__(self, parent):

      rospy.Subscriber("/input", Perception, self.input_callback)

      self.signx = []
      self.signy = []
      self.objx = []
      self.objy = []
      self.objr = []
      self.tred = 0
      self.tyellow = 0
      self.tleft = 0
      self.tgreen = 0
      self.signname = ""

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