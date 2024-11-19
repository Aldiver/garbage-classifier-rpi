import customtkinter as ctk
import requests
from utils.utils import API_URL

class Leaderboard(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="#0077B6")
        self.student = None

        # Store the navigation callback
        self.navigate_callback = navigate_callback

        # Grid configuration for the main frame
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

        # Grid configuration for left_frame (30% for button and title, 70% for labels)
        self.left_frame.grid_rowconfigure(0, weight=1)  # Top 30% for button and title
        self.left_frame.grid_rowconfigure(1, weight=3)  # Bottom 70% for the labels_frame
        self.left_frame.grid_columnconfigure(1, weight=1)

        # Add "Back" button in the top-left of the frame
        self.back_button = ctk.CTkButton(self.left_frame, fg_color="white", text_color="black", text="Back", command=self.on_back_button_click)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add the title for the left frame
        self.title_label = ctk.CTkLabel(self.left_frame, text="User Ranking", font=("Arial", 24, "bold"), text_color="black")
        self.title_label.grid(row=0, column=1, padx=10, pady=10)

        # Create a new frame for the leaderboard labels inside left_frame
        self.labels_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.labels_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")

        # Grid configuration for labels_frame to center its content
        self.labels_frame.grid_columnconfigure(0, weight=1)
        self.labels_frame.grid_rowconfigure(0, weight=1)

        # Start the timer to navigate to the homepage if not clicked within 5 seconds
        self.navigate_timer = None

    def on_back_button_click(self):
        """
        This method is called when the 'Back' button is clicked.
        It cancels the timer and navigates back to the main menu.
        """
        try:
            if self.navigate_timer is not None:  # Ensure the timer is not None
                self.after_cancel(self.navigate_timer)  # Cancel the navigate timer
                self.navigate_timer = None
            self.navigate_callback("main_menu")  # Navigate to the main menu
        except Exception as e:
            print(f"Error in on_back_button_click: {e}")  # Log the error to console
            # Optionally, add a fallback or error message for the user if needed

    def navigate_homepage(self):
        """
        This method automatically navigates to the homepage after 5 seconds if the 'Back' button is not clicked.
        """
        print(f"Leaderboards page. Waiting for input")
        self.after(5000, self.navigate_callback("homepage"))

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
        # Clear the labels_frame first (only remove previous leaderboard labels)
        for widget in self.labels_frame.winfo_children():
            widget.destroy()

        # Display the top 10 users in the right frame
        for index, student in enumerate(leaderboard_data['leaderboard']):
            name = student['alias']
            points = student['current_points']
            label = ctk.CTkLabel(
                self.right_frame,
                text=f"{index + 1}. {name} -> {points}",  # Use index + 1 for ranking
                font=("Arial", 24),
                text_color="white" if student['rank'] == leaderboard_data['student_rank'][0]['rank'] else "black"  # Highlight user
            )
            label.pack(pady=5)

        # Display the surrounding students (3 above, 3 below) in the labels_frame
        for student in leaderboard_data['student_rank']:
            name = student['alias']
            points = student['current_points']
            label = ctk.CTkLabel(
                self.labels_frame,
                text=f"{student['rank']}. {name} -> {points}",
                font=("Arial", 24),
                text_color="white" if student['rank'] == leaderboard_data['student_rank'][0]['rank'] else "black"
            )
            label.pack(pady=5)  # Center the labels in the frame
