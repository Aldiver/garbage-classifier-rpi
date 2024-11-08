import hid
import time

def read_rfid_device(device_path='/dev/hidraw0'):
    # Open the HID device
    try:
        h = hid.device()
        h.open_path(device_path)
        print(f"Opened device: {device_path}")

        print("Waiting for RFID scan...")
        while True:
            # Read from the device
            data = h.read(64)  # Read up to 64 bytes (size may vary)
            if data:
                # Process data
                print("Scanned RFID:", data)
                # Here you would decode or process the RFID data
                # For example, if it's in a particular format, decode it

    except Exception as e:
        print(f"Error reading from device: {e}")

if __name__ == "__main__":
    read_rfid_device('/dev/hidraw0')
