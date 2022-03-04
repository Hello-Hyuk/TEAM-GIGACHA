#!/usr/bin/env python3
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler

import io
import pynmea2
import serial

ser = serial.Serial('/dev/gps', 115200)
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

while True:

    line = sio.readline()
    print(line)
    msg = pynmea2.parse(line)
    print(repr(msg))
    break


Activate_Signal_Interrupt_Handler()