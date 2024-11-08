import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import pyudev
import time
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
                    rfid = ""  # Placeholder for RFID data

                    while not self.stop_scanning:  # Loop until stop_scanning is set to True
                        # Send a test RFID after 5 seconds
                        # if not test_sent and (time.time() - start_time >= 5):
                            # self.send_rfid_to_server("12346579")  # Send test RFID
                            # test_sent = True  # Test RFID has been sent

                        # Read a chunk of data from the RFID reader
                        rfid_data = f.read(1).decode('utf-8', errors='ignore')  # Read one byte at a time
                        rfid += rfid_data  # Append to the RFID buffer

                        # Check if the RFID data ends with a newline (indicating scan completion)
                        if rfid.endswith('\n'):
                            rfid = rfid.strip()  # Remove any whitespace and newline characters
                            if rfid:  # If we have valid RFID data
                                print(f"RFID Read: {rfid}")
                                time.sleep(0.5)  # Delay to allow scan completion
                                self.send_rfid_to_server(rfid)
                            rfid = ""  # Reset RFID buffer for the next read

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
                    # No student found, prompt to add a new student
                    self.show_add_student_modal(rfid)

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

        def show_add_student_modal(self, rfid):
            """Show a modal to add a student if RFID is not found."""
            modal = ctk.CTkToplevel(self)
            modal.title("No Record Found")
            modal.geometry("400x400")

            label = ctk.CTkLabel(modal, text="No record found, do you want to add this student?")
            label.pack(pady=10)

            yes_button = ctk.CTkButton(modal, text="Yes", command=lambda: self.show_add_student_form(modal, rfid))
            yes_button.pack(pady=10)

            no_button = ctk.CTkButton(modal, text="No", command=modal.destroy)
            no_button.pack(pady=10)

        def show_add_student_form(self, modal, rfid):
            """Display the student form to add a new student."""
            modal.destroy()

            # Create a new modal for adding the student
            form_modal = ctk.CTkToplevel(self)
            form_modal.title("Add Student")
            form_modal.geometry("400x500")

            # Input fields
            rfid_label = ctk.CTkLabel(form_modal, text="RFID:")
            rfid_label.pack(pady=5)
            rfid_input = ctk.CTkEntry(form_modal, state="disabled", value=rfid)
            rfid_input.pack(pady=5)

            alias_label = ctk.CTkLabel(form_modal, text="Alias:")
            alias_label.pack(pady=5)
            alias_input = ctk.CTkEntry(form_modal)
            alias_input.pack(pady=5)

            first_name_label = ctk.CTkLabel(form_modal, text="First Name:")
            first_name_label.pack(pady=5)
            first_name_input = ctk.CTkEntry(form_modal)
            first_name_input.pack(pady=5)

            last_name_label = ctk.CTkLabel(form_modal, text="Last Name:")
            last_name_label.pack(pady=5)
            last_name_input = ctk.CTkEntry(form_modal)
            last_name_input.pack(pady=5)

            middle_name_label = ctk.CTkLabel(form_modal, text="Middle Name (optional):")
            middle_name_label.pack(pady=5)
            middle_name_input = ctk.CTkEntry(form_modal)
            middle_name_input.pack(pady=5)

            # Default value for current points
            current_points_label = ctk.CTkLabel(form_modal, text="Current Points:")
            current_points_label.pack(pady=5)
            current_points_value = ctk.CTkLabel(form_modal, text="0")
            current_points_value.pack(pady=5)

            # Email and password fields for authentication
            email_label = ctk.CTkLabel(form_modal, text="Email:")
            email_label.pack(pady=5)
            email_input = ctk.CTkEntry(form_modal)
            email_input.pack(pady=5)

            password_label = ctk.CTkLabel(form_modal, text="Password:")
            password_label.pack(pady=5)
            password_input = ctk.CTkEntry(form_modal, show="*")
            password_input.pack(pady=5)

            # Submit button
            submit_button = ctk.CTkButton(form_modal, text="Submit", command=lambda: self.submit_new_student(form_modal, rfid, alias_input, first_name_input, last_name_input, middle_name_input, email_input, password_input))
            submit_button.pack(pady=20)

        def submit_new_student(self, form_modal, rfid, alias_input, first_name_input, last_name_input, middle_name_input, email_input, password_input):
            """Submit the new student data to the backend after authentication."""
            # Get the input values
            alias = alias_input.get()
            first_name = first_name_input.get()
            last_name = last_name_input.get()
            middle_name = middle_name_input.get() if middle_name_input.get() else None
            email = email_input.get()
            password = password_input.get()

            # Verify user email and password for authentication
            if not email or not password:
                self.show_error_modal("Email and password are required.")
                return

            # Send the request to the backend to create the student
            try:
                url = f"{API_URL}/students"
                data = {
                    "rfid": rfid,
                    "alias": alias,
                    "first_name": first_name,
                    "last_name": last_name,
                    "middle_name": middle_name,
                    "email": email,
                    "password": password
                }

                response = requests.post(url, json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Student added successfully!")
                    form_modal.destroy()
                    self.navigate_callback("main_menu")  # Navigate to the main menu after success
                else:
                    self.show_error_modal("Failed to add student. Please try again.")

            except requests.RequestException as e:
                self.show_error_modal(f"Error contacting server: {e}")
