import keyboard
import threading

from src.loop import registerHotkeys, runLoop
from src.userConfig import getConfig, printConfig

def main():
    registerHotkeys()
    appName, channel, filename, command, confirmation = getConfig()
    printConfig(appName, channel, filename, command, confirmation)

    thread = threading.Thread(target=runLoop, args=(appName, channel, filename, command, confirmation))
    thread.daemon = True
    thread.start()

    keyboard.wait()

main()