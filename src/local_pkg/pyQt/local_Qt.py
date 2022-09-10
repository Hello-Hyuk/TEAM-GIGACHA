import sys
import rospy
from local_pkg.msg import Local
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from geometry_msgs.msg import Pose
from sensor_msgs.msg import NavSatFix 
from ublox_msgs.msg import NavPVT 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("uis/local_ui.ui")[0]

class WindowClass(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        rospy.init_node("Gigacha_ui", anonymous = False)
        rospy.Subscriber("/local_msgs", Local, self.localCallback)
        rospy.Subscriber("ublox_gps/fix", NavSatFix, self.gpsCallback) 
        rospy.Subscriber("ublox_gps/navpvt", NavPVT, self.navpvtCallback) 
        rospy.Subscriber("/serial", Serial_Info, self.serialCallback)
        rospy.Subscriber("/simul_gps", Pose, self.simulGpsCallback)
        rospy.Subscriber("/controller", Control_Info, self.controlCallback)

        self.dial_heading.setMaximum(180)
        self.dial_heading.setMinimum(-180)

        self.dial_steer.setMaximum(30)
        self.dial_steer.setMinimum(-30)

        self.slider_speed.setMaximum(20)
        self.slider_speed.setMinimum(0)

    def localCallback(self, msg):
        self.lbl_x.setText(str(msg.x))
        self.lbl_y.setText(str(msg.y))
        self.lbl_drx.setText(str(msg.dr_x))
        self.lbl_dry.setText(str(msg.dr_y))

        if 0 <= msg.heading < 180:
            heading = msg.headin
        else:
            heading = msg.heading - 360

        self.dial_heading.setValue(int(heading))
        self.lbl_heading.setText(str(msg.heading))

    def controlCallback(self, msg):
        self.dial_steer.setValue(int(msg.steer))
        self.lbl_steer.setText("{0}".format(self.dial_steer.value()))

        if msg.gear == 0:
            self.lbl_gear.setText("Forward")
        elif msg.gear == 2:
            self.lbl_gear.setText("Backward")

    def serialCallback(self, data):
        self.slider_speed.setValue(round(data.speed))
        self.lbl_speed.setText("{0} km/h".format(self.slider_speed.value()))

        self.slider_brake.setValue(data.brake)
        self.lbl_brake.setText("{0}".format(self.slider_brake.value()))

        if data.auto_manual == 1:
            self.lbl_ma.setText("AUTO")
        else:
            self.lbl_ma.setText("MANUAL")

    def gpsCallback(self, data):
        self.lbl_lat.setText(str(data.latitude))
        self.lbl_lon.setText(str(data.longitude))

        if data.fixType == 0:
            self.lbl_gnss.setText("UNAVAILABLE")
        elif data.fixType == 1:
            self.lbl_gnss.setText("INACCURACY")
        elif data.fixType == 2:
            self.lbl_gnss.setText("GNSS - 3sat")
        elif data.fixType == 3:
            self.lbl_gnss.setText("GNSS - 12sat")
        elif data.fixType == 4:
            self.lbl_gnss.setText("DIFF")
        else:
            self.lbl_gnss.setText("FIX")

    def navpvtCallback(self, data):
        self.lbl_acc.setText("{0}".format(data.hAcc))

        if data.hAcc < 50:
            self.lbl_rtk.setText("ON")
        else:
            self.lbl_rtk.setText("OFF")

    def simulGpsCallback(self, data):
        self.lbl_lat.setText(str(data.position.x))
        self.lbl_lon.setText(str(data.position.y))

    def initUI(self):
        self.setWindowTitle('Local Informations')
        self.setWindowIcon(QIcon("location.png"))
        self.setGeometry(300, 300, 600, 560)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())