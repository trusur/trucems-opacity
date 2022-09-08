import time
from datetime import datetime
import requests
import json

while True:
    try:
        now = datetime.now()
        patch_url_runtime = "http://localhost/trucems-opacity/public/api/runtime"
        get_payload = {}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response_runtime = requests.request(
            "GET", patch_url_runtime, headers=headers, data=get_payload)
        json_get_runtime = json.loads(response_runtime.text)
        time.sleep(60)
        if(json_get_runtime["success"] == True):
            if(int(json_get_runtime["data"]["hours"]) >= 23 and int(json_get_runtime["data"]["minutes"]) >= 59):
                days = float(json_get_runtime["data"]["days"]) + 1
                hours = 0
                minutes = 0
            elif(int(json_get_runtime["data"]["minutes"]) >= 59):
                days = json_get_runtime["data"]["days"]
                hours = float(json_get_runtime["data"]["hours"]) + 1
                minutes = 0
            else:
                days = json_get_runtime["data"]["days"]
                hours = json_get_runtime["data"]["hours"]
                minutes = float(json_get_runtime["data"]["minutes"]) + 1
            patch_payload_runtime = 'days=' + \
                str(days)+'&hours='+str(hours)+'&minutes='+str(minutes)
            response = requests.request(
                "PATCH", patch_url_runtime, headers=headers, data=patch_payload_runtime)
    except Exception as e:
        now2 = datetime.now()
        timestamp = now2.strftime("%Y-%m-%d %H:%M:%S")
