import customtkinter as ctk
from PIL import Image

class TestHomePage(ctk.CTkFrame):
    def __init__(self, parent, show_frame):
        super().__init__(parent)

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center frame
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")

        # RFID image
        self.rfid_image = ctk.CTkImage(light_image=Image.open("images/homepage.png"), size=(1280, 720))
        self.rfid_label = ctk.CTkLabel(self.frame,  image=self.rfid_image, text="")  # Empty text to display only the image
        self.rfid_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the RFID image
