import random
import customtkinter as ctk
import tkinter as tk

from screens.check_point import CheckPoints
from screens.dispose_waste import DisposeWaste
from screens.homepage import HomePage
from screens.leaderboards import Leaderboard
from screens.main_menu import MainMenu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Navigation Example")
        # self.geometry("1080x720")
        self.attributes("-fullscreen", True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a dictionary to hold all the pages
        self.pages = {}

        # Store the student data globally within the app (initially None)
        self.student_data = None

        # Track the currently visible frame
        self.current_frame = None

        # Initialize the frames (pages)
        self.create_frames()

        # Show the homepage initially
        self.show_frame("homepage")

    def create_frames(self):
        all_users = [(f"User{i}", random.randint(1, 100)) for i in range(1, 101)]
        user_rank = 25

        # Create and store each frame, passing the navigation callback
        self.pages["homepage"] = HomePage(self, self.show_frame, self.set_student_data)
        self.pages["main_menu"] = MainMenu(self, self.show_frame)
        self.pages["check_points"] = CheckPoints(self, self.show_frame, username="", points=0)
        self.pages["leaderboard"] = Leaderboard(self, self.show_frame)
        self.pages["dispose_waste"] = DisposeWaste(self, self.show_frame)

        # Place each frame in the root window
        for frame_name, frame in self.pages.items():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.pages.values():
            frame.grid_forget()

        if frame_name == "homepage":
            self.student_data = None

        # Pass the student data to the frame if needed
        frame = self.pages[frame_name]
        if self.student_data:
            if hasattr(frame, 'update_with_student_data'):
                frame.update_with_student_data(self.student_data)

        self.current_frame = frame_name

        if frame_name == "dispose_waste":
            self.pages["dispose_waste"].start_detection()  # Run object detection for dispose_waste
            # TODO: Implement the object detection method in DisposeWaste

        # Show the requested frame
        frame.grid(row=0, column=0, sticky="nsew")

    def set_student_data(self, student_data):
        """
        Update the current student data and trigger navigation if needed.
        """
        self.student_data = student_data
        print(f"Student data updated: {self.student_data}")

if __name__ == "__main__":
    # Initialize customtkinter appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
