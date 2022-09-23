import rospy

from geometry_msgs.msg import PoseArray

class Perception_():
   def __init__(self):
      rospy.Subscriber("/cone_blue", PoseArray, self.blue_callback)
      rospy.Subscriber("/cone_yellow", PoseArray, self.yellow_callback)
      self.point_x = 1
      self.point_y = 0
      self.point_r = 0
      self.percep_state = 1 #노랑만 다 보이면 1 파랑만 다보이면 2로 

   def blue_callback(self, msg):

      obj_x
      pass
   
   def yellow_callback(self, msg):
      pass

   def Make_Path(self):
      pass
