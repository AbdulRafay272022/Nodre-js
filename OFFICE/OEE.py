# Importing Libraries
import RPi.GPIO as GPIO
import serial
from datetime import datetime
from queue import Queue
import time
import requests
import os

# Serial Communication Initiallization
ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=5)

# Initiallize Log Files
logFilePath = '/home/pi/Pakistan_Automation/Saad/logFiles'
plcLog = ''
uploadLog = ''
errorLog = ''

# Pin Initialization
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                  # Set the GPIO mode to BCM
Counter_Rst = 2
Status_Pin = 3
Status_LED = 22
GPIO.setup(Counter_Rst, GPIO.OUT)       # Set the GPIO pin as an output
GPIO.setup(Status_Pin, GPIO.OUT)        # Set the GPIO pin as an output
GPIO.setup(Status_LED, GPIO.OUT)        # Set the GPIO pin as an output

GPIO.output(Counter_Rst, GPIO.LOW)
time.sleep(0.5)
GPIO.output(Counter_Rst, GPIO.HIGH)
GPIO.output(Status_Pin, GPIO.HIGH)
GPIO.output(Status_LED, GPIO.LOW)

# Initiallize Variables
deviceName = "MiraFlex 1"
serTime = 0             # Store Time at which Serial Data Received
serTimeDiff = 0         # Store Time Difference Between 2 Serial Events
serAvailable = False    # True when New Ser Data Received
machineCount = 0        # Store Machine Count 
countDiff = 0           # Store Count Difference for calculating RPM 
machineRPM = 0          # Store RPM of Machine RPM = countDiff/ SerTimeDiff
uploadInterval = 5     # Upload Data in Every 20 Secs
sensingInterval = 5    # Time To Make Upload Data
sensingTime = 0         # Time To Make Upload Data
uploadTime = 0          # Store Uploading Time
# Api Variables
machineStatus = 0       # Store Status of Machine
machineSpeed = 0        # Store machine Speed machineSpeed= machineRPM*0.381
productionTotal=0       # Store Total Manufactured Product in Meter productionTotal = machineCount*0.381
productionKg = 0
add_count = 0
activePO = ''
activeShift = ''
SKU = ''
SKUTarget = ''
orderId = ''
serverStatus = False
pKg = 0


# Initialize Que
my_queue = Queue()      # Store Data to Upload



# API URL
LivePath = "https://oeeb-k.pakistanautomation.com.pk"
LocalPath = "http://10.1.1.92:5000"
baseURL = LivePath + "/api" 

#data_api ='http://192.168.18.6:5000/api/deviceData/insertData'
data_api = baseURL + '/deviceData/insertDataNew'
#order_api = baseURL + '/order/getOrders'
order_api = baseURL + '/deviceData/getOrderInfo'

HoldOrder_api = {
    'Save': baseURL + '/holdOrder/saveRecord',
    'View': baseURL + '/holdOrder/selectRecord',
    'Delete': baseURL + '/holdOrder/deleteRecord'
}



check_api = LivePath + '/checkServer'

# Initiallize Dictionary for Holding Data
Upload = {
    'deviceId':"DevID",
    'timestamp':"time",
    'd1': 0, 
    'v2': 0, 
    'v3': 0, 
    'machineSpeed': 0, 
    'runningPO': '',
    'SKU':'',
    'SKUTarget': '',
    'orderId': ''
}


# Function to get time
def millis():
    return time.time()

def ResetCounter():
    global productionTotal,activePO,add_count
    GPIO.output(Counter_Rst, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(Counter_Rst, GPIO.HIGH)
    productionTotal = 0
    activePO = ''
    add_count = 0


# Function to prepare Upload Dictionary for Data Upload
def make_upload(dev_id, time, status, speed, P_total, P_total_kg, PO, sku, skuTarget, orderID, shift):
    # Upload ={'deviceId':dev_id,'timestamp':time,'d1':status,'machineSpeed':speed, 'v2':P_total}
    Upload = {
        'deviceId':dev_id,
        'timestamp':time,
        'd1': status, 
        'v2': P_total, 
        'v3': P_total_kg, 
        'machineSpeed': speed, 
        'runningPO': PO,
        'SKU':sku,
        'SKUTarget': skuTarget,
        'orderId': orderID,
        'currentShift': shift
    }
    return Upload

# Try-Catch to prevent crashing
try:
    # Never Ending Loop
    while True:
        plcLog = logFilePath + '/plcLog-' + datetime.now().strftime("%m-%d-%Y")+'.txt'
        uploadLog = logFilePath + '/uploadLog-' + datetime.now().strftime("%m-%d-%Y")+'.txt'
        errorLog = logFilePath + '/errorLog-' + datetime.now().strftime("%m-%d-%Y")+'.txt'

        if not(os.path.isfile(plcLog)):
            log = open(plcLog,'x')
            log.write('New File Created')
            log.write('\n')
            log.close()
        if not(os.path.isfile(uploadLog)):
            log = open(uploadLog,'x')
            log.write('New File Created')
            log.write('\n')
            log.close()
        if not(os.path.isfile(errorLog)):
            log = open(errorLog,'x')
            log.write('New File Created')
            log.write('\n')
            log.close()

        # If Serial Data is Available 
        if ser.in_waiting > 9:
            # Calculate Time Difference Between Previous & this Serial Event
            serTimeDiff = round((millis() - serTime), 6)                 
            
            # Store Time of This Serial Event
            serTime = round(millis(), 6)                               
            
            # Read Serial Data
            data = ser.readline()
            #print(f'  Ser Data: {data} Length: {len(data)}')

            if (serTimeDiff < 25):
                if (len(data) == 10):
                    # New Serial Data Received
                    serAvailable = True

                    # Get Machine Status From Serial Data
                    machineStatus = int.from_bytes(data[2:3], "big")
                
                    # Calculate Count Difference to Calculate RPM of Roller
                    countDiff = (
                        (data[5] * 16777216) + (data[6] * 65536) + (data[3] * 256) + data[4]
                    ) - machineCount
                    
                    # Store Current Count from Serial Data
                    machineCount = (
                        (data[5] * 16777216) + (data[6] * 65536) + (data[3] * 256) + data[4]
                    )

                    # Calculate Machine RPM to Calculate Machine Speed
                    machineRPM = round((countDiff * (60.0 / serTimeDiff)), 2)
                    
                    # Circumference of Roller is 15 inch which is 0.381 Meter
                    machineSpeed = round((machineRPM * 0.380), 2)
                    #if machinespeed is negative then make it zero
                    if machineSpeed<0:
                        machineSpeed=0
                    # Calculate Production Total 
                    productionTotal=(machineCount*0.380) + add_count   #0.381 is 15 inch to meter 
                    
                    # Create Log of Serial Data
                    TimeStamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    log = open(plcLog, 'a')
                    log.write(f"{TimeStamp}, {len(data)}, {machineStatus}, {machineCount}, {countDiff}, {machineRPM}, {machineSpeed}, {productionTotal}")
                    log.write('\n')
                    log.close()
                    ser.flush()
                else:
                    ser.flush()
            else:
                if (len(data) >= 10):
                    # Store Current Count from Serial Data
                    machineCount = (
                        (data[5] * 16777216) + (data[6] * 65536) + (data[3] * 256) + data[4]
                    )
                ser.flush()


            # print(f"RPM: {machineRPM} CountDiff: {countDiff} TimeDiff: {serTimeDiff}")
        
        if (my_queue.qsize()>0) :
            uploadInterval = 5
        else:
            uploadInterval = 5
        
        
        # Wait for Upload Time & availablity of Serial Data
        # if((millis()-uploadTime) > uploadInterval) and serAvailable:
        if((millis()-sensingTime) > sensingInterval) and serAvailable:
            sensingTime = round(millis(),2) + (sensingInterval - 5)
            TimeStamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

            try:
                print("Call get Order Query")
                data = requests.post(
                    order_api, 
                    json={
                        "deviceId": deviceName,
                        "currentPO": activePO,
                        "timestamp": TimeStamp
                    },
                    timeout=4
                )
                data.raise_for_status()
                serverStatus = False
                if data.status_code == 200:
                    sensingTime = round(millis(),2)
                    serverStatus = True
                    data = data.json()
                    data = data['data']
                    print(f"Api Response: {data}")
                    
                    if data["resetCounter"] == 1:
                        ResetCounter()
                        add_count = data["lastProductCount"]
                    elif data["resetCounter"] == 0 and activeShift != data["activeShift"]:
                        ResetCounter()
                     
                    
                    # Handle Hold Orders
                    if activePO != '':
                        try:
                            print("Call Hold Order API")
                            if data["currentPOStatus"] != 2:
                                # if current PO Status if not equal to complete then save current production in hold Order table
                                try:
                                    Api_response = requests.post(HoldOrder_api['Save'], json={'deviceName':deviceName, 'poNumber':activePO ,'lastCount':productionTotal})
                                except requests.RequestException as re:
                                    print("Request error:", re)
                                except Exception as e:
                                    print("An error occurred:", e)
                            else:
                                # else delete entry for this order
                                try:
                                    Api_response = requests.post(HoldOrder_api['Delete'], json={'deviceName':deviceName, 'poNumber':activePO})
                                except requests.RequestException as re:
                                    print("Request error:", re)
                                except Exception as e:
                                    print("An error occurred:", e)
                            
                            print("Save Hold Order Data >>> ", Api_response.json())
                        except Exception as e:
                            print('error in saving/Deleting Hold Order >>> ', e)
                    
                    
                    activePO = data['activePo']
                    SKU = data['skuName']
                    SKUTarget = data['skuTarget']
                    orderId = data['orderid']
                    pKg = float(data['qtyInKg']) / float(data['qtyInMeter'])
                    activeShift = data["activeShift"]
                    productionTotal =  productionTotal + add_count
                    
            except Exception as e:
                print(f"  Error in get order >>> {e}")
            
            if activeShift != '':
                serAvailable = False
                productionKg = productionTotal*pKg
                ready_up=make_upload(deviceName,TimeStamp,machineStatus,machineSpeed,productionTotal,productionKg,activePO, SKU, SKUTarget,orderId, activeShift)
                #print("Upload Data >>> ", ready_up)
                my_queue.put(ready_up)        

        try:
            if (my_queue.qsize()!=0 and ((millis()-uploadTime) > uploadInterval)):
                print(f"my_queue.qsize() > {my_queue.qsize()}, uploadInterval > {uploadInterval}, uploadTime > {(millis()-uploadTime)}")
                
                if serverStatus == False:
                    print("Check Server API")
                    data1 = requests.get(check_api, timeout=4)
                    data1.raise_for_status()
                    if data1.status_code == 200:
                        serverStatus = True
                    else:
                        serverStatus = False
                
                if serverStatus == True:
                    print("Insert Data API")
                    uploadTime=round(millis(),2)
                    serverStatus = False
                    GPIO.output(Status_LED, GPIO.HIGH)
                    GPIO.output(Status_Pin, GPIO.LOW)
                    value=my_queue.get()
                    print(value)
                    try:
                        response = requests.post(data_api, json=value, timeout=4)
                        response.raise_for_status()
                        if response.status_code == 200:
                            print(f"  Data updated successfully {value}")
                            log=open(uploadLog,'a')
                            log.write(str(value))
                            log.write('\n')
                            log.close()
                    except requests.RequestException as re:
                        print("Request error:", re)
                    except Exception as e:
                        print("An error occurred:", e)        
                    
                    GPIO.output(Status_LED, GPIO.LOW)
                    GPIO.output(Status_Pin, GPIO.HIGH)
                #else:
                #    print("API request failed with status code:", response.status_code)
                #    my_queue.put(value)
                print(f"my_queue.qsize() > {my_queue.qsize()}, uploadInterval > {uploadInterval}, uploadTime > {uploadTime}")


        except Exception as e:
            print(f"Network error: {e}")  
            TimeStamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            log=open(errorLog,'a')
            log.write(TimeStamp)   
            log.write(' Error in Uploading')   
            log.write(str(e))   
            log.write('\n')
            log.close()   
            
        # print(f"Time: '{time_Diff}', Status: '{machine_Status}', CountDiff: '{count_Diff}', RPM: '{machine_RPM}', Machine Speed: '{machine_Speed}' Meter/sec , Total Production: '{production_Total}' ,Machine Count: '{machine_Count}'")
except Exception as e:
    ser.close()
    GPIO.cleanup()
    TimeStamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    log=open(errorLog,'a')
    log.write(TimeStamp)
    log.write('Error in Program ')   
    log.write(str(e))   
    log.write('\n')
    log.close()   
    print("Serial communication closed.")
    print(e)