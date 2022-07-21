import threading
import struct
from time import sleep

class SerialWriter(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.ser = parent.ser
        self.ego = parent.shared.ego

        # print("SerialWriter")

    def run(self):
        while True:
            #Min/Max Limit
            if self.ego.input_speed > 20:
                self.ego.input_speed = 20

            self.ego.input_speed = max(0, min(self.ego.input_speed, 20))

            if self.ego.input_brake > 200:
                self.ego.input_brake = 200

            result = struct.pack(
                ">BBBBBBHhBBBB",
                0x53,
                0x54,
                0x58,
                0x01, #always auto
                self.ego.input_estop,
                self.ego.input_gear,
                int(self.ego.input_speed * 10),
                int(self.ego.input_steer * 71),
                self.ego.input_brake,
                self.ego.alive,
                0x0D,
                0x0A
            )
            self.ser.write(result)

            # print(self.ego.input_gear)
            # print(self.ego.input_steer)

            sleep(self.period)