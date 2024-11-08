import evdev

# List all available input devices (this will help you identify the correct device path)
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(f"Found device: {device}")

# Open the device (use the correct event path from the output above)
device_path = '/dev/input/event5'  # Replace with your actual event path
device = evdev.InputDevice(device_path)

# Function to process RFID input and filter out unwanted keys
def process_rfid_input():
    rfid_input = ""
    for event in device.read_loop():
        # Print event data for debugging
        print(f"Received event: {event}")

        if event.type == evdev.ecodes.EV_KEY:
            key = evdev.ecodes.KEY[event.code]
            print(f"Key pressed: {key}")

            # If key press (value 1), add it to the input string, filter 'Enter' key
            if event.value == 1:
                if key != 'KEY_ENTER':
                    rfid_input += key[-1]  # Get the last character (e.g., '1' from 'KEY_1')

            # Stop reading after 'Enter' key (code 28)
            if event.value == 0 and 'KEY_ENTER' in locals() and rfid_input.endswith("Enter"):
                rfid_input = rfid_input.rstrip('Enter')  # Remove "Enter"
                break

    return rfid_input

# Call the function to get the filtered RFID input
rfid_code = process_rfid_input()
print(f"RFID Input so far: {rfid_code}")
