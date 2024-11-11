import customtkinter as ctk

class TestMainMenu(ctk.CTkFrame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Main Menu")
        label.pack(pady=20)
        button1 = ctk.CTkButton(self, text="Check Points", command=lambda: show_frame("check_points"))
        button2 = ctk.CTkButton(self, text="Dispose Waste", command=lambda: show_frame("dispose_waste"))
        button1.pack(pady=10)
        button2.pack(pady=10)
