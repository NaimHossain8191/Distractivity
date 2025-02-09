from PIL import Image
import sys
import ctypes
import pystray

def create_tray_icon():
    # Load the tray icon image
    try:
        image = Image.open("./icon/icon.png")
    except FileNotFoundError:
        print("Tray icon image not found. Ensure 'icon.png' exists in the './icon/' directory.")
        return
    
    def on_open(icon, item):
        if sys.platform == 'win32':
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 5)

    # Create the tray icon with a menu
    icon = pystray.Icon(
        "Distractivity",
        image,
        title="Distractivity",
        menu=pystray.Menu(
            pystray.MenuItem("Open", on_open)
        )
    )

    # Run the icon
    icon.run()
def hide_window():
    if sys.platform == 'win32':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)  # 0 = SW_HIDE