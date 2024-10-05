import customtkinter as ctk
import tkinter as tk

class CheckPoints(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback, username, points):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Points Display
        self.points_circle = ctk.CTkLabel(self, text=str(points), font=("Arial", 60), bg_color="black", fg_color="white")
        self.points_circle.pack(expand=True)

        # Greeting
        points_text = "points" if points != 1 else "point"
        self.greeting = ctk.CTkLabel(self, text=f"Hello {username}, this is your current {points_text}.", font=("Arial", 24), fg_color="white", bg_color="black")
        self.greeting.pack(pady=20)

        # Bottom Buttons
        self.bottom_frame = ctk.CTkFrame(self, fg_color="black")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.leaderboard_button = ctk.CTkButton(self.bottom_frame, text="Leaderboard", fg_color="green", border_color="white", width=200, command=lambda: self.navigate_callback("leaderboard"))
        self.leaderboard_button.pack(side=tk.LEFT, padx=20)

        self.skip_button = ctk.CTkButton(self.bottom_frame, text="Skip", fg_color="red", width=200, command=lambda: self.navigate_callback("main_menu"))
        self.skip_button.pack(side=tk.RIGHT, padx=20)

if __name__ == "__main__":
    app = CheckPoints(username="John", points=10)
    app.mainloop()
