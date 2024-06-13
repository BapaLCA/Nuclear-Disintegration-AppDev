import tkinter as tk
from tkinter import ttk
from tkinter import OptionMenu, StringVar, Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.terminalUART import *

def createGraph(x_coord, y_coord, canvas, root):
# Crée une figure matplotlib vide
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_title('Graphic Displayer')  # Titre
    ax.set_xlabel('Time (in µs)')  # Abscisse
    ax.set_ylabel('Iteration')  # Ordonnée
    ax.grid(True)  # Affichage d'une grille

    # Intègre la figure matplotlib dans Tkinter
    figure_canvas = FigureCanvasTkAgg(fig, master=root)
    figure_canvas.draw()
    figure_widget = figure_canvas.get_tk_widget()

    # Place la figure aux coordonnées données
    canvas.create_window(x_coord, y_coord, window=figure_widget, anchor=tk.NW)

    return fig, ax



class controlPIC(tk.Frame):
    def __init__(self, parent, uart_terminal):
        super().__init__(parent)
        self.uart_terminal = uart_terminal

        self.buttons = []
        self.create_widgets()
        self.update_buttons_state()

        # Ajouter des labels au conteneur
        self.label1 = ttk.Label(self, text="Label 1")
        self.label1.grid(row=0, column=0, padx=5, pady=5)
        
        self.label2 = ttk.Label(self, text="Label 2")
        self.label2.grid(row=0, column=1, padx=5, pady=5)
        
        


    def create_widgets(self):
        # Ajouter des boutons au conteneur
        startMeasures = ttk.Button(self, text="Start", command=self.on_startMeasures_click)
        startMeasures.grid(row=1, column=0, padx=5, pady=5)
        self.buttons.append(startMeasures)
        
        stopMeasures = ttk.Button(self, text="Stop", command=self.on_stopMeasures_click)
        stopMeasures.grid(row=1, column=1, padx=5, pady=5)
        self.buttons.append(stopMeasures)

        # Selection du Mode de mesure
        self.mode_var = StringVar(self)
        self.mode_var.set("Erlang")
        self.mode_options = ["Erlang", "Poisson"]
        self.mode_menu = OptionMenu(self, self.mode_var, *self.mode_options)
        self.mode_menu.grid(row=0, column=2, padx=5, pady=5)
        self.mode_var.trace_add("write", self.on_mode_select)

        # Création du menu déroulant pour le facteur
        self.factor_var = StringVar(self)
        self.factor_var.set("1")
        self.factor_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.factor_menu = OptionMenu(self, self.factor_var, *self.factor_options)
        self.factor_menu.grid(row=1, column=2, padx=5, pady=5)
        self.factor_var.trace_add("write", self.on_factor_select)    


    # Commande de lancement des mesures
    def on_startMeasures_click(self):
        if self.uart_terminal is not None:
            self.send_character('g')
        else:
            print("UART Terminal is not initialized!")
    
    # Commande d'arret des mesures
    def on_stopMeasures_click(self):
        if self.uart_terminal is not None:
            self.send_character('s')
        else:
            print("UART Terminal is not initialized!")

    # Commande de selection du facteur k pour le mode de mesure Erlang
    def on_factor_select(self, *args):
        factor = self.factor_var.get()
        if self.uart_terminal is not None:
            self.uart_terminal.send_data('k')
            self.uart_terminal.send_data(factor)
        else:
            print("UART Terminal is not initialized!")

    def on_mode_select(self, *args):
        mode = self.mode_var.get()
        if self.uart_terminal and self.uart_terminal.serial_port:
            if mode == "Erlang":
                self.uart_terminal.send_data('e')
            elif mode == "Poisson":
                self.uart_terminal.send_data('p')
        else:
            print("UART Terminal is not initialized!")

    def send_character(self, char):
        if self.uart_terminal and self.uart_terminal.serial_port:
            self.uart_terminal.send_data(char)
        else:
            print("UART terminal is not connected.")

    def update_buttons_state(self):
        state = tk.NORMAL if self.uart_terminal and self.uart_terminal.serial_port else tk.DISABLED
        for button in self.buttons:
            button.config(state=state)
        self.factor_menu.config(state=state)
        self.mode_menu.config(state=state)