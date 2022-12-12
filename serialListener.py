import serial
import time
#import numpy as np
import math
#import random
from sklearn.linear_model import LinearRegression

X = []
y = []
for i in range(0, 181):
    X.append([math.sin(math.radians(i * 0.5)), i * 0.5])
    y.append([math.sin(math.radians((i + 1) * 0.5)) * 3 + 3, (i + 1) * 0.5])
reg = LinearRegression().fit(X, y)

serialPort = serial.Serial(port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print("Connection established")
serialString = ""  # Used to hold data coming over UART
crit = 2.0
data1 = []
data2 = []
comm = "1"
while 1:
    resp = 0
    # Wait until there is data waiting in the serial buffer
    if serialPort.in_waiting > 0:

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()
        resp = 1

        # Print the contents of the serial data
        try:
            i = serialString.decode("Ascii")
            print(i)
            if (len(data1) < 1) or (len(data1) == 1):
                j = i.split(";")
                v1 = (float(j[0])/100 - 3)/3
                v2 = (float(j[1])/100 - 3)/3
                t = float(j[2].rstrip())/100
                data1.append([v1, t])
                data2.append([v2, t])
            elif len(data1) == 2:
                data1[0] = data1[1]
                data2[0] = data2[1]
                j = i.split(";")
                v1 = (float(j[0]) / 100 - 3) / 3
                v2 = (float(j[1]) / 100 - 3) / 3
                t = float(j[2].rstrip()) / 100
                data1[1] = [v1, t]
                data2[1] = [v2, t]
            print(data1)
            print(data2)
            if len(data1) == 2:
                pred1 = reg.predict(data1)
                pred2 = reg.predict(data2)
                print(pred1)
                if (pred1[1][0] > crit) & (pred2[1][0] > crit):
                    comm = 0
                else:
                    comm = 1
            print(comm)
        except:
            time.sleep(10)
            pass
    else:
        if resp == 1:
            try:
                serialPort.writelines(comm)
            except:
                time.sleep(10)
                pass
    serialPort.flush()