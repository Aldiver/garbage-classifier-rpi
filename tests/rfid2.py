import time
from evdev import InputDevice, ecodes

def read_rfid_from_device(device_path):
    """Read RFID tag from the device."""
    try:
        # Open the device
        dev = InputDevice(device_path)
        print(f"Opened device: {dev}")

        # Loop to capture events
        print("Waiting for RFID scan...")
        while True:
            for event in dev.read():
                # Check if the event is a key press
                if event.type == ecodes.EV_KEY:
                    key_event = ecodes.KEY[event.code]
                    if event.value == 1:  # key down event
                        print(f"Key pressed: {key_event}")

                        # Process RFID scan here (e.g., print scanned tag or trigger a function)
                        if key_event == 'KEY_ENTER':
                            print("RFID scan completed!")
                            # Stop the loop or handle the scanned RFID
                            return
            time.sleep(0.1)

    except Exception as e:
        print(f"Error reading from device: {e}")

if __name__ == "__main__":
    # The device is detected at /dev/input/event5 for your Sycreader
    rfid_device_path = '/dev/input/event5'
    read_rfid_from_device(rfid_device_path)
