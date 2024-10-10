import customtkinter as ctk
import tkinter as tk

class CheckPoints(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback, username="", points=0):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback
        self.student = None

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Points Display
        self.points_circle = ctk.CTkLabel(self, text=str(points), font=("Arial", 60), bg_color="black", fg_color="white")
        self.points_circle.pack(expand=True)

        # Greeting Label
        points_text = "points" if points != 1 else "point"
        self.greeting = ctk.CTkLabel(self, text=f"Hello {username}, this is your current {points_text}.", font=("Arial", 24), fg_color="white", bg_color="black")
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
        self.student = student_data
        self.points_circle.configure(text=str(student_data['current_points']))
        student_info = f"Hello {student_data['first_name']} {student_data['last_name']}, this is your current point/s."
        self.greeting.configure(text=student_info)

        self.info_label.configure(text=f"Student ID: {student_data['id']}")
