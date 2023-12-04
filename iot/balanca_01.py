# Import necessary modules
from machine import Pin, UART
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import time

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)
led = Pin("LED", Pin.OUT)
#uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart = UART(1)

def setup():
    uart.init(bits=8, parity=None, stop=1, baudrate=9600, tx=Pin(4), rx=Pin(5),timeout=10)
    led.on()
    

def on_rx(data):
    dados=0 
    print("Data received: ", data)  # Print the received data
    if data == b'troca\r\n':  # Check if the received data is "toggle"
        if led.value():
            led.off()
        else:
            led.on()
        uart.write(b'\x05')
        uart.flush();
        time.sleep_ms(100)
        if uart.any():
#        dados= uart.read(7) # == b'txgo\n' :
            sp.send("Peso = ")
            sp.send(uart.read())
            sp.send(b'\r\n')
#            print("UART DATA recebido",uart.read())
#        loop = True
        #Initiate uart loop
#        while loop:
#            if uart.any():
#                print("passou 1")
#                readed = uart.read()
#                print("passou 2")
#                if readed == b'ok\r\n':
#                    led.toggle()
#                    loop = False
#                    uart.write('toggle\r\n')
#            time.sleep(1)


def loop():
    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception


if __name__ == "__main__":
    setup()
    loop()
