import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="#0077B6")

        # Store the navigation callback
        self.navigate_callback = navigate_callback

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Frame: Show Points
        self.left_frame = ctk.CTkFrame(self, fg_color="white")
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.left_frame.bind("<Button-1>", self.on_show_points_click)  # Bind click event to the left frame

        self.show_points_icon = ctk.CTkLabel(self.left_frame, text_color="black", text="Show Points", font=("Arial", 36))
        self.show_points_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.show_points_icon.bind("<Button-1>", self.on_show_points_click)  # Also make the label clickable

        # Right Frame: Dispose Waste
        self.right_frame = ctk.CTkFrame(self, fg_color="grey")
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.right_frame.bind("<Button-1>", self.on_dispose_waste_click)  # Bind click event to the right frame

        self.dispose_waste_icon = ctk.CTkLabel(self.right_frame,text_color="white", text="Dispose Waste", font=("Arial", 36))
        self.dispose_waste_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.dispose_waste_icon.bind("<Button-1>", self.on_dispose_waste_click)  # Also make the label clickable
        self.navigate_timer = None

    def on_show_points_click(self, event):
        """Navigate to the Check Points screen."""
        try:
            if self.navigate_timer is not None:  # Ensure the timer is not None
                self.after_cancel(self.navigate_timer)  # Cancel the navigate timer
                self.navigate_timer = None
            self.navigate_callback("check_points")  # Navigate to the main menu
        except Exception as e:
            print(f"Error in on_back_button_click: {e}")  # Log the error to console
            # Optionally, add a fallback or error message for the user if needed


    def on_dispose_waste_click(self, event):
        """Navigate to the Dispose Waste screen."""
        try:
            if self.navigate_timer is not None:  # Ensure the timer is not None
                self.after_cancel(self.navigate_timer)  # Cancel the navigate timer
                self.navigate_timer = None
            self.navigate_callback("dispose_waste")
        except Exception as e:
            print(f"Error in on_back_button_click: {e}")  # Log the error to console
            # Optionally, add a fallback or error message for the user if needed


    def navigate_homepage(self):
        """
        This method automatically navigates to the homepage after 5 seconds if the 'Back' button is not clicked.
        """
        self.update()
        print(f"Leaderboards page. Waiting for input")
        self.navigate_timer = self.after(15000, lambda: self.navigate_callback("homepage"))
