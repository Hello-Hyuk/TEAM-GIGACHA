import threading
import struct
import rospy
from time import sleep

class SerialReader(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.ser = parent.ser
        self.ego = parent.shared.ego

    def run(self):
        while True:
            packet = self.ser.read_until(b'\x0d\x0a')
            if len(packet) == 18:
                header = packet[0:3].decode()
                if header == "STX":
                    #auto_manual, e-stop, gear
                    (self.serial_msg.auto_manual,
                    self.serial_msg.emergency_stop,
                    self.serial_msg.gear) \
                    = struct.unpack("BBB", packet[3:6])
                    
                    #speed, steer
                    tmp1, tmp2 = struct.unpack("2h", packet[6:10])
                    self.serial_msg.speed = tmp1 / 10  # km/h
                    self.serial_msg.steer = 0  # degree
                    self.serial_msg.steer = tmp2 / 71  # degree

                    #brake
                    self.serial_msg.brake = struct.unpack("B", packet[10:11])[0]

                    #encoder -- not working
                    self.serial_msg.encoder = struct.unpack("BBBB", packet[11:15])

                    #alive (heartbeat)
                    self.alive = struct.unpack("B", packet[15:16])[0]

            sleep(self.period)