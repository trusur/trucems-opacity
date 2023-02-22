from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import json
import requests
import logging
import datetime
import sys

baseUrl = "http://localhost/trucems-opacity/public/{}"
portADC = '/dev/ttyADC'
# portADC = 'COM5'
portDAC = '/dev/ttyDAC'

def linear_map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def get_opacity(value):
    try:
        url = baseUrl.format("/api/getOpacityBy420Concentration/" + str(value))
        response = requests.request("GET", url, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        return json.loads(response.text)
    except Exception as e:
        return False

def updateValue(sensorId, value):
    try:
        url = baseUrl.format("/api/sensor-value/"+str(sensorId))
        payload = 'value='+str(value)
        response = requests.request("PATCH", url, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }, data=payload)
        return json.loads(response.text)
    except Exception as e:
        date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        # logging.error(e)
        return False


def getSensorValue(sensorId):
    try:
        response = requests.request("GET", baseUrl.format(
            "/api/sensor-value/"+str(sensorId)))
        return json.loads(response.text)
    except Exception as e:
        date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/" + \
        #     str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w',
        #                     format='%(asctime)s - %(message)s')
        # logging.error(e)
        return False


def getAnalogInput():
    try:
        clientInput = ModbusClient(
            method='rtu', port=portADC, baudrate=9600, parity='N', timeout=3)
        if(clientInput.connect()):
            read = clientInput.read_holding_registers(0, 1, unit=1)
            clientInput.close()
            return read.registers[0]
        return -1
    except Exception as e:
        date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/" + \
        #     str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w',
        #                     format='%(asctime)s - %(message)s')
        # logging.error(e)
        return -1


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
            # print(write)
            client.close()
            return True

        return False
    except Exception as e:
        date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/" + \
        #     str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w',
        #                     format='%(asctime)s - %(message)s')
        # logging.error(e)
        return False


sensors = [1]
while True:
    try:
        for sensorId in sensors:
            sensor = getSensorValue(sensorId)
            value = getAnalogInput()
            writeAddress = sensor['sensor']['write_address']

            concentrate = get_opacity(value)["opacity"];
            updateValue(sensor['sensor']['id'], round(concentrate,2))
            concentrate420 = int(round(linear_map(concentrate,0,100,4000,20000),0))
            # print(concentrate)
            # print(concentrate420)
            time.sleep(1)
            setAnalogOutput(writeAddress, concentrate420)
            time.sleep(1)
        time.sleep(1)
    except Exception as e:
        date = datetime.datetime.now()
        # errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/" + \
        #     str(date.strftime("%d_%m_%y"))+'_errors.log'
        # logging.basicConfig(filename=errorFile, filemode='w',
        #                     format='%(asctime)s - %(message)s')
        # logging.error(e)
