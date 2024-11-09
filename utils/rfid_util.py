import evdev
import threading

class RFIDReader:
    """Class to handle RFID scanning in a separate thread and store the last scanned RFID number."""

    def __init__(self):
        self.reader_name = "Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader"
        self.device = self.find_rfid_device()
        self.rfid_number = None
        self.authcode = []
        self.conversion_table = {
            11: '0', 2: '1', 3: '2', 4: '3', 5: '4',
            6: '5', 7: '6', 8: '7', 9: '8', 10: '9',
            28: 'Enter'
        }

    def find_rfid_device(self):
        """Find the RFID reader device."""
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for dev in devices:
            if dev.name == self.reader_name:
                return evdev.InputDevice(dev.path)
        return None

    def map_input(self, input_event_array):
        """Convert the event codes into an RFID string."""
        return ''.join(self.conversion_table[event.code] for event in input_event_array if event.code in self.conversion_table)

    def scan_rfid_loop(self):
        """Main loop to scan RFID and update `rfid_number`."""
        if not self.device:
            print("RFID reader device not found.")
            return

        self.rfid_number = ""  # Clear the last scanned number
        self.authcode = []

        for event in self.device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.value == 1 and event.code != 28:  # Key press and not Enter
                    self.authcode.append(event)
                elif event.value == 0:  # Key release
                    if self.authcode:
                        input_str = self.map_input(self.authcode)
                        self.rfid_number += input_str
                        self.authcode = []
                    if event.code == 28:  # Enter key signals end of scan
                        return self.rfid_number  # Return complete RFID number

    def start_scanning(self):
        """Start a thread that continually scans for RFID."""
        threading.Thread(target=self.scan_rfid_loop, daemon=True).start()

    def get_rfid_number(self):
        """Return the current RFID number."""
        return self.rfid_number
