# utils.py

API_URL = "http://192.168.1.162:8000/api"

def center_modal(window, modal_width, modal_height):
    """
    Calculate the position to center the modal on the screen and return it.
    """
    screen_width = 1024
    screen_height = 600

    print(f"Screen Width = {screen_width} \n Screen Height = {screen_height}")
    # Calculate the position to center the modal
    position_top = (screen_height // 2) - (modal_height // 2)
    position_left = (screen_width // 2) - (modal_width // 2)

    return position_left, position_top
