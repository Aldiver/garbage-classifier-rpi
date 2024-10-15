import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import pyudev  # For automatic USB port detection
import time  # For time tracking
from utils.utils import API_URL

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback
        self.stop_scanning = False  # Flag to control the scanning thread

        # Find the RFID port upon instantiation
        self.port = self.find_rfid_port()

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center frame
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=(20, 20), sticky="nsew")

        # RFID Text
        self.scan_text = ctk.CTkLabel(self.frame, text="Scan your RFID", font=("Arial", 24), bg_color="black", fg_color="white")
        self.scan_text.pack(pady=20)

        # Start RFID scanning when the homepage is loaded
        self.start_rfid_scanning()

    def start_rfid_scanning(self):
        """Start the RFID scanning in a separate thread."""
        self.stop_scanning = False  # Reset the stop flag
        threading.Thread(target=self.scan_rfid, daemon=True).start()

    def stop_rfid_scanning(self):
        """Stop the RFID scanning loop."""
        self.stop_scanning = True

    def find_rfid_port(self):
        """Check if the HID device is available. This method is for demonstration purposes."""
        context = pyudev.Context()
        for device in context.list_devices(subsystem='hidraw'):
            print(f"Checking device: {device.device_node}")
            if device.device_node == '/dev/hidraw1':
                return device.device_node
        return None

    def scan_rfid(self):
        """Function to scan RFID, send data to the server, and handle response."""
        if self.port:  # Ensure the port was found during instantiation
            try:
                with open(self.port, 'rb') as f:
                    test_sent = False  # Flag to check if test RFID was sent
                    start_time = time.time()  # Record the start time
                    rfid = False  # Placeholder for RFID data

                    while not self.stop_scanning:  # Loop until stop_scanning is set to True
                        print(time.time())

                        # Send a test RFID after 5 seconds
                        if not test_sent and (time.time() - start_time >= 5):
                            self.send_rfid_to_server("12346579")  # Send test RFID
                            test_sent = True  # Test RFID has been sent

                        # Simulate RFID reading
                        # rfid_data = f.read(8)  # Adjust based on the expected length of the RFID
                        # rfid = rfid_data.decode('utf-8', errors='ignore').strip()

                        # Check if an RFID was read
                        if rfid:
                            print(f"RFID Read: {rfid}")
                            time.sleep(0.5)  # Add a delay to ensure the scan is complete
                            self.send_rfid_to_server(rfid)

            except Exception as e:
                self.show_error_modal(f"Error reading RFID scanner: {e}")
        else:
            self.show_error_modal("RFID scanner not found.")

    def send_rfid_to_server(self, rfid):
        """Send the RFID data to the server and process the response."""
        url = f"{API_URL}/rfid/{rfid}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                student = data.get('student')

                # RFID found, stop scanning and show success
                self.show_success_modal("RFID found!", student)
                self.stop_rfid_scanning()  # Stop scanning once RFID is processed

            else:
                # No student found, continue scanning
                self.show_error_modal("No student record found")

        except requests.RequestException as e:
            # Server error, continue scanning
            self.show_error_modal(f"Error contacting server: {e}")

    def show_success_modal(self, message, student):
        """Display a success modal, then navigate after 2 seconds."""
        messagebox.showinfo("Success", message)
        self.after(2000, lambda: self.navigate_callback("main_menu", student_data=student))

    def show_error_modal(self, message):
        """Display an error modal."""
        messagebox.showerror("Error", message)
