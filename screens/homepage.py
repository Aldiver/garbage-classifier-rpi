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

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center frame
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=(20, 20), sticky="nsew")

        # RFID Text
        self.scan_text = ctk.CTkLabel(self.frame, text="Scan your RFID", font=("Arial", 24), bg_color="black", fg_color="white")
        self.scan_text.pack(pady=20)

        # Start RFID scanning in a separate thread
        threading.Thread(target=self.scan_rfid, daemon=True).start()

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
        # Find the correct port for the RFID scanner
        port = self.find_rfid_port()

        if port:
            try:
                print("Scanner found!")
                # Open the HID device for reading
                with open(port, 'rb') as f:
                    test_sent = False  # Flag to check if test RFID was sent
                    start_time = time.time()  # Record the start time
                    print("HID is open!")

                    while True:
                        print(time.time())
                        # Check if 5 seconds have passed to send the test RFID
                        if not test_sent and (time.time() - start_time >= 5):
                            self.send_rfid_to_server("12346579")  # Send test RFID

                            test_sent = True  # Set the flag to indicate test RFID was sent

                        rfid_data = f.read(8)  # Adjust based on the expected length of the RFID
                        rfid = rfid_data.decode('utf-8', errors='ignore').strip()

                        # Check if an RFID was read
                        if rfid:
                            print(f"RFID Read: {rfid}")
                            # Wait for the RFID scan to finish before sending
                            time.sleep(0.5)  # Add a delay to ensure the scan is complete
                            self.send_rfid_to_server(rfid)

            except Exception as e:
                self.show_error_modal(f"Error reading RFID scanner: {e}")
        else:
            # Fallback case if RFID scanner is not found
            self.show_error_modal("RFID scanner not found.")

    def send_rfid_to_server(self, rfid):
        """Send the RFID data to the server and process the response."""
        # Append the RFID path to the base URL
        url = f"{API_URL}/rfid/{rfid}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                student = data.get('student')
                # Show success modal and pass the student data to the callback
                self.show_success_modal("RFID found!", student)
            else:
                self.show_error_modal("No student record found")

        except requests.RequestException as e:
            self.show_error_modal(f"Error contacting server: {e}")

    def show_success_modal(self, message, student):
        """Display a success modal, then navigate after 2 seconds."""
        messagebox.showinfo("Success", message)
        self.after(2000, lambda: self.navigate_callback("main_menu", student_data=student))

    def show_error_modal(self, message):
        """Display an error modal."""
        messagebox.showerror("Error", message)
