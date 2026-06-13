import os
import pyautogui
import mss
import cv2
import time
import pygetwindow as gw
import numpy as np
import keyboard
import threading

pauseEvent = threading.Event()
pauseEvent.set()

def togglePause():
    if pauseEvent.is_set():
        print("Pausing script...")
        pauseEvent.clear()
    else:
        print("Resuming script...")
        pauseEvent.set()

def cancel():
    print("Cancelling script...")
    os._exit(0)


def applicationIsOpen(name, channel):
    window = gw.getWindowsWithTitle(name)[0]
    if window is not None:
        pass
    else:
        raise Exception(f"No window found with title: {name}")
    
    if channel in window.title:
        print(f"Found application: {window.title}")
    else:
        raise Exception(f"Window found but channel '{channel}' incorrect channel selected")
    
    return window

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

        needle = cv2.imread('./images/messagebox.png')
        needle_height, needle_width = needle.shape[:2]

        result = cv2.matchTemplate(img, needle, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(f"Confidence: {max_val}")
        print(f"Location: {max_loc}")

        if max_val >= 0.8:
            center_x = max_loc[0] + needle_width // 2
            center_y = max_loc[1] + needle_height // 2

            abs_x = application.left + center_x
            abs_y = application.top + center_y

            print(f"Absolute position: {abs_x}, {abs_y}")
            return (abs_x, abs_y)
        else:
            print("Message box not found")
            return None

def clickMessageBox(application, message):
    position = findMessageBox(application)
    if position is not None:
        pyautogui.click(position[0], position[1])
        pyautogui.sleep(0.5)
        pyautogui.write(message)
        pyautogui.sleep(0.5)
        pyautogui.press("enter")
        print("Clicked message box")
    else:
        print("Could not click message box because it was not found")

def getCharacterName(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    character = lines[0].strip()
    
    with open(filename, 'w') as f:
        f.writelines(lines[1:])

    print(f"Retrieved character name: {character}")
    return character



def main():
    keyboard.on_press_key("esc", lambda _: togglePause())
    keyboard.add_hotkey("ctrl+q", lambda: cancel())

    try:
        while True:
            pauseEvent.wait()  # Wait until the script is not paused

            discord = applicationIsOpen("discord", "puppets-1")
            character = getCharacterName("characters.txt")

            if character is None:
                break

            clickMessageBox(discord, f"Hello, {character}!")
            time.sleep(3)

        print("Character have been divorced, exiting.")
        return
    
    except Exception as e:
        print(f"Error: {e}")
        return
main()