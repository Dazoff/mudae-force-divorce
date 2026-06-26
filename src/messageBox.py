import random
import mss
import cv2
import numpy as np
import pyautogui
import pyperclip
import time
import os
import sys

def getFilePath(filename):
    basePath = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(basePath, filename)

def findMessageBox(application):
    with mss.MSS() as sct:
        monitor = {
            "left": application.left,
            "top": application.top,
            "width": application.width,
            "height": application.height
        }
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) 

        needle = cv2.imread(getFilePath('./images/messagebox.png'))
        needle_height, needle_width = needle.shape[:2]

        result = cv2.matchTemplate(img, needle, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= 0.8:
            center_x = max_loc[0] + needle_width // 2
            center_y = max_loc[1] + needle_height // 2

            abs_x = application.left + center_x
            abs_y = application.top + center_y

            return (abs_x, abs_y)
        else:
            return None


def writeMessageBox(message, confirmation):
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.sleep(random.uniform(0.5, 1.5)) 
        pyautogui.press("enter")

        pyperclip.copy("")  # Clear clipboard after pasting

        if confirmation == "y":
            time.sleep(random.uniform(2.5, 3.7))
            pyautogui.press("y")
            pyautogui.sleep(random.uniform(0.5, 1.5))
            pyautogui.press("enter")

def clickMessageBox(application, message, confirmation):
    position = findMessageBox(application)

    if position is not None:
        pyautogui.click(position[0], position[1])
        pyautogui.sleep(random.uniform(0.5, 1.5))

        writeMessageBox(message, confirmation)
        return True
    else:
        print("Could not click message box because it was not found")
        return False