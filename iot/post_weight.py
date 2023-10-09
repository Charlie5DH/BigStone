import json
import requests
import random
import time
from datetime import datetime
import argparse
from sense_hat import SenseHat

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

# define time interval
if args.interval:
    interval = int(args.interval)
else:
    interval = 0

# generate random weight data


def generate_weight():
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


if __name__ == '__main__':

    sense.set_pixels(smiley_face)
    # send data every interval seconds
    # callibrate the accelerometer to detect vertical movement
    # if vertical movement is detected, send data

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
        # if no movement, sleep for interval seconds
        else:
            time.sleep(interval)
