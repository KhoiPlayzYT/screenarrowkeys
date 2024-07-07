import tkinter as tk
import keyboard

class DraggableWindow(tk.Toplevel):
    def __init__(self, parent, direction, x, y):
        super().__init__(parent)
        self.parent = parent
        self.direction = direction
        self.initial_x = x
        self.initial_y = y

        # Configure window
        self.title(f"{direction} Window")
        self.geometry('50x50')

        # Create label with arrow symbol or character
        self.arrow_label = tk.Label(self, text=self.get_arrow_symbol(direction), font=('Arial', 24))
        self.arrow_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Set window always on top
        self.attributes('-topmost', 1)

        # Make window draggable without focus
        self.arrow_label.bind("<ButtonPress-1>", self.on_drag_start)
        self.arrow_label.bind("<B1-Motion>", self.on_drag_motion)

        # Position the window
        self.geometry(f'+{x}+{y}')

        # Make the window non-interactable with keyboard events
        self.overrideredirect(True)

    def get_arrow_symbol(self, direction):
        if 'Up' in direction:
            return '\u2191'  # Unicode for up arrow
        elif 'Down' in direction:
            return '\u2193'  # Unicode for down arrow
        elif 'Left' in direction:
            return '\u2190'  # Unicode for left arrow
        elif 'Right' in direction:
            return '\u2192'  # Unicode for right arrow

    def on_drag_start(self, event):
        # Record the initial position of the mouse cursor
        self.start_x = event.x_root
        self.start_y = event.y_root

        # Record the initial position of the window
        self.start_pos_x = self.winfo_x()
        self.start_pos_y = self.winfo_y()

    def on_drag_motion(self, event):
        # Calculate the movement of the window
        delta_x = event.x_root - self.start_x
        delta_y = event.y_root - self.start_y

        # Update the window position
        new_pos_x = self.start_pos_x + delta_x
        new_pos_y = self.start_pos_y + delta_y
        self.geometry(f'+{new_pos_x}+{new_pos_y}')

    def reset_position(self):
        # Reset window position to initial coordinates
        self.geometry(f'+{self.initial_x}+{self.initial_y}')

class FlashingWindowsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('0x0')  # Make the root window effectively invisible

        # Calculate screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Initial positions
        y_left = screen_height - 90  # 50 (window height) + 40 (move up)
        y_down = screen_height - 90
        y_up = screen_height - 140  # 100 (window height) + 40 (move up)
        y_right = screen_height - 90

        # Create four draggable windows for arrow keys
        self.windows = {
            'Left': DraggableWindow(self.root, 'Left', 0, y_left),
            'Down': DraggableWindow(self.root, 'Down', 50, y_down),
            'Up': DraggableWindow(self.root, 'Up', 50, y_up),
            'Right': DraggableWindow(self.root, 'Right', 100, y_right),
        }

        self.bind_keys()

    def bind_keys(self):
        # Arrow keys
        keyboard.on_press_key('left', lambda e: self.change_background('Left', 'black'))
        keyboard.on_release_key('left', lambda e: self.change_background('Left', 'white'))
        keyboard.on_press_key('down', lambda e: self.change_background('Down', 'black'))
        keyboard.on_release_key('down', lambda e: self.change_background('Down', 'white'))
        keyboard.on_press_key('up', lambda e: self.change_background('Up', 'black'))
        keyboard.on_release_key('up', lambda e: self.change_background('Up', 'white'))
        keyboard.on_press_key('right', lambda e: self.change_background('Right', 'black'))
        keyboard.on_release_key('right', lambda e: self.change_background('Right', 'white'))

        # WASD keys affect arrow keys
        keyboard.on_press_key('w', lambda e: self.change_background('Up', 'black'))
        keyboard.on_release_key('w', lambda e: self.change_background('Up', 'white'))
        keyboard.on_press_key('a', lambda e: self.change_background('Left', 'black'))
        keyboard.on_release_key('a', lambda e: self.change_background('Left', 'white'))
        keyboard.on_press_key('s', lambda e: self.change_background('Down', 'black'))
        keyboard.on_release_key('s', lambda e: self.change_background('Down', 'white'))
        keyboard.on_press_key('d', lambda e: self.change_background('Right', 'black'))
        keyboard.on_release_key('d', lambda e: self.change_background('Right', 'white'))

        # Alt+Ctrl+R to reset positions
        keyboard.add_hotkey('alt+ctrl+r', self.reset_positions)

    def change_background(self, direction, color):
        if direction in self.windows:
            self.windows[direction].configure(bg=color)

    def reset_positions(self):
        # Reset all windows positions to initial coordinates
        for window in self.windows.values():
            window.reset_position()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FlashingWindowsApp()
    app.run()