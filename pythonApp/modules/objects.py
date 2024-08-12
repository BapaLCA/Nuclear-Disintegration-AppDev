import tkinter as tk
from threading import Thread
import time
from tkinter import simpledialog

class Chronometer:
    def __init__(self, root, text, callback=None):
        self.root = root
        self.text = text
        self.mode = "-"
        self.callback = callback #Call back function
        self.update_time = 10
        
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.last_notified_second = 0  # Time elapsed to check (delay for pool mode)
        
        self.label = tk.Label(root, text=self.text)
        self.label.pack(side=tk.LEFT, padx=1, pady=2)
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 10))
        self.time_label.pack(side=tk.LEFT, padx=1, pady=2)
        
        self.start_button = tk.Button(root, text="Start", command=self.start)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.RIGHT, padx=5)
        
        self.update_clock()
    
    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_clock()
    
    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
    
    def reset(self):
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.last_notified_second = 0  # Reset the time elapsed to check (delay)
        self.time_label.config(text="00:00:00")
    
    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            elapsed_seconds = int(self.elapsed_time)
            hours = elapsed_seconds // 3600
            minutes = (elapsed_seconds % 3600) // 60
            seconds = elapsed_seconds % 60
            self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
            
            # Check if a multiple of the Delay set has elapsed and call the callback function
            if elapsed_seconds % self.update_time == 0 and elapsed_seconds != self.last_notified_second:
                self.last_notified_second = elapsed_seconds
                if self.callback and self.mode == "Activation":
                    self.callback()
                
        self.root.after(50, self.update_clock)  # Update the timer every 50 ms



class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, show_choice1=False, show_choice2=False, show_choice3=False, show_choice4=False):
        self.show_choice1 = show_choice1
        self.show_choice2 = show_choice2
        self.show_choice3 = show_choice3
        self.show_choice4 = show_choice4
        super().__init__(parent, title=title)
    
    def body(self, master):
        tk.Label(master, text="Select which fit function you wish to save:").pack(pady=10)
        
        self.choice = None
        self.button1 = tk.Button(master, text="Erlang", command=lambda: self.set_choice("Erlang"))
        self.button2 = tk.Button(master, text="Gaussian", command=lambda: self.set_choice("Gaussian"))
        self.button3 = tk.Button(master, text="Poisson", command=lambda: self.set_choice("Poisson"))
        self.button4 = tk.Button(master, text="Exponential", command=lambda: self.set_choice("Exponential"))
        # Create buttons for each choice
        if self.show_choice1==True:
            
            self.button1.pack(side=tk.LEFT, padx=5, expand=True)
        
        if self.show_choice2==True:
            
            self.button2.pack(side=tk.LEFT, padx=5, expand=True)
        
        if self.show_choice3==True:
            
            self.button3.pack(side=tk.LEFT, padx=5, expand=True)
        
        if self.show_choice4==True:

            self.button4.pack(side=tk.LEFT, padx=5, pady=5)
        
        return self.button1 if self.show_choice1 else (self.button2 if self.show_choice2 else (self.button3 if self.show_choice3 else self.button4))


    def set_choice(self, choice):
        self.choice = choice
        self.destroy()  # Close the dialog box

    def apply(self):
        self.result = self.choice