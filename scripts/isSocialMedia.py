import win32gui
import time

def isSocialMedia(socialMediaList):
    win = win32gui.GetForegroundWindow()
    fullName = str(win32gui.GetWindowText(win))
    if "https://" in fullName or "http://" in fullName:
        fullName = "Pop-up Window"
    time.sleep(1)
    for socialMedia in socialMediaList:
        if socialMedia.lower() in fullName.lower():
            return True
        else:
            return False
