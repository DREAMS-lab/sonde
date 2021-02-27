import serial
import time
ser = serial.Serial('/dev/ttyUSB0',baudrate=19200,
                    rtscts=False, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,timeout=30,bytesize=serial.EIGHTBITS)
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
file = open(timestr+'-dreams-manta.csv','w')
while(1):
    ser.write(b'\r\n')
    time.sleep(3)
    print(ser.readline())
    ser.write(b'read\r\n')
    data = ser.readline().decode().replace('> > #DATA: ','').rstrip()
    print(data)
    file.write(data+'\n')
    file.flush()

