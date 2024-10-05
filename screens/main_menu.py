import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

         # Left Frame (75% of width)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.show_points_icon = ctk.CTkLabel(self.left_frame, text="Show Points", font=("Arial", 36), fg_color="white", bg_color="green")
        self.show_points_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Right Frame (25% of width)
        self.right_frame = ctk.CTkFrame(self, fg_color="white")
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.dispose_waste_icon = ctk.CTkLabel(self.right_frame, text="Dispose Waste", font=("Arial", 36), fg_color="white", bg_color="blue")
        self.dispose_waste_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
