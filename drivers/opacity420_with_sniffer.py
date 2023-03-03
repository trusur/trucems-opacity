from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
from textwrap import wrap
import math
import json
import requests
# import json
# import requests
# import logging
# import datetime
# import sys

import serial
from mysql.connector.constants import ClientFlag
import mysql.connector

baseUrl = "http://localhost/trucems-opacity/public/{}"
portADC = '/dev/ttyADC'
portDAC = '/dev/ttyDAC'


def connecting():
    try:
        return mysql.connector.connect(host="localhost", user="root", passwd="root", database="trucems_opacity")
    except Exception as e:
        return


db = connecting()
cursor = db.cursor(dictionary=True)


def get_pcld():
    try:
        url = baseUrl.format("/api/getPCLD")
        response = requests.request("GET", url, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        return json.loads(response.text)
    except Exception as e:
        return False


def updateValue(sensorId, value):
    try:
        cursor.execute("UPDATE sensor_values SET value = '" +
                       str(round(value, 0)) + "' WHERE id = '" + str(sensorId) + "'")
        db.commit()
    except Exception as e:
        # date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        # logging.error(e)
        return False


def getSensorValue(sensorId):
    try:
        sensorId = str(sensorId)
        cursor.execute(
            "SELECT * FROM sensor_values WHERE sensor_id = '"+sensorId+"'")
        values = cursor.fetchone()
        cursor.execute("SELECT * FROM sensors WHERE id = '"+sensorId+"'")
        values['sensor'] = cursor.fetchone()
        return values
    except Exception as e:
        # date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        # logging.error(e)
        return False


def setAnalogOutput(outputIndex, value):
    outputIndex = int(outputIndex)
    if(value > 4000 and value < 20000):
        value = value
    elif value < 4000:
        value = 4000
    elif value > 20000:
        value = 20000
    if(type(value) != "int"):
        value = int(value)
    try:
        client = ModbusClient(method='rtu', port=portDAC,
                              baudrate=9600, parity='N', timeout=3)
        connection = client.connect()
        if(connection):
            write = client.write_register(outputIndex, value, unit=1)
            print(write)
            client.close()
            return True

        return False
    except Exception as e:
        # date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        # logging.error(e)
        return False


sensors = [1]
while True:
    try:
        for sensorId in sensors:
            with serial.Serial('portADC', 9600, timeout=10) as ser:
                responses = wrap(ser.read_until(b'\r').hex(), 2)
                if(len(responses) == 18):
                    try:
                        LD1 = int(str(responses[6]) + str(responses[7]), 16)
                        PD = int(str(responses[14]) + str(responses[15]), 16)
                        PCLD = get_pcld()["PCLD"]
                        LD2 = LD1 * PCLD
                        T = math.sqrt(PD/LD2)
                        value = (1-T) * 100

                        sensor = getSensorValue(sensorId)
                        writeAddress = sensor['sensor']['write_address']
                        concentrate = -1 if value == - \
                            1 else eval(sensor['sensor']['read_formula'])
                        concentrate = 100 if concentrate > 100 else concentrate
                        updateValue(sensor['sensor']['id'], concentrate)
                        setAnalogOutput(writeAddress, value)
                    except Exception as e:
                        print(e)
            time.sleep(1)
    except Exception as e:
        updateValue(1, -1)
        # print(e)
        # date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        # logging.error(e)
