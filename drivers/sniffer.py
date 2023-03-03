from __future__ import print_function
import serial
import time
from textwrap import wrap

while True:
    with serial.Serial('/dev/ttyADC', 9600, timeout=10) as ser:
        responses = wrap(ser.read_until(b'\r').hex(),2)
        if(len(responses) == 18):
            try:
                Io = int(str(responses[6]) + str(responses[7]),16)
                I = int(str(responses[14]) + str(responses[15]),16)
                T = I/Io
                O = (1-T) * 100
                print("Io = " + str(Io))
                print("I = " + str(I))
                print("T = " + str(T))
                print("O = " + str(O))
                
            except Exception as e:
                print(e)
        
