# raspberry

https://www.notion.so/Python-978fc2e64c2440ea9a16fe6fec21c4d2

## LED On/Off

```jsx
from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)

```

## DHT
https://github.com/adafruit/Adafruit_CircuitPython_DHT  
pip3 install adafruit-circuitpython-dht  
sudo apt-get install libgpiod2  

dht.py
```python
import adafruit_dht
from board import D18
dht_device = adafruit_dht.DHT11(D18)
temperature = dht_device.temperature
humidity = dht_device.humidity
print(temperature, humidity)
```
python3 dht.py

## UBIDOTS example

```jsx
$ pip install requests 

import time
import requests
import math
import random
import Adafruit_DHT

sensor = Adafruit_DHT.AM2302
gpio_pin = 4
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxx" 
DEVICE_LABEL = "GICT2020"  
VARIABLE_LABEL_1 = "temperature" 
VARIABLE_LABEL_2 = "humidity" 

def build_payload(variable_1, variable_2):
    # temperature = random.randint(-10, 50)
    # humidity = random.randint(0, 85)
    humidity, temperature = Adafruit_DHT.read_retry(sensor,gpio_pin)
    payload = {variable_1: temperature ,variable_2: humidity}
    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(15)
```

```jsx
import time
import requests
import math
from gpiozero import LED
from time import sleep

TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GPIO_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
led = LED(17)

def get_request():
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/variables/{}".format(url, GPIO_ID)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    status = 400
    attempts = 0
    req =""
    while status >= 400 and attempts <= 5:
        req = requests.get(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        time.sleep(1)
    # Processes results
    if status >= 400:
        return False

    response =req.json()
    return response["last_value"]["value"]

def main():

    if get_request()==1.0:
        led.on()
        print("[INFO] LED ON")
    else:
        led.off()
        print("[INFO] LED OFF")

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
```
