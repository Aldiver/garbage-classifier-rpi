import evdev

class RFIDReader:
    def __init__(self, device_name="IC Reader IC Reader"):
        """
        Initialize the RFID reader.
        :param device_name: The name of the RFID device as shown in evdev.
        """
        self.device_name = device_name
        self.device = None

    def find_device(self):
        """
        Find the RFID reader device from the list of input devices.
        """
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for dev in devices:
            if dev.name == self.device_name:
                self.device = evdev.InputDevice(dev.path)
                print(f"RFID reader found: {self.device.name} at {self.device.path}")
                return
        raise Exception(f"RFID reader '{self.device_name}' not found.")

    def read_card(self):
        """
        Read RFID card data.
        :return: The scanned RFID tag as a string.
        """
        if not self.device:
            print("RFID reader device is not initialized.")
            return None

        print("Waiting for RFID card... Press Ctrl+C to exit.")
        try:
            rfid_data = ""
            for event in self.device.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    if key_event.keystate == evdev.KeyEvent.key_down:
                        key = evdev.ecodes.KEY[key_event.scancode]
                        if key == "KEY_ENTER":
                            return rfid_data  # Return the full RFID data when Enter is detected
                        rfid_data += key.lstrip("KEY_").lower()  # Append key to RFID data
        except KeyboardInterrupt:
            print("\nExiting RFID reader...")
        return None

# Example usage
if __name__ == "__main__":
    rfid_reader = RFIDReader(device_name="IC Reader IC Reader")
    try:
        rfid_reader.find_device()
        while True:
            card_data = rfid_reader.read_card()
            if card_data:
                print(f"RFID card detected: {card_data}")
    except Exception as e:
        print(f"Error: {e}")
