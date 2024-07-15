import tkinter as tk
from tkinter import ttk

# Création de la fenêtre principale
root = tk.Tk()
root.title("Redimensionnement avec PanedWindow")

# Création du PanedWindow horizontal
paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Création de la première frame (à gauche)
frame1 = ttk.Frame(paned_window, width=200, height=400, relief=tk.SUNKEN)
frame1.pack_propagate(False)
label1 = tk.Label(frame1, text="Frame 1")
label1.pack(fill=tk.BOTH, expand=True)

# Création de la seconde frame (à droite)
frame2 = ttk.Frame(paned_window, width=200, height=400, relief=tk.SUNKEN)
frame2.pack_propagate(False)
label2 = tk.Label(frame2, text="Frame 2")
label2.pack(fill=tk.BOTH, expand=True)

# Ajout des frames au PanedWindow
paned_window.add(frame1, weight=1)
paned_window.add(frame2, weight=1)

# Lancement de la boucle principale
root.mainloop()
