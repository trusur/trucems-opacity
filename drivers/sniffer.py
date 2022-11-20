from __future__ import print_function
import serial
import time
import db_connect

try:
    mydb = db_connect.connecting()
    mycursor = mydb.cursor()
    
except Exception as e: 
    print("[X] " + e)


while True:
    with serial.Serial('COM3', 9600, timeout=10) as ser:
        response = ser.read_until(b'\r')
        print(response)
        response = str(response).replace("!","").replace(" ","").replace("\\r","").replace("'","")
        responses = response.split('\\x')
        if(responses[0] == 'b'):
            try:
                # print(str(responses[7]) + str(responses[8]))
                # print(str(responses[15]) + str(responses[16]))
                Io = int(str(responses[7]) + str(responses[8]),16)
                I = int(str(responses[15]) + str(responses[16]),16)
                T = I/Io
                O = (1-T) * 100
                print("Io = " + str(Io))
                print("I = " + str(I))
                print("T = " + str(T))
                print("O = " + str(O))
                
                try:
                    mycursor.execute("SELECT id FROM sensor_values WHERE sensor_id = '1'")
                    sensor_value_id = mycursor.fetchone()[0]
                    mycursor.execute("UPDATE sensor_values SET value = '" + str(round(O,0)) + "' WHERE id = '" + str(sensor_value_id) + "'")
                    mydb.commit()
                except Exception as e:
                    mycursor.execute("INSERT INTO sensor_values (sensor_id,value) VALUES ('1','0','" + str(round(O,0)) + "')")
                    mydb.commit()
                
            except Exception as e:
                print(e)
        
