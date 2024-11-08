import evdev

# Open the device (ensure this matches your device name or path)
device = evdev.InputDevice('/dev/input/event5')  # Replace with your event path

# Function to filter out unwanted keys like 'Enter'
def process_rfid_input():
    rfid_input = ""
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.value == 1:  # Key press
                key = evdev.ecodes.KEY[event.code]

                # Filter out the 'Enter' key (code 28 or 13) or any other unwanted keys
                if key != 'KEY_ENTER':
                    rfid_input += key[-1]  # Get last character of the key string (e.g., '1' from 'KEY_1')

            if event.value == 0:  # Key release
                pass

        # Stop when 'Enter' (code 28) is pressed
        if 'KEY_ENTER' in locals() and rfid_input.endswith("Enter"):
            rfid_input = rfid_input.rstrip('Enter')  # Remove "Enter"
            break

    return rfid_input

# Call the function to get the filtered RFID input
rfid_code = process_rfid_input()
print(f"RFID Input so far: {rfid_code}")
