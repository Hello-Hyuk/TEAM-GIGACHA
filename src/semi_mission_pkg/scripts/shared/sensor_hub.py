class SensorHub:
    def __init__(self, parent):
        self.ego = parent.ego
        self.per = parent.perception

        rospy.Subscriber(asdfasdf, callback1)
        rospy.Subscirber(asdfasdf, self.obstacleCallback)

    def speedCallback(self, msg):
        self.ego.speed = msg.data

    def obstacleCallback(self, msg):
        self.env.obs = msg.data