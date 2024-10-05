import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import itertools

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback

         # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center frame
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=(20, 20), sticky="nsew")

        # Logo
        # self.logo = Image.open("logo.png").resize((200, 200))
        # self.logo_img = ImageTk.PhotoImage(self.logo)
        # self.logo_label = ctk.CTkLabel(self.frame, image=self.logo_img, text="")
        # self.logo_label.pack(pady=20)

        # RFID Text
        self.scan_text = ctk.CTkLabel(self.frame, text="Scan your RFID", font=("Arial", 24), bg_color="black", fg_color="white")
        self.scan_text.pack(pady=20)

        # Example button to navigate to the main menu
        button = ctk.CTkButton(self.frame, text="Go to Main Menu", command=lambda: self.navigate_callback("main_menu"))
        button.pack(pady=20)

        # Loading Animation
        # self.loading_imgs = itertools.cycle([ImageTk.PhotoImage(Image.open(f"loading_{i}.png").resize((50, 50))) for i in range(1, 5)])
        # self.loading_label = ctk.CTkLabel(self.frame, text="")
        # self.loading_label.pack(pady=20)
        # self.rotate_loading()

    def rotate_loading(self):
        self.loading_label.configure(image=next(self.loading_imgs))
        self.after(100, self.rotate_loading)

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
