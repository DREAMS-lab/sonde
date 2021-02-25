import serial
import time
ser = serial.Serial('/dev/ttyUSB0',baudrate=19200,
                    rtscts=False, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,timeout=30,bytesize=serial.EIGHTBITS)

while(1):
    ser.write(b'\r\n')
    time.sleep(1)
    print(ser.readline())
    ser.write(b'read\r\n')
    print(ser.readline())
    time.sleep(1)

