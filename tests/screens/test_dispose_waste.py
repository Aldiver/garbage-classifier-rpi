import customtkinter as ctk

class TestDisposeWaste(ctk.CTkFrame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Dispose Waste")
        label.pack(pady=20)
        button = ctk.CTkButton(self, text="Back to Main Menu", command=lambda: show_frame("main_menu"))
        button.pack(pady=10)
