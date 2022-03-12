import serial


ser = serial.Serial('/dev/gps', baudrate = 115200)

def make_decode(coord):

    deg = float(coord[0:2])
    min = float(coord[2:]) / 60

    return deg + min

while True:
    ser_read = ser.readline()
    try:
        decode = ser_read.decode('ascii')
    except:
        UnicodeDecodeError
    
    if decode[0:6] == '$GNGGA':
        sdata = decode.split(',')
        
        lat = make_decode(sdata[2])
        print(lat)