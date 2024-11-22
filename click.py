from pynput import mouse, keyboard
import time
import threading

# Initialize the mouse controller
mouse_controller = mouse.Controller()

# Flag to control clicking
clicking = False

def click_mouse():
    """Function to click mouse repeatedly while the flag is set."""
    while clicking:
        mouse_controller.click(mouse.Button.left)
        #time.sleep(0.1)  # Adjust speed of clicks by changing this value

# Function to handle key presses
def on_press(key):
    global clicking
    try:
        if key.char == 'c' and not clicking:
            clicking = True
            # Start the clicking in a separate thread
            threading.Thread(target=click_mouse).start()
    except AttributeError:
        pass  # Handle special keys that don't have char attributes

# Function to handle key releases
def on_release(key):
    global clicking
    try:
        if key.char == 'c':
            clicking = False
    except AttributeError:
        pass

# Set up listeners
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
