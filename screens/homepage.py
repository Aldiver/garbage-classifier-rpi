import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import serial
import requests
import threading
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

    def scan_rfid(self):
        """Function to scan RFID, send data to the server, and handle response."""
        try:
            # Open serial connection (adjust port and baudrate based on your RFID reader)
            ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

            while True:
                rfid = ser.readline().decode().strip()
                self.send_rfid_to_server("12346579")
                if rfid:
                    self.send_rfid_to_server(rfid)

        except serial.SerialException as e:
            # Show an error if the RFID scanner is not found
            self.send_rfid_to_server("12346579")
            self.show_error_modal(f"RFID scanner not found: {e}")


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
