from evdev import InputDevice, ecodes, list_devices
from select import select

keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
dev = InputDevice("/dev/input/by-id/usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd")

barcode = ""
while True:
    r,w,x = select([dev], [], [])

    for event in dev.read():
        if event.type != 1 or event.value != 1:
            continue
        if event.code == 28:
            print(barcode)
            barcode = ""
            break
        barcode += keys[event.code]
