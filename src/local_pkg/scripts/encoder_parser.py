import serial
import rospy
import signal
import sys
from std_msgs.msg import Int64

def signal_handler(sig, frame):
    print("Shut Down")
    sys.exit(0)

class Encoder_Parsing():
    def __init__(self):
        rospy.init_node('Displacement_right', anonymous = False)
        self.pub = rospy.Publisher('/Displacement_right', Int64, queue_size = 1)
        self.ser = serial.Serial(port = '/dev/encoder', baudrate = 115200)
        signal.signal(signal.SIGINT, signal_handler)

    def main(self):
        res = self.ser.readline()
        while True:
            try:
                rospy.loginfo(int(res))
                break
            except:
                res = self.ser.readline()

        self.pub.publish(int(res))

if __name__ == "__main__":
    enc = Encoder_Parsing()

    while not rospy.is_shutdown():
        enc.main()