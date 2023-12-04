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
    uart.init(bits=8, parity=None, stop=1, baudrate=9600, tx=Pin(4), rx=Pin(5))
    led.on()
    


def on_rx(data):
    dados=0 
#    print("Data received: ", data)  # Print the received data
    if data == b'troca\r\n':  # Check if the received data is "toggle"
        if led.value():
            led.off()
        else:
            led.on()
        uart.write('\x05')
        uart.flush();
        time.sleep_ms(100)
        if uart.any():
            dados= uart.read(7)
#            print(dados.strip('\x02'))
            if dados.startswith('\x02')  and  dados.endswith('\x03') :
#                dados=dados.lstrip(b'\x02')
#                dados=dados.lstrip('0')
#                dados=dados.rstrip('\x03')
                print(dados[1:6])
                sp.send("Peso = ")
                sp.send(dados[1:6])
                sp.send('\r\n')
            else:
                sp.send('Deu algum problema')
            time.sleep(1)


def loop():
    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception


if __name__ == "__main__":
    setup()
    loop()
