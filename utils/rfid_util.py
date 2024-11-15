import evdev
import threading

class RFIDReader:
    def __init__(self, device_name="IC Reader IC Reader", callback=None):
        """
        Initialize the RFID reader.
        :param device_name: The name of the RFID device as shown in evdev.
        :param callback: A function to call when an RFID card is scanned.
        """
        self.device_name = device_name
        self.device = None
        self.callback = callback  # Callback to handle detected RFID
        self.running = False

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

    def read_loop(self):
        """
        Continuously listen for RFID card scans and invoke the callback.
        """
        if not self.device:
            print("RFID reader device is not initialized.")
            return

        self.running = True
        try:
            rfid_data = ""
            for event in self.device.read_loop():
                if not self.running:
                    break

                if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    if key_event.keystate == evdev.KeyEvent.key_down:
                        key = evdev.ecodes.KEY[key_event.scancode]
                        if key == "KEY_ENTER":
                            if self.callback:
                                self.callback(rfid_data)  # Invoke callback with RFID data
                            rfid_data = ""  # Reset for next read
                        else:
                            rfid_data += key.lstrip("KEY_").lower()  # Append to RFID data
        except Exception as e:
            print(f"Error in RFID read loop: {e}")

    def start(self):
        """
        Start the RFID reader loop in a separate thread.
        """
        if not self.device:
            self.find_device()
        thread = threading.Thread(target=self.read_loop, daemon=True)
        thread.start()

    def stop(self):
        """
        Stop the RFID reader loop.
        """
        self.running = False
