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