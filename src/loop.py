import random
import threading
import keyboard
import time

from src.application import applicationIsOpen
from src.character import getCharacterName, removeCharacterName
from src.messageBox import clickMessageBox

cancelEvent = threading.Event()
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
    cancelEvent.set()

def registerHotkeys():
    keyboard.on_press_key("esc", lambda _: togglePause())
    keyboard.add_hotkey("ctrl+q", lambda: cancel())

def runLoop(appName, channel, filename, command, confirmation):
    try:
        while not cancelEvent.is_set():
            pauseEvent.wait()  # Wait until the script is not paused

            discord = applicationIsOpen(appName, channel)

            character = getCharacterName(filename)

            if character is None:
                break

            success = clickMessageBox(discord, f"{command} {character}", confirmation)
            
            print(success)

            if success:
                print(f"Successfully removed character: {character}")
                removeCharacterName(filename, character)

            time.sleep(random.uniform(3.0, 4.0))  # Simulate human-like delay

        print("Script is now done, exiting.")
        return
    
    except Exception as e:
        print(f"Error: {e}")
        return