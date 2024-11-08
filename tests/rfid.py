from pprint import pprint
import evdev

# Initialize the pprint function to print nicely
pprint = pprint

# Specify the RFID reader device name
reader = "Sycreader RFID Technology Co."

# Initialize the device and authcode list
device = evdev.InputDevice
authcode = []

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
        # Check the key code and map it to the correct character
        if event.code in conversionTable:
            input_str += conversionTable[event.code]
    return input_str

# # Get a list of all input devices
# devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

# # Loop through devices to find the matching RFID reader
# for dev in devices:
#     if dev.name == reader:
#         device = evdev.InputDevice(dev.path)

# Check if the device is found
# if device is None:
#     print("RFID Reader device not found.")
#     exit()

print(f"Device '{reader}' found, waiting for RFID scan...")

# Start reading events from the device
for event in device.read_loop():
    # Only process key events (EV_KEY)
    if event.type == evdev.ecodes.EV_KEY:
        # When a key is pressed (value = 1)
        if event.value == 1:
            # Add the event to the authcode list
            authcode.append(event)
        # When key is released (value = 0)
        elif event.value == 0:
            # Process the input if there are any collected key events
            if len(authcode) > 0:
                input_str = mapInput(authcode)
                print(f"Scanned RFID Input: {input_str}")
                authcode = []  # Reset the authcode list after processing
