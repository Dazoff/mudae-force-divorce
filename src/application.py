import pygetwindow as gw

def applicationIsOpen(name, channel):
    window = gw.getWindowsWithTitle(name)[0]
    if window is not None:
        pass
    else:
        raise Exception(f"No window found with title: {name}")
    
    if channel in window.title:
        pass
    else:
        raise Exception(f"Window found but channel '{channel}' incorrect channel selected")
    
    return window