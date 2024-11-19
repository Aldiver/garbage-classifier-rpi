# utils.py

API_URL = "http://192.168.1.162:8000/api"

def center_modal(window, modal_width, modal_height):
    """
    Calculate the position to center the modal on the screen and return it.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the modal
    position_top = (screen_height // 2) - (modal_height // 2)
    position_left = (screen_width // 2) - (modal_width // 2)

    return position_left, position_top
