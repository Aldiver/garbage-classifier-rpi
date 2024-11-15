import customtkinter as ctk
import tkinter as tk
import requests

from utils.utils import API_URL  # Make sure to import your API_URL if needed

class CheckPoints(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback
        self.student = None  # This will hold the student data

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Points Display
        self.points_circle = ctk.CTkLabel(self, text=str(0), font=("Arial", 60), bg_color="black", fg_color="white")
        self.points_circle.pack(expand=True)

        # Greeting Label
        self.greeting = ctk.CTkLabel(self, text=f"Loading Data", font=("Arial", 24), fg_color="white", bg_color="black")
        self.greeting.pack(pady=20)

        # Info Label
        self.info_label = ctk.CTkLabel(self, text="", font=("Arial", 20), fg_color="white", bg_color="black")
        self.info_label.pack(pady=10)

        # Bottom Buttons
        self.bottom_frame = ctk.CTkFrame(self, fg_color="black")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.leaderboard_button = ctk.CTkButton(self.bottom_frame, text="Leaderboard", fg_color="green", border_color="white", width=200, command=lambda: self.navigate_callback("leaderboard"))
        self.leaderboard_button.pack(side=tk.LEFT, padx=20)

        self.skip_button = ctk.CTkButton(self.bottom_frame, text="Skip", fg_color="red", width=200, command=lambda: self.navigate_callback("main_menu"))
        self.skip_button.pack(side=tk.RIGHT, padx=20)

    def update_with_student_data(self, student_data):
        """
        Update the UI with the student data and fetch the points.
        """
        self.student = student_data  # Store the student data directly in the prop
        # Display student info initially
        student_info = f"Hello {student_data['first_name']} {student_data['last_name']}, loading your points..."
        self.greeting.configure(text=student_info)
        self.update()

        # Fetch points for the student using their RFID
        self.fetch_student_points(student_data['rfid'])

    def fetch_student_points(self, rfid):
        """
        Fetch student's current points from the API.
        """
        try:
            url = f"{API_URL}/points/{rfid}"  # Update with correct API URL
            response = requests.get(url)

            if response.status_code == 200:
                # Update points and UI with the fetched data
                data = response.json()
                self.points_circle.configure(text=str(data['points']))
                self.greeting.configure(text=f"Hello {self.student['first_name']} {self.student['last_name']}, your current points are {data['points']}.")
                self.info_label.configure(text=f"Student ID: {self.student['id']}")
                
            else:
                # Handle errors if student not found
                self.greeting.configure(text="Student not found.")
                self.info_label.configure(text="")
        except Exception as e:
            print(f"Error fetching points: {e}")
            self.greeting.configure(text="Error fetching points.")
            self.info_label.configure(text="")
