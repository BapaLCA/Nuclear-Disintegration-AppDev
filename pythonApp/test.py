import tkinter as tk
import time

class Chronometer:
    def __init__(self, root, text, callback=None):
        self.root = root
        self.text = text
        self.callback = callback  # Ajout de la fonction de rappel
        
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.last_notified_second = 0  # Marqueur pour les derniers 10 secondes vérifiés
        
        self.label = tk.Label(root, text=self.text)
        self.label.pack(side=tk.LEFT, padx=1, pady=2)
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 10))
        self.time_label.pack(side=tk.LEFT, padx=1, pady=2)
        
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
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
        self.last_notified_second = 0  # Réinitialiser le marqueur
        self.time_label.config(text="00:00:00")
    
    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            elapsed_seconds = int(self.elapsed_time)
            hours = elapsed_seconds // 3600
            minutes = (elapsed_seconds % 3600) // 60
            seconds = elapsed_seconds % 60
            self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
            
            # Vérifier si un multiple de 10 secondes s'est écoulé et appeler le callback si défini
            if elapsed_seconds % 10 == 0 and elapsed_seconds != self.last_notified_second:
                self.last_notified_second = elapsed_seconds
                if self.callback and self.mode.get() == "Piscine":
                    self.callback()
                
        self.root.after(50, self.update_clock)  # Mettre à jour toutes les 50 ms

# Exemple de classe Controller
class Controller:
    def __init__(self, root):
        self.chronometer = Chronometer(root, "Chrono", self.ten_seconds_elapsed)
        
    def ten_seconds_elapsed(self):
        print("10 secondes se sont écoulées")

if __name__ == "__main__":
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()
