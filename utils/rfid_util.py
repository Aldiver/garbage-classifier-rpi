import evdev

# Specify the RFID reader device name
reader = "Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader"

# Initialize the device and authcode list
device = None
authcode = []
rfid_number = ""  # Variable to store the entire RFID number

# Conversion table to map evdev key codes to characters (adding "Enter" for the return key)
conversionTable = {
    11: '0',     # Key '0'
    2: '1',      # Key '1'
    3: '2',      # Key '2'
    4: '3',      # Key '3'
    5: '4',      # Key '4'
    6: '5',      # Key '5'
    7: '6',      # Key '6'
    8: '7',      # Key '7'
    9: '8',      # Key '8'
    10: '9',     # Key '9'
    28: 'Enter'  # Enter key
}

# Function to map the input event array to a string
def mapInput(inputEventArray):
    input_str = ""
    for event in inputEventArray:
        if event.code in conversionTable:
            input_str += conversionTable[event.code]
    return input_str

def find_rfid_device():
    """Find the RFID reader device."""
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for dev in devices:
        if dev.name == reader:
            return evdev.InputDevice(dev.path)
    return None

def scan_rfid():
    """Scan the RFID and return the number."""
    global device, rfid_number, authcode
    device = find_rfid_device()
    if device is None:
        print("No Device")
        return None

    rfid_number = ""  # Reset the RFID number
    authcode = []  # Clear the authcode list

    # Start reading events from the device
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.value == 1:
                if event.code != 28:
                    authcode.append(event)
            elif event.value == 0:
                if len(authcode) > 0:
                    input_str = mapInput(authcode)
                    rfid_number += input_str  # Append to rfid_number
                    authcode = []  # Reset the authcode list after processing

                    # If the RFID scan is complete (Enter key pressed)
                    if event.code == 28:
                        return rfid_number
