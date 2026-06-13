import os
import pyautogui
import mss
import cv2
import time
import pygetwindow as gw
import numpy as np
import keyboard
import threading

import pyperclip

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


def writeMessageBox(message, confirmation):
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.sleep(0.5)
        pyautogui.press("enter")

        pyperclip.copy("")  # Clear clipboard after pasting

        if confirmation == "y":
            time.sleep(3)
            pyautogui.press("y")
            pyautogui.sleep(0.5)
            pyautogui.press("enter")

def clickMessageBox(application, message, confirmation):
    position = findMessageBox(application)

    if position is not None:
        pyautogui.click(position[0], position[1])
        pyautogui.sleep(0.5)
        print("Clicked message box")
        writeMessageBox(message, confirmation)
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

def registerHotkeys():
    keyboard.on_press_key("esc", lambda _: togglePause())
    keyboard.add_hotkey("ctrl+q", lambda: cancel())

def getConfig():
    appName = input("Enter the application name (default: Discord): ").strip() or "Discord"
    channel = input("Channel name: ").strip()
    filename = input("Name of the file containing character names (default: characters.txt): ").strip() or "characters.txt"
    command = input("Desired command to send to the message box (default: $forcedivorce): ").strip() or "$forcedivorce"
    confirmation = input("Will this command require a confirmation (e.g typing y/n or character name afterwards)?").strip().lower()

    return appName, channel, filename, command, confirmation

def printConfig(appName, channel, filename, command, confirmation):
    print("\nStarting with the following configuration:")
    print(f"Application Name: {appName}")
    print(f"Channel Name: {channel}")
    print(f"Character File: {filename}")
    print(f"Command: {command}")
    print(f"Confirmation Required: {confirmation}")
    print("Press ESC to pause/resume, CTRL+Q to quit.")

def runLoop(appName, channel, filename, command, confirmation):
    try:
        while True:
            pauseEvent.wait()  # Wait until the script is not paused

            discord = applicationIsOpen(appName, channel)

            character = getCharacterName(filename)

            if character is None:
                break

            clickMessageBox(discord, f"{command} {character}", confirmation)
            time.sleep(3)

        print("Character have been divorced, exiting.")
        os._exit(0)
    
    except Exception as e:
        print(f"Error: {e}")
        os._exit(1)

def main():
    registerHotkeys()
    appName, channel, filename, command, confirmation = getConfig()
    printConfig(appName, channel, filename, command, confirmation)

    thread = threading.Thread(target=runLoop, args=(appName, channel, filename, command, confirmation))
    thread.daemon = True
    thread.start()

    keyboard.wait()

main()