import customtkinter as ctk
import tkinter as tk
import requests

from utils.utils import API_URL

class Leaderboard(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)
        self.student = None

        # Store the navigation callback
        self.navigate_callback = navigate_callback

        # Grid configuration
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Frame (75% of width)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # Right Frame (25% of width)
        self.right_frame = ctk.CTkFrame(self, fg_color="white")
        self.right_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        # Title for Top 10
        title = ctk.CTkLabel(self.right_frame, text="Top 10 Leaderboard", font=("Arial", 28, "bold"), fg_color="white", bg_color="white")
        title.pack(pady=20)

        # Add "Back" button in the top-left of the frame
        back_button = ctk.CTkButton(self.left_frame, text="Back", command=self.navigate_callback(("main_menu")))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def update_with_student_data(self, student_data):
        """
        Update the leaderboard with student data fetched from an API.
        The `student_data` parameter should contain the student's RFID,
        which will be used to fetch leaderboard information from the API.
        """
        self.student = student_data
        self.get_leaderboard(student_data['rfid'])

    def get_leaderboard(self, rfid):
        """
        Fetch leaderboard data from the server.
        """
        try:
            url = f"{API_URL}/leaderboard/{self.student['rfid']}"
            response = requests.get(url)
            if response.status_code == 200:
                leaderboard_data = response.json()
                self.display_leaderboard(leaderboard_data)
            else:
                print(f"Error: {response.json()['message']}")
        except Exception as e:
            print(f"Error fetching leaderboard: {e}")

    def display_leaderboard(self, leaderboard_data):
        """
        Display the leaderboard data in the left frame.
        """
        # Clear the left frame first
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Add "Back" button in the top-left of the frame
        back_button = ctk.CTkButton(self.left_frame, text="Back", command=self.navigate_callback(("main_menu")))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Display the top 10 users in the left frame
        for i, student in leaderboard_data['leaderboard']:
            name = student['alias']
            points = student['current_points']
            label = ctk.CTkLabel(
                self.right_frame,
                text=f"{i}. {name} -> {points}",
                font=("Arial", 24),
                fg_color="black",
                bg_color="black",
                text_color="yellow" if student['rank'] == leaderboard_data['student_rank'][0]['rank'] else "white"  # Highlight user
            )
            label.pack(pady=5)

        # Display the surrounding students (3 above, 3 below)
        for student in leaderboard_data['student_rank']:
            name = student['alias']
            points = student['current_points']
            label = ctk.CTkLabel(
                self.left_frame,
                text=f"{student['rank']}. {name} -> {points}",
                font=("Arial", 24),
                fg_color="black",
                bg_color="black",
                text_color="yellow" if student['rank'] == leaderboard_data['student_rank'][0]['rank'] else "white"
            )
            label.pack(pady=5)
