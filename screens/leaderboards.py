import customtkinter as ctk
import tkinter as tk
import random

class Leaderboard(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback, user_rank, all_users):
        super().__init__(parent)

        # Store the navigation callback
        self.navigate_callback = navigate_callback

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sort all users by points in descending order
        self.sorted_users = sorted(all_users, key=lambda x: x[1], reverse=True)
        self.user_rank = user_rank

        # Left Frame (75% of width)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # Right Frame (25% of width)
        self.right_frame = ctk.CTkFrame(self, fg_color="white")
        self.right_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        # Display Top 10 on the right
        self.display_top_10()

        # Wait for the frame to be fully rendered and then display user rank
        self.after(100, self.display_user_rank)  # Delay in milliseconds

    def display_top_10(self):
        title = ctk.CTkLabel(self.right_frame, text="Top 10 Leaderboard", font=("Arial", 28, "bold"), fg_color="white", bg_color="white")
        title.pack(pady=20)

        for i, (name, points) in enumerate(self.sorted_users[:10]):
            label = ctk.CTkLabel(
                self.right_frame,
                text=f"{i+1}. {name} -> {points}",
                font=("Arial", 24),
                fg_color="white",
                bg_color="white"
            )
            label.pack(pady=5)

    def display_user_rank(self):
        # Update and ensure frame is fully rendered
        self.update_idletasks()

        available_width = self.left_frame.winfo_width()  # Get width of the left frame
        available_height = self.left_frame.winfo_height() / 7  # Allocate height per user display

        print(f"available width = {available_width}")
        print(f"available height = {available_height}")

        # Fetch users to display: top 3 above and 3 below the user
        start_index = max(self.user_rank - 4, 0)
        end_index = min(self.user_rank + 3, len(self.sorted_users))

        display_users = self.sorted_users[start_index:end_index]

        # Dynamically adjust font size for the user's rank
        max_font_size = self.calculate_max_font_size(f"{self.user_rank}. {display_users[3][0]} -> {display_users[3][1]}", available_width)

        # Print out the calculated font sizes for visualization
        print("Calculated Font Sizes:")
        title = ctk.CTkLabel(self.left_frame, text="Top 10 Leaderboard", font=("Arial", 28, "bold"), fg_color="white", bg_color="white")
        title.pack(pady=20)
        for i, (name, points) in enumerate(display_users):
            rank = start_index + i + 1
            if rank == self.user_rank:
                font_size = max_font_size
            else:
                scale_factor = 0.8 ** abs(self.user_rank - rank)  # Scale font size by 20% for each rank away from the user
                font_size = int(max_font_size * scale_factor)
            print(f"Rank {rank}: Font Size = {font_size}")
            label = self.create_label(rank, name, points, font_size)
            label.pack(pady=5)

    def create_label(self, rank, name, points, font_size):
        return ctk.CTkLabel(
            self.left_frame,
            text=f"{rank}. {name} -> {points}",
            font=("Arial", font_size),
            fg_color="black",
            bg_color="black",
            text_color="yellow" if rank == self.user_rank else "white"  # Highlight color for the user
        )

    def calculate_max_font_size(self, text, max_width):
        # Start with a large font size and decrease until it fits the width
        font_size = 100
        test_label = ctk.CTkLabel(self.left_frame, text=text, font=("Arial", font_size))
        test_label.pack()
        test_label.update_idletasks()

        while test_label.winfo_reqwidth() > max_width and font_size > 10:
            font_size -= 1
            test_label.configure(font=("Arial", font_size))
            test_label.update_idletasks()

        test_label.destroy()
        return font_size

if __name__ == "__main__":
    # Initialize customtkinter appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create 100 users with random points for testing
    all_users = [(f"User{i}", random.randint(1, 100)) for i in range(1, 101)]

    # Assume we want to highlight User25's rank
    user_rank = 25

    app = Leaderboard(user_rank=user_rank, all_users=all_users)
    app.mainloop()
