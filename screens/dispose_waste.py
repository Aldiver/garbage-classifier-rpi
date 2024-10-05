import customtkinter as ctk
import tkinter as tk

class DisposeWaste(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback

        # Layout configuration
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Frame (75% of width)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")

        # Right Frame (25% of width)
        self.right_frame = ctk.CTkFrame(self, fg_color="white")
        self.right_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

        self.status_label = ctk.CTkLabel(self.left_frame, text="Scanning...", font=("Arial", 36), fg_color="white", bg_color="black")
        self.status_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.camera_label = ctk.CTkLabel(self.right_frame, text="Camera Feed Here", font=("Arial", 24), fg_color="black", bg_color="white")
        self.camera_label.pack(pady=20)

        self.details_label = ctk.CTkLabel(self.right_frame, text="Details Below Camera", font=("Arial", 18), fg_color="black", bg_color="white")
        self.details_label.pack(pady=10)

if __name__ == "__main__":
    app = DisposeWaste()
    app.mainloop()
