from evdev import InputDevice, list_devices, categorize, ecodes

def read_input():
    devices = [InputDevice(path) for path in list_devices()]
    dev = None
    for device in devices:
        if device.name == "USB Adapter USB Device" and device.phys == "usb-3f980000.usb-1.4/input0":
            dev = device
            break

    if dev is None:
        print("Device not found")
        return
    barcode = ''

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            if data.keystate == 1:  # key down events only
                key = data.keycode[4:] if data.keycode.startswith('KEY_') else ''
                if key.isdigit():
                    barcode += key
                elif key == 'ENTER':
                    print('barcode scanned: ', barcode)
                    barcode = ''

if __name__ == '__main__':
    read_input()