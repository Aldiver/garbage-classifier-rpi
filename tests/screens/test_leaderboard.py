import customtkinter as ctk

class TestLeaderboard(ctk.CTkFrame):
    def __init__(self, parent, show_frame, user_rank=1, all_users=[]):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Leaderboard")
        label.pack(pady=20)
        rank_label = ctk.CTkLabel(self, text=f"Your Rank: {user_rank}")
        rank_label.pack(pady=10)
        button = ctk.CTkButton(self, text="Back to Main Menu", command=lambda: show_frame("main_menu"))
        button.pack(pady=10)
