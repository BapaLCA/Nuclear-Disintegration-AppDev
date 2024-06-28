import tkinter as tk
from threading import Thread
import time
from tkinter import simpledialog

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



class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, show_choice1=False, show_choice2=False, show_choice3=False):
        self.show_choice1 = show_choice1
        self.show_choice2 = show_choice2
        self.show_choice3 = show_choice3
        super().__init__(parent, title=title)
    
    def body(self, master):
        tk.Label(master, text="Select which fit function you wish to save:").pack(pady=10)
        
        self.choice = None
        self.button1 = tk.Button(master, text="Erlang", command=lambda: self.set_choice("Erlang"))
        self.button2 = tk.Button(master, text="Gaussian", command=lambda: self.set_choice("Gaussian"))
        self.button3 = tk.Button(master, text="Poisson", command=lambda: self.set_choice("Poisson"))
        # Créez des boutons pour les trois choix
        if self.show_choice1==True:
            
            self.button1.pack(side=tk.LEFT, padx=5, expand=True)
        
        if self.show_choice2==True:
            
            self.button2.pack(side=tk.LEFT, padx=5, expand=True)
        
        if self.show_choice3==True:
            
            self.button3.pack(side=tk.LEFT, padx=5, expand=True)
        
        return self.button1 if self.show_choice1 else (self.button2 if self.show_choice2 else self.button3)


    def set_choice(self, choice):
        self.choice = choice
        self.destroy()  # Ferme la boîte de dialogue

    def apply(self):
        self.result = self.choice