from evdev import InputDevice, ecodes

def read_rfid_device(device_path='/dev/hidraw0'):
    device = InputDevice(device_path)
    print(f"Opened device: {device}")

    # Wait for RFID scan
    print("Waiting for RFID scan...")
    while True:
        try:
            for event in device.read():
                if event.type == ecodes.EV_KEY and event.value == 1:  # Key press event
                    print(f"Scanned RFID: {event}")
        except OSError as e:
            if e.errno == 11:  # Resource temporarily unavailable
                print("Device temporarily unavailable, retrying...")
                time.sleep(1)  # Retry after 1 second
                continue
            print(f"Error reading from device: {e}")
            break

if __name__ == "__main__":
    read_rfid_device()
