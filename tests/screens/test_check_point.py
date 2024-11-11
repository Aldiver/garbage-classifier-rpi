import customtkinter as ctk

class TestCheckPoints(ctk.CTkFrame):
    def __init__(self, parent, show_frame, username="User", points=0):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text=f"Check Points\nUser: {username}\nPoints: {points}")
        label.pack(pady=20)
        button = ctk.CTkButton(self, text="Back to Main Menu", command=lambda: show_frame("main_menu"))
        button.pack(pady=10)
