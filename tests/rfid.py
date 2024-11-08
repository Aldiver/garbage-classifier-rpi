from pprint import pprint

import evdev
pprint = pprint
reader = "Sycreader RFID Technology Co."
device = evdev.InputDevice
authcode = []

conversionTable = {
    11: 0,
    2:1,
    3:2,
    4:3,
    5:4,
    6:5,
    7:6,
    8:7,
    9:8,
    10:9,
    28:"Enter"

}

def mapInput(inputEventArray):

    input = ""
    # pprint(inputEventArray)
    for event in inputEventArray:

        if event.code is not 28:
            input+=str(conversionTable[event.code])
    return input


def checkEntry():

    return

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:

    if device.name == reader:
        device = evdev.InputDevice(device.path)

for event in device.read_loop():

    if event.type == evdev.ecodes.EV_KEY :
        #on Key_Down
            if event.value == 1:
                authcode.append(event)

    if(len(authcode) == 11):

        input = mapInput(authcode)
        pprint(input)
        authcode = []
