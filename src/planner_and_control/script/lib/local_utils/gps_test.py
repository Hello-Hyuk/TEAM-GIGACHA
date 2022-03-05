import serial


ser = serial.Serial('/dev/gps', baudrate = 115200)

def make_decode(coord):
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return float(deg + "." + min + tail)

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
    