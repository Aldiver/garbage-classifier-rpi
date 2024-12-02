import customtkinter as ctk
import tkinter as tk
import requests

from utils.utils import API_URL  # Make sure to import your API_URL if needed

class CheckPoints(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="#0077B6")

        # Store the navigation callback
        self.navigate_callback = navigate_callback
        self.student = None  # This will hold the student data

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Container Frame for Centering
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.pack(expand=True)

        # Circle Canvas
        self.circle_canvas = tk.Canvas(
            self.center_frame,
            width=300,
            height=300,
            bg="#0077B6",  # Match theme background color
            highlightthickness=0
        )

        self.circle_canvas.create_oval(
            10, 10, 290, 290,
            outline="white",
            width=5
        )  # Circle
        self.circle_canvas.pack()

        # Points Display (Inside the Circle)
        self.points_circle = ctk.CTkLabel(
            self.circle_canvas,
            text=str(0),
            font=("Arial", 48),
            fg_color="#0077B6",  # Match canvas color
            text_color="white"
        )
        self.points_circle.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Greeting Label
        self.greeting = ctk.CTkLabel(
            self.center_frame,
            text=f"Hello #NoDataLoaded, this is your current point/s.",
            font=("Arial", 24),
            text_color="white" if ctk.get_appearance_mode() == "Light" else "white",  # Adjust text color based on theme
        )
        self.greeting.pack(pady=(50,10))

       # Info Label
        self.info_label = ctk.CTkLabel(
            self.center_frame,
            text=f"Student ID: 25",
            font=("Arial", 18),
            text_color="white" if ctk.get_appearance_mode() == "Light" else "white",  # Adjust text color based on theme
        )
        self.info_label.pack(pady=5)

        # Bottom Buttons
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#0077B6")
        self.bottom_frame.pack(side=tk.BOTTOM, pady=20)

        self.skip_button = ctk.CTkButton(
            self.bottom_frame,
            text="Back to Main Menu",
            width=200,
            height=50,
            fg_color="#003a6c",
            command=lambda: navigate_callback("main_menu"),
        )
        self.skip_button.pack(side=tk.LEFT, padx=20)

        self.leaderboard_button = ctk.CTkButton(
            self.bottom_frame,
            text="Leaderboard",
            width=200,
            height=50,
            fg_color="#003a6c",
            command=lambda: navigate_callback("leaderboard"),
        )
        self.leaderboard_button.pack(side=tk.RIGHT, padx=20)

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
            print(f"CheckPoints API fetch: {self.student}")

            response = requests.get(url)

            if response.status_code == 200:
                # Update points and UI with the fetched data
                data = response.json()
                self.points_circle.configure(text=str(data['points']))
                self.greeting.configure(text=f"Hello {self.student['first_name']} {self.student['last_name']}, this is your current point/s.")
                self.info_label.configure(text=f"Student ID: {self.student['id']}")

            else:
                # Handle errors if student not found
                self.greeting.configure(text="Student not found.")
                self.info_label.configure(text="")
        except Exception as e:
            print(f"Error fetching points: {e}")
            self.greeting.configure(text="Error fetching points.")
            self.info_label.configure(text="")
