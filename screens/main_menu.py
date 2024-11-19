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

        self.show_points_icon = ctk.CTkLabel(self.left_frame, text="Show Points", font=("Arial", 36))
        self.show_points_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.show_points_icon.bind("<Button-1>", self.on_show_points_click)  # Also make the label clickable

        # Right Frame: Dispose Waste
        self.right_frame = ctk.CTkFrame(self, fg_color="grey")
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.right_frame.bind("<Button-1>", self.on_dispose_waste_click)  # Bind click event to the right frame

        self.dispose_waste_icon = ctk.CTkLabel(self.right_frame,text_color="white", text="Dispose Waste", font=("Arial", 36))
        self.dispose_waste_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.dispose_waste_icon.bind("<Button-1>", self.on_dispose_waste_click)  # Also make the label clickable

    def on_show_points_click(self, event):
        """Navigate to the Check Points screen."""
        self.navigate_callback("check_points")

    def on_dispose_waste_click(self, event):
        """Navigate to the Dispose Waste screen."""
        self.navigate_callback("dispose_waste")
