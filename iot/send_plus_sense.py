import json
import requests
import random
import time
from datetime import datetime
import argparse
from sense_hat import SenseHat
import threading
from evdev import InputDevice, list_devices, categorize, ecodes

# assumming this is running on a raspberry pi with a sense hat
# draw a smiley face on the sense hat

w = (150, 150, 150)
b = (56, 126, 184)
e = (0, 0, 0)
g = (53, 133, 61)
r = (255, 0, 0)

sense = SenseHat()

smiley_face = [
    e, e, e, e, e, e, e, e,
    w, w, w, e, e, w, w, w,
    w, b, w, e, e, w, b, w,
    w, w, w, e, e, w, w, w,
    e, e, e, e, e, e, e, e,
    e, w, e, e, e, e, w, e,
    e, e, w, w, w, w, e, e,
    e, e, e, e, e, e, e, e
]

sad_face = [
    e, e, e, e, e, e, e, e,
    e, e, e, w, w, e, e, e,
    e, e, w, e, e, w, e, e,
    e, e, e, e, e, e, e, e,
    e, w, e, e, e, e, w, e,
    e, e, e, e, e, e, e, e,
    e, w, w, w, w, w, w, e,
    e, e, e, e, e, e, e, e
]

arrow_up = [
    e, e, e, e, e, e, e, e,
    e, e, e, w, w, e, e, e,
    e, e, w, w, w, w, e, e,
    e, w, e, w, w, e, w, e,
    w, e, e, w, w, e, e, w,
    e, e, e, w, w, e, e, e,
    e, e, e, w, w, e, e, e,
    e, e, e, w, w, e, e, e
]

# This script generates random weight between 0 and 2 (Kg) data and sends it to the url specified in the parameters
# the url is defined with a host and a port
# if a time interval is specified, the script will send data every interval seconds
# if no time interval is specified, the script will run once and send one data point

# usage example:
# python post_weight.py --host localhost --port 8080 --api /api/weight --interval 1
# python post_weight.py --host Dell-Carlos --port 8003 --api /api/current_dish_weight/add

# the host (the server running the api) is, in my case, the name of my computer (Dell-Carlos) because I am running the server in my computer
# and the Raspberry Pi is connected to the same network as my computer
# if you are running the server in a different computer, you will need to specify the ip address of that computer

# the port is 8003
# the api is /api/current_dish_weight/add/{weight}/{timestamp} where {weight} is the current weight of the dish and {timestamp} is the current time in utc format
# to send this you make a post request to the url http://{host}:8003/api/current_dish_weight/add/{weight}/{timestamp}

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--host', help='host name', required=True)
parser.add_argument('--port', help='port number', required=True)
parser.add_argument('--api', help='api url', required=True)
parser.add_argument(
    '--interval', help='time interval in seconds', required=False)
args = parser.parse_args()

# define url
url = 'http://' + args.host + ':' + args.port + args.api

# define headers
headers = {'Content-Type': 'application/json'}

devices = [InputDevice(path) for path in list_devices()]
dev = None

# define time interval
if args.interval:
    interval = int(args.interval)
else:
    interval = 0

current_barcode = '0'
# generate random weight data


def generate_weight():
    # Here is where you would get the weight from the scale and return it
    # for now, we will generate random weight data
    weight = random.uniform(0, 2)
    # round to 2 decimal places
    weight = round(weight, 2)
    return weight

# send data to url


def send_data():
    # generate weight data
    weight = generate_weight()
    # get current time in utc format
    #timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = datetime.utcnow().isoformat() + 'Z'
    # create payload
    payload = {'weight': weight, 'timestamp': timestamp}
    # convert payload to json
    payload = json.dumps(payload)
    # send data
    url = 'http://' + args.host + ':' + \
        args.port + args.api + '/' + str(weight) + "/" + timestamp
    print("url: \n", url)
    response = requests.post(url, headers=headers)
    # print response
    print(response.text)
    
def send_rfid(barcode):
    
    payload = {'message': "rfid", 'value': barcode}
    # convert payload to json
    payload = json.dumps(payload)
    # send data
    url = 'http://' + args.host + ':' + \
        args.port + '/api/registered_barcode/'+ str(barcode)
    print("url: \n", url)
    response = requests.post(url, headers=headers)
    # print response
    print(response.text)
    
def read_barcode(callback):
    '''
    Function that reads a single input from the barcode scanner
    and calls the callback function with the string of the barcode
    Input: callback function that takes a string argument
    Output: None
    '''
    for device in devices:
        
        if device.name == "USB Adapter USB Device" and device.phys.startswith('usb-3f980000'):
            dev = device
            break

    if dev is None:
        print("Device not found")
        return
    
    barcode = ''
    print("waiting barcode")

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            if data.keystate == 1:  # key down events only
                key = data.keycode[4:] if data.keycode.startswith('KEY_') else ''
                if key.isdigit():
                    barcode += key
                elif key == 'ENTER':
                    print('barcode scanned: ', barcode)
                    callback(barcode)
                    barcode = ''

if __name__ == '__main__':

    sense.set_pixels(smiley_face)
    # send data every interval seconds
    # callibrate the accelerometer to detect vertical movement
    # if vertical movement is detected, send data
    
    # read barcode
    t = threading.Thread(target=read_barcode, args=(send_rfid,))
    t.start()

    print("running...")

    while True:
        # get accelerometer data
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']
        # detect vertical movement of the board
        if x > 0.5 or x < -0.5 or y > 0.5 or y < -0.5:
            sense.set_pixels(arrow_up)
            send_data()
            time.sleep(1)
            sense.set_pixels(smiley_face)
        