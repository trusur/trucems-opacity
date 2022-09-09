from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import json
import requests
import logging
import datetime


baseUrl = "http://localhost/trucems-opacity/public/{}"
portADC = 'COM3'
portDAC = 'COM4'

def updateValue(sensorId, value):    
    try:
        url = baseUrl.format("/api/sensor-value/"+str(sensorId))
        payload='value='+str(value)
        response = requests.request("PATCH", url, headers={
          'Content-Type': 'application/x-www-form-urlencoded'
        }, data=payload)
        return json.loads(response.text)
    except Exception as e:
        date = datetime.datetime.now()
        errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        logging.error(e)
        return False
    
def getSensorValue(sensorId):
    try:
        response = requests.request("GET", baseUrl.format("/api/sensor-value/"+str(sensorId)))
        return json.loads(response.text)
    except Exception as e:
        date = datetime.datetime.now()
        errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        logging.error(e)
        return False
    
def getAnalogInput():
    try:
        clientInput = ModbusClient(method = 'rtu',port=portADC,baudrate=9600,parity = 'N',timeout=3)
        if(clientInput.connect()):
            read = clientInput.read_holding_registers(0, 8, unit=1)
            clientInput.close()
            return read.registers[0]
        return -1
    except Exception as e:
        date = datetime.datetime.now()
        errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        logging.error(e)
        return -1

def setAnalogOutput(outputIndex, value):
    if(value > 4000 and value < 20000):
        value = value
    elif value < 4000:
        value = 4000
    elif value > 20000:
        value = 20000
    value = int(value)
    print(value)
    try:
        client = ModbusClient(method = 'rtu',port=portDAC,baudrate=9600,parity = 'N',timeout=3)
        connection = client.connect()
        if(connection):
            write = client.write_register(outputIndex, value, unit=1)
            client.close()
            return True
        
        return False
    except Exception as e:
        date = datetime.datetime.now()
        errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        logging.error(e)    
        return False
sensors = [1]
while True:    
    try:
        for sensorId in sensors:
            sensor = getSensorValue(sensorId)
            value = getAnalogInput()
            concentrate = -1 if value == -1 else eval(sensor['sensor']['read_formula'])
            time.sleep(1)
            updateValue(sensorId,concentrate)
            # setAnalogOutput(0,value)
            time.sleep(1)
        time.sleep(1)
    except Exception as e:
        date = datetime.datetime.now()
        errorFile = "/var/www/html/trucems-opacity/drivers/error_logs/"+str(date.strftime("%d_%m_%y"))+'_errors.log'
        logging.basicConfig(filename=errorFile, filemode='w', format='%(asctime)s - %(message)s')
        logging.error(e)