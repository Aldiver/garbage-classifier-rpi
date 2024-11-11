import customtkinter as ctk
import random

# Import placeholder frames (testing versions of your screens)
from test_homescreen import TestHomePage
from test_main_menu import TestMainMenu
from test_check_point import TestCheckPoints
from test_leaderboard import TestLeaderboard
from test_dispose_waste import TestDisposeWaste

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Navigation Test App")
        self.attributes("-fullscreen", True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Dictionary to hold all pages
        self.pages = {}
        # Track the currently visible frame
        self.current_frame = None

        # Initialize and create frames (pages)
        self.create_frames()

        # Show the homepage initially
        self.show_frame("homepage")

    def create_frames(self):
        all_users = [(f"User{i}", random.randint(1, 100)) for i in range(1, 101)]
        user_rank = 25

        # Create and store each frame
        self.pages["homepage"] = TestHomePage(self, self.show_frame)
        self.pages["main_menu"] = TestMainMenu(self, self.show_frame)
        self.pages["check_points"] = TestCheckPoints(self, self.show_frame, username="TestUser", points=42)
        self.pages["leaderboard"] = TestLeaderboard(self, self.show_frame, user_rank=user_rank, all_users=all_users)
        self.pages["dispose_waste"] = TestDisposeWaste(self, self.show_frame)

        # Place each frame in the root window
        for frame_name, frame in self.pages.items():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.pages.values():
            frame.grid_forget()

        # Show the requested frame
        frame = self.pages[frame_name]
        frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = frame_name

if __name__ == "__main__":
    # Initialize customtkinter appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
