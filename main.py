import threading
import time
from scripts.isSocialMedia import isSocialMedia
from scripts.printCalendar import print_colored_calendar
from scripts.updateJSON import update_json
from scripts.tray import create_tray_icon, hide_window
import json

# List of social media to track
# Not scrolling anymore, promise 👀
socialMediaList = ["Facebook", "Youtube"]

# Dates, but make it digital. 💾
days_file = "dates.json"

# Load date colors from the JSON file 🔴🟢🟡
def load_date_colors(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# "nah, we done here" 🛑
stop_program = False

# "Eyes on you, fam 👀"
def monitor_social_media():
    global stop_program
    while not stop_program:
        # See if you’re still vibing on socials 👀
        is_active = isSocialMedia(socialMediaList)
        update_json(days_file, is_active)
        # It's time to take some rest!
        time.sleep(1)

# Dealing with your thoughts 🤔
def handle_user_input():
    global stop_program
    
    while not stop_program:
        user_input = input(">>> ").strip().lower()
        if user_input == "print":
            date_colors = load_date_colors(days_file)
            print_colored_calendar(date_colors)
        elif user_input == "exit":
            stop_program = True
            print("Exiting the program...")
        elif user_input == "minimize":
            hide_window()


def main():
    hide_window()
    print("Social Media Tracker is running...")
    print("Type 'print' to see your usage statistics or 'exit' to stop.")
    
    # Eyes on you in a separate thread 👀
    monitor_thread = threading.Thread(target=monitor_social_media, daemon=True)
    monitor_thread.start()

    # Thread for the tray icon
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()

    # Handle your thoughts
    handle_user_input()

if __name__ == "__main__":
    main()
