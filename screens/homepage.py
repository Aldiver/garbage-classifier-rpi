import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import serial
import requests
import threading
import pyudev  # For automatic USB port detection
from utils.utils import API_URL
import time

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

    def find_rfid_port(self, vendor_id, product_id):
        """Find the USB port based on vendor and product ID."""
        context = pyudev.Context()
        for device in context.list_devices(subsystem='tty'):
            if device.parent:
                vendor_id_attr = device.parent.attributes.get('ID_VENDOR_ID', None)
                product_id_attr = device.parent.attributes.get('ID_MODEL_ID', None)

                # Check if vendor and product IDs match
                if vendor_id_attr == vendor_id and product_id_attr == product_id:
                    return device.device_node
        return None


    def scan_rfid(self):
        """Function to scan RFID, send data to the server, and handle response."""
        # Define the vendor and product ID of your RFID scanner
        vendor_id = 'ffff'  # Change this based on your device info
        product_id = '0035'  # Change this based on your device info

        # Find the correct port for the RFID scanner
        port = self.find_rfid_port(vendor_id, product_id)

        if port:
            try:
                ser = serial.Serial(port, 9600, timeout=1)
                test_sent = False  # Flag to check if test RFID was sent
                start_time = time.time()  # Record the start time
                # Open serial connection on the detected port
                ser = serial.Serial(port, 9600, timeout=1)
                while True:

                    if not test_sent and (time.time() - start_time >= 5):
                        self.send_rfid_to_server("12346579")  # Send test RFID
                        test_sent = True  # Set the flag to indicate test RFID was sent
                    rfid = ser.readline().decode().strip()
                    if rfid:
                        self.send_rfid_to_server(rfid)

            except serial.SerialException as e:
                # Show an error if the RFID scanner is not found
                self.show_error_modal(f"RFID scanner not found: {e}")
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
