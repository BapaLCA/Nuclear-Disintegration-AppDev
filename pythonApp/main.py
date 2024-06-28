# main.py
# EXE can be built with the command : pyinstaller --onefile main.py --additional-hooks-dir serial\\__init__.py

# Modules imports
#from modules.fitFunctions import add_erlang_fit, add_poisson_fit, add_gaussian_fit
from modules.controller import *
from modules.terminalUART import *
# General libraries
from collections import defaultdict
import tkinter
from tkinter import *
import sys

# Screen
analysis = tkinter.Tk() # Définition d'un écran
#analysis.geometry("1280x720") # Définition de la taille de l'écran
analysis.attributes('-fullscreen', False)
analysis.title("Desintegrations Nucleaires") # Définition du nom de l'application

# Méthode pour basculer entre plein écran et mode fenêtré
def toggle_fullscreen(event=None):
    fullscreen = analysis.attributes('-fullscreen')
    analysis.attributes('-fullscreen', not fullscreen)

# Méthode pour quitter le mode plein écran
def end_fullscreen(event=None):
    analysis.attributes('-fullscreen', False)

# Lier la touche F11 à la bascule plein écran
analysis.bind('<F11>', toggle_fullscreen)

# Lier la touche Échap pour quitter le plein écran
analysis.bind('<Escape>', end_fullscreen)

# Titre de l'application
title = Label(text="Distribution de Poisson/Erlang", font=("Arial", 16, "bold")) # Définition du titre
title.pack() # Affichage du label


# Définition des variables globales
data = defaultdict(list) # Liste de données pour la lecture du fichier csv
user_input = 0 # Fréquence du signal pour l'adaptation de l'échelle des abscisses
selected_value = tkinter.IntVar()  # Variable k
selected_value.set(1) # Valeur par défaut

# Définir la fonction de fermeture
analysis.protocol("WM_DELETE_WINDOW", lambda: on_closing(analysis, terminal))


############################## Définition des fonction principales ############################## 

def plot_uart_data(uart_data):
    control.plot_uart_data(uart_data)

# Fonction de fermeture du terminal
def on_closing(root, terminal):
    terminal.close()
    root.destroy()
    sys.exit()

############################## Configuration des boutons et menus ##############################
"""
# Créer un frame principal pour le layout
main_frame = tk.Frame(analysis, bg="red")
main_frame.pack(expand=True, fill=tk.BOTH)

# Configurer le layout pour qu'il s'étende correctement
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)

# Créer les quatre frames pour les coins de l'application
top_left_frame = tk.Frame(main_frame, bg="blue")
top_left_frame.grid(row=0, column=0, padx=5, pady=5)

top_right_frame = tk.Frame(main_frame, bg="lightgreen")
top_right_frame.grid(row=0, column=1, padx=5, pady=5)

bottom_left_frame = tk.Frame(main_frame, bg="lightyellow")
bottom_left_frame.grid(row=1, column=0, padx=5, pady=5)

bottom_right_frame = tk.Frame(main_frame, bg="lightcoral")
bottom_right_frame.grid(row=1, column=1, padx=5, pady=5)

# Ajout du terminal UART
terminal = UARTTerminal(top_right_frame, plot_uart_data)
terminal.pack(expand=True, fill=tk.BOTH)

# Ajout du controleur
control = controller(top_left_frame, bottom_right_frame, terminal)
control.pack(expand=True, fill=tk.BOTH)
"""

left_frame = tk.Frame(analysis)
left_frame.pack(expand=True, fill=tk.BOTH, side=LEFT)

right_frame = tk.Frame(analysis)
right_frame.pack(expand=True, fill=tk.BOTH, side=RIGHT)

terminal = UARTTerminal(right_frame, plot_uart_data)
terminal.pack(expand=True, fill=tk.BOTH, side=TOP)

control = controller(left_frame, right_frame, terminal)
control.pack(expand=True, fill=tk.BOTH, side=TOP, padx=5, pady=5)


# Bouton pour quitter l'application
#bclose = Button(left_frame, text="Close Application", command=(on_closing(analysis, terminal))) # Bouton pour fermer l'application
#bclose.pack(expand=True, fill=tk.X, side=BOTTOM, pady=5)


# Loop
analysis.mainloop() # Pour maintenir l'application ouverte
