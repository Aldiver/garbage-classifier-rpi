import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
from utils.rfid_util import scan_rfid
from utils.utils import API_URL


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback
        self.stop_scanning = False  # Flag to control the scanning loop

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
    def read_rfid(self):
        """Scan the RFID and handle the process without blocking the main UI."""
        if not self.stop_scanning:
            rfid_number = scan_rfid()  # Call the utility function to scan RFID
            if rfid_number:
                print(f"Scanned RFID Number: {rfid_number}")
                self.send_rfid_to_server(rfid_number)
            else:
                # If no RFID is scanned, try again after 1 second
                self.after(1000, self.scan_rfid)  # Check again in 1 second

    def start_rfid_scanning(self):
        """Start the RFID scanning without threading, using after method."""
        self.stop_scanning = False  # Reset the stop flag
        self.read_rfid()  # Call the scan_rfid method directly

    def stop_rfid_scanning(self):
        """Stop the RFID scanning loop."""
        self.stop_scanning = True

    def send_rfid_to_server(self, rfid):
        """Send the RFID data to the server and process the response."""
        url = f"{API_URL}/rfid/{rfid}"
        print(f"Sending request to: {url}")

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                student = data.get('student')

                # RFID found, stop scanning and show success
                self.show_success_modal("RFID found!", student)

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
        submit_button = ctk.CTkButton(form_modal, text="Submit", command=lambda: self.add_student_to_server(form_modal, rfid, alias_input, first_name_input, last_name_input, middle_name_input, email_input, password_input, current_points_value))
        submit_button.pack(pady=10)

    def add_student_to_server(self, modal, rfid, alias, first_name, last_name, middle_name, email, password, points):
        """Add the student to the server and display a confirmation modal."""
        modal.destroy()

        # Logic to add student (POST request) here
        # After success, navigate to main menu
        self.show_success_modal("Student added successfully!", {"rfid": rfid, "alias": alias.get()})
