import serial
import rospy
from sensor_msgs.msg import Imu
from sig_int_handler import Activate_Signal_Interrupt_Handler


class AHRS_parser():
    def __init__(self):
        rospy.init_node('ahrs_parser', anonymous = False)
        rospy.loginfo('ahrs_parser is on......')
        
        self.ser = serial.Serial(port = '/dev/imu',  baudrate = 115200)
        self.raw_data = Imu()
        self.pub = rospy.Publisher("/imu", Imu, queue_size = 1)
        self.raw_data.header.stamp = rospy.Time.now()
        self.raw_data.header.frame_id = "imu_link"

    def parser(self):
        try :
            data = self.ser.readline()
            data = data.decode('ascii')
            sdata = data.split(',')

        except :
            UnicodeDecodeError
        
        try : 
            self.raw_data.orientation.x = float(sdata[3])
            self.raw_data.orientation.y = float(sdata[2])
            self.raw_data.orientation.z = float(sdata[1])
            self.raw_data.orientation.w = float(sdata[4])
            self.raw_data.angular_velocity.x = float(sdata[5])
            self.raw_data.angular_velocity.y = float(sdata[6])
            self.raw_data.angular_velocity.z = float(sdata[7])
            self.raw_data.linear_acceleration.x = float(sdata[8])
            self.raw_data.linear_acceleration.y = float(sdata[9])
            self.raw_data.linear_acceleration.z = float(sdata[11])

        except IndexError:
            rospy.loginfo('++++++++++++++++++++++++++++++++++')
    
        self.pub.publish(self.raw_data)



if __name__ == '__main__':

    try :
        Activate_Signal_Interrupt_Handler()
        imu = AHRS_parser()
        while not rospy.is_shutdown():
            imu.parser()
    except rospy.ROSInterruptException:
        pass
        