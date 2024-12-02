import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
from utils.rfid_util import RFIDReader
from utils.utils import API_URL, center_modal
from PIL import Image


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback, set_student_data_callback):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback
        self.set_student_data = set_student_data_callback

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center frame
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")

        # RFID image
        self.rfid_image = ctk.CTkImage(light_image=Image.open("images/homepage.png"), size=(1280, 720))
        self.rfid_label = ctk.CTkLabel(self.frame, image=self.rfid_image, text="")  # Empty text to display only the image
        self.rfid_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the RFID image

        # Initialize the RFID reader and start scanning
        self.rfid_reader = RFIDReader(callback=self.handle_rfid_scan)

        # Start RFID scanning when the homepage is loaded

    def start_scanning(self):
        self.rfid_reader.start()

    def handle_rfid_scan(self, rfid_number):
        """
        Handle the scanned RFID number.
        :param rfid_number: The RFID data scanned.
        """
        print(f"Scanned RFID Number: {rfid_number}")

        self.send_rfid_to_server(rfid_number)

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
        """
        Display a success modal with a 200x200 size, then navigate after 2 seconds.
        """
        modal = ctk.CTkToplevel(self)
        modal.title("Success")

        # Set the modal size
        modal_width = 200
        modal_height = 200

        # Get the centered position using the utility function
        position_left, position_top = center_modal(self, modal_width, modal_height)
        print(f"SUCCESS: {modal_width}x{modal_height}+{position_left}+{position_top}")
        modal.geometry(f"{modal_width}x{modal_height}+{position_left}+{position_top}")

        label = ctk.CTkLabel(modal, text=message, wraplength=180, justify="center")
        label.pack(pady=20)

        ok_button = ctk.CTkButton(
            modal, text="OK",
            command=lambda: [
                modal.destroy(),
                self.set_student_data(student), #store student data to App.py
                self.after(500, lambda: self.navigate_callback("main_menu"))
            ]
        )
        ok_button.pack(pady=10)


    def show_error_modal(self, message):
        """
        Display an error modal with a 200x200 size.
        """
        modal = ctk.CTkToplevel(self)
        modal.title("Error")

        # Set the modal size
        modal_width = 200
        modal_height = 200

        # Get the centered position using the utility function
        position_left, position_top = center_modal(self, modal_width, modal_height)
        print(f"{modal_width}x{modal_height}+{position_left}+{position_top}")
        modal.geometry(f"{modal_width}x{modal_height}+{position_left}+{position_top}")

        label = ctk.CTkLabel(modal, text=message, wraplength=180, justify="center")
        label.pack(pady=20)

        ok_button = ctk.CTkButton(modal, text="OK", command=modal.destroy)
        ok_button.pack(pady=10)


    def show_add_student_modal(self, rfid):
        """Show a modal to add a student if RFID is not found."""
        modal = ctk.CTkToplevel(self)
        modal.title("No Record Found")

        # Set the modal size
        modal_width = 400
        modal_height = 400

        # Get the centered position using the utility function
        position_left, position_top = center_modal(self, modal_width, modal_height)
        modal.geometry(f"{modal_width}x{modal_height}+{position_left}+{position_top}")

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

        # Set the modal size
        modal_width = 400
        modal_height = 450

        # Get the centered position using the utility function
        position_left, position_top = center_modal(self, modal_width, modal_height)
        form_modal.geometry(f"{modal_width}x{modal_height}+{position_left}+{position_top}")

        # Configure grid layout with padding
        form_modal.columnconfigure(0, weight=1)
        form_modal.columnconfigure(1, weight=1)

        # Input fields
        rfid_label = ctk.CTkLabel(form_modal, text="RFID:")
        rfid_label.grid(row=0, column=0, sticky="w", padx=(20, 10), pady=(10, 5))
        rfid_input = ctk.CTkEntry(form_modal)
        rfid_input.insert(0, rfid)  # Insert RFID value
        rfid_input.configure(state="readonly")  # Make the field readonly
        rfid_input.grid(row=0, column=1, padx=(10, 20), pady=(10, 5))

        alias_label = ctk.CTkLabel(form_modal, text="Alias:")
        alias_label.grid(row=1, column=0, sticky="w", padx=(20, 10), pady=(5, 5))
        alias_input = ctk.CTkEntry(form_modal)
        alias_input.grid(row=1, column=1, padx=(10, 20), pady=(5, 5))

        first_name_label = ctk.CTkLabel(form_modal, text="First Name:")
        first_name_label.grid(row=2, column=0, sticky="w", padx=(20, 10), pady=(5, 5))
        first_name_input = ctk.CTkEntry(form_modal)
        first_name_input.grid(row=2, column=1, padx=(10, 20), pady=(5, 5))

        last_name_label = ctk.CTkLabel(form_modal, text="Last Name:")
        last_name_label.grid(row=3, column=0, sticky="w", padx=(20, 10), pady=(5, 5))
        last_name_input = ctk.CTkEntry(form_modal)
        last_name_input.grid(row=3, column=1, padx=(10, 20), pady=(5, 5))

        middle_name_label = ctk.CTkLabel(form_modal, text="Middle Name (optional):")
        middle_name_label.grid(row=4, column=0, sticky="w", padx=(20, 10), pady=(5, 5))
        middle_name_input = ctk.CTkEntry(form_modal)
        middle_name_input.grid(row=4, column=1, padx=(10, 20), pady=(5, 5))

        # Default value for current points
        # current_points_label = ctk.CTkLabel(form_modal, text="Current Points:")
        # current_points_label.grid(row=5, column=0, sticky="w", padx=(20, 10), pady=(5, 5))
        # current_points_value = ctk.CTkLabel(form_modal, text="0")
        # current_points_value.grid(row=5, column=1, padx=(10, 20), pady=(5, 5))

        # Email and password fields for authentication
        email_label = ctk.CTkLabel(form_modal, text="Email:")
        email_label.grid(row=6, column=0, sticky="w", padx=(20, 10), pady=(5, 5))
        email_input = ctk.CTkEntry(form_modal)
        email_input.grid(row=6, column=1, padx=(10, 20), pady=(5, 5))

        password_label = ctk.CTkLabel(form_modal, text="Password:")
        password_label.grid(row=7, column=0, sticky="w", padx=(20, 10), pady=(5, 5))
        password_input = ctk.CTkEntry(form_modal, show="*")
        password_input.grid(row=7, column=1, padx=(10, 20), pady=(5, 5))

        # Submit button
        submit_button = ctk.CTkButton(
            form_modal, text="Submit",
            command=lambda: self.add_student_to_server(
                form_modal, rfid,
                alias_input.get(),
                first_name_input.get(),
                last_name_input.get(),
                middle_name_input.get() if middle_name_input.get() else None,
                email_input.get(),
                password_input.get()
            )
        )

        submit_button.grid(row=8, column=0, columnspan=2, pady=(20, 10))

    def add_student_to_server(self, modal, rfid, alias, first_name, last_name, middle_name, email, password):
        """Submit the new student data to the backend after authentication."""
        modal.destroy()

        # Verify user email and password for authentication
        if not email or not password:
            self.show_error_modal("Email and password are required.")
            return

        # Send the request to the backend to create the student
        try:
            url = f"{API_URL}/students"
            print(f"Sending request to: {url}")
            student_data = {
                "rfid": rfid,
                "alias": alias,
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "email": email,
                "password": password
            }
            print(student_data)
            response = requests.post(url, json=student_data)
            print(response)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Student added successfully!")
                self.navigate_callback("main_menu")  # Navigate to the main menu after success
            else:
                self.show_error_modal("Failed to add student. Please try again.")

        except requests.RequestException as e:
            self.show_error_modal(f"Error contacting server: {e}")
