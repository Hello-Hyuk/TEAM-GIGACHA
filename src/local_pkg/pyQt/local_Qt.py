import sys
import rospy
from local_pkg.msg import Local
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from sensor_msgs.msg import NavSatFix 
from ublox_msgs.msg import NavPVT 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("uis/local_ui.ui")[0]

class WindowClass(QDialog, form_class):
    def __init__(self):
        super().__init__()
        rospy.Subscriber("/local_msgs", Local, self.localCallback)
        rospy.Subscriber("ublox_gps/fix", NavSatFix, self.gpsCallback) 
        rospy.Subscriber("ublox_gps/navpvt", NavPVT, self.navpvtCallback) 
        rospy.Subscriber("/serial", Serial_Info, self.serialCallback)
        rospy.Subscriber("/simul_gps", Pose, self.simulGpsCallback)
        rospy.Subscriber("/controller", Control_Info, self.controlCallback)

        self.setupUi(self)
        self.initUI()
        self.data = Local()

        self.checker_list = [False, False, False]

        self.dial.setMaximum(359)
        self.dial.setMinimum(0)
        self.dial.setSingleStep(1)

        self.dial_steer.setMaximum(30.0)
        self.dial_steer.setMinimum(-30.0)
        self.dial_steer.setSinglestep(1.0)

        self.slider_speed.setMaximum(20.0)
        self.slider_speed.setMinimum(0.0)
        self.slider_speed.setSingleStep(1.0)

        self.dial.valueChanged.connect(self.LCDHeading)

    def controlCallback(self, msg):
        self.dial_steer.setValue(self.msg.steer)
        self.lbl_steer.setText("{0}",format(self.dial_steer.value()))

        if msg.gear == 0:
            self.lbl_gear.setText("Forward")
        elif msg.gear == 2:
            self.lbl_gear.setText("Backward")

    def serialCallback(self, data):
        self.slider_speed.setValue(data.speed)
        self.lbl_speed.setText("{0} km/h".format(self.slider_speed.value()))

        self.slider_brake.setValue(data.brake)
        self.lbl_brake.setText("{0}".format(self.slider_brake.value()))

        if data.auto_manual == 1:
            self.lbl_ma.setText("AUTO")
        else:
            self.lbl_ma.setText("MANUAL")

    def localCallback(self, msg):
        self.data = msg

        if not self.checker_list[0]:
            self.tb_position.setPlainText('x : {0}\n\
            y : {1}\n\
            dr_x : {2}\n\
            dr_y : {3}\n\
            ==============='.format(self.data.x, self.data.y,\
            self.data.dr_x, self.data.dr_y))
            self.checker_list[0] = True

        self.tb_position.append('x : {0}\n\
            y : {1}\n\
            dr_x : {2}\n\
            dr_y : {3}\n\
            ==============='.format(self.data.x, self.data.y,\
            self.data.dr_x, self.data.dr_y))

        self.dial.setValue(self.data.heading)

    def gpsCallback(self, data):

        if not self.checker_list[1]:
            self.tb_geo.setPlainText('latitude : {0}\nlongitude : {1}\n\
            ==============='.format(self.data.latitude, self.data.longitude))
            self.checker_list[1] = True

        self.tb_geo.append('latitude : {0}\nlongitude : {1}\n\
            ==============='.format(self.data.latitude, self.data.longitude))

    def navpvtCallback(self, data):
        self.lbl_acc.setText("{0}".format(data.hAcc))

        if data.hAcc < 50:
            self.lbl_rtk.setText("ON")
        else:
            self.lbl_rtk.setText("OFF")

    def simulGpsCallback(self, data):
        
        if not self.checker_list[1]:
            self.tb_geo.setPlainText('latitude : {0}\nlongitude : {1}\n\
            ==============='.format(self.data.position.x, self.data.position.y))
            self.checker_list[1] = True

        self.tb_geo.append('latitude : {0}\nlongitude : {1}\n\
            ==============='.format(self.data.position.x, self.data.position.y))


    def LCDHeading(self):
        self.heading.display

    def initUI(self):
        self.setWindowTitle('Local Informations')
        self.setWindowIcon(QIcon("location.png"))
        self.setGeometry(300, 300, 600, 560)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()