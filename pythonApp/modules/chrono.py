import tkinter as tk
from threading import Thread
import time

class Chronometer:
    def __init__(self, root, text):
        self.root = root
        self.text = text
        
        self.running = False
        self.time_elapsed = 0
        
        self.label = tk.Label(root, text=self.text)
        self.label.pack(side=tk.LEFT, padx=1, pady=2)
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 10))
        self.label.pack(side=tk.LEFT, padx=1, pady=2)
        
        self.start_button = tk.Button(root, text="Start", command=self.start)
        #self.start_button.pack(side="left", padx=20)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        #self.stop_button.pack(side="left", padx=20)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        #self.reset_button.pack(side="left", padx=20)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.run)
            self.thread.start()

    def stop(self):
        self.running = False

    def reset(self):
        self.stop()
        self.time_elapsed = 0
        self.update_label()

    def run(self):
        while self.running:
            time.sleep(1)
            self.time_elapsed += 1
            self.update_label()

    def update_label(self):
        # This method should only be called from the main thread
        self.root.after(0, self.update_time)

    def update_time(self):
        minutes, seconds = divmod(self.time_elapsed, 60)
        hours, minutes = divmod(minutes, 60)
        self.label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")