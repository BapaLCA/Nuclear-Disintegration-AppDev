# main.py
# EXE can be built with the command : pyinstaller --onefile main.py --additional-hooks-dir serial\\__init__.py

# Modules imports
from modules.controller import *
from modules.terminalUART import *
# General libraries
from collections import defaultdict
import tkinter
from tkinter import *
import sys

# Screen
analysis = tkinter.Tk() # Define screen
analysis.attributes('-fullscreen', False)
analysis.title("Nuclear Disintegration Controller") # Define application name

# Function to switch between fullscreen and windowed
def toggle_fullscreen(event=None):
    fullscreen = analysis.attributes('-fullscreen')
    analysis.attributes('-fullscreen', not fullscreen)

# Function to quit fullscreen
def end_fullscreen(event=None):
    analysis.attributes('-fullscreen', False)

# Bind F11 key to fullscreen
analysis.bind('<F11>', toggle_fullscreen)

# Bind ESC to quit fullscreen
analysis.bind('<Escape>', end_fullscreen)

# Application Title
title = Label(text="Nuclear Disintegration Analyzer & Controller", font=("Arial", 16, "bold"))
title.pack()

# Define the function to close application
analysis.protocol("WM_DELETE_WINDOW", lambda: on_closing(analysis, terminal))


############################## Main functions ############################## 

def plot_uart_data(uart_data): # Callback from UART terminal to controller
    control.plot_uart_data(uart_data)

# Function to close terminal
def on_closing(root, terminal):
    answer = messagebox.askyesno("Close Application ?", "Do you wish to close the application ? All unsaved data will be lost!")
    if answer:
        terminal.close()
        root.destroy()
        sys.exit()

############################## Frames Configuration ##############################

# Creates the horizontal PanedWindow
paned_window = tk.PanedWindow(analysis, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=10)
paned_window.pack(fill=tk.BOTH, expand=True)

# Sets up a left frame to put the Controller instance
left_frame = tk.Frame(paned_window, width=800, height=900)
left_frame.pack_propagate(False)

# Sets up a right frame to put the UART Terminal instance
right_frame = tk.Frame(paned_window, width=800, height=900)
right_frame.pack_propagate(False)

# Binds frames to the PanedWindow
paned_window.add(left_frame)
paned_window.add(right_frame)

# Creates an instance of UART Terminal
terminal = UARTTerminal(right_frame, plot_uart_data)
terminal.pack(expand=True, fill=tk.BOTH, side=TOP)

# Creates an instance of Controller
control = controller(left_frame, right_frame, terminal)
control.pack(expand=True, fill=tk.BOTH, side=TOP, padx=5, pady=5)

# Button to close application
bclose = Button(control, text="Close Application", command=lambda:(on_closing(analysis, terminal)))
bclose.grid(row=1, column=0, sticky="nsew")



# Loop
analysis.mainloop() # To maintain the application open
