# Import necessary modules
from machine import Pin, UART
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import time

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Create a Pin object for the onboard LED, configure it as an output
led = Pin("LED", Pin.OUT)

# Initialize the LED state to 0 (off)
led_state = 0

# Initialize UART
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
# Configure UART parameters
uart.init(bits=8, parity=None, stop=1)

# Define a callback function to handle received data


def on_rx(data):
    print("Data received: ", data)  # Print the received data
    global led_state  # Access the global variable led_state
    if data == b'toggle\n':  # Check if the received data is "toggle"
        led.value(not led_state)  # Toggle the LED state (on/off)
        led_state = 1 - led_state  # Update the LED state
        loop = True
        # Initiate uart loop
        while loop:
            uart.write('toggle')
            if uart.any():
                readed = uart.read()
                if readed == b'ok':
                    led.toggle()
                    loop = False
            time.sleep(1)


# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  # Set the callback function for data reception
