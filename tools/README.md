# Tools

Information regarding what each library is used for in this script.

## Requirements.in

File contains libraries needed to run the code.

### pyautogui

Used in [messageBox.py](../src/messageBox.py)

Pyautogui is primarily used for controlling the mouse and keyboard, in this case to click on the chat input box, paste the copies message, and press enter to send it.

### mss

Used in [messageBox.py](../src/messageBox.py)

mss allows screen grab of multiple monitors, which is needed when searching for the application and detecting chat input box.

### opencv-python

Used in [messageBox.py](../src/messageBox.py) (imported as cv2)

opencv-python loads the given image, slides it over the screenshot of the application and calculates how well it matches at every position before giving the best matching position.

### Pillow

Not directly used in code.

Dependency of pyautogui/pyscreeze for screenshots. (Supposed to come with the libraries, but had to download manually)

### Keyboard

Used in [forcedivorce.py](../forcedivorce.py) and [loop.py](../src/loop.py)

Keyboard allows the user to pause or cancel the program when pressing a key (Esc for pausing) or hotkey (Ctrl + q for quitting)

## Requirements-dev.in

File contains libraries needed to run compile the code into an exe.

### Pip-tools

Pip-tools allows separation of dev libraries and production libraries, instead of having everything in one requirements file.

#### Auto-py-to-ex

Graphical interface for pyinstaller, to convert python files to executables (exe).
