import tkinter as tk
from tkinter import ttk, OptionMenu, StringVar, Label, Button, Entry, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.terminalUART import *
from modules.fitFunctions import add_erlang_fit, add_poisson_fit, add_gaussian_fit
from modules.fileManaging import open_file, plot_data
import numpy as np
import time

def createGraph(x_coord, y_coord, canvas, root):
# Crée une figure matplotlib vide
    fig, ax = plt.subplots(figsize=(6, 4))
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

class controller(tk.Frame):
    def __init__(self, parent, bottom_right_frame, uart_terminal):
        super().__init__(parent)

        # Ajout du graphique et des contrôles
        self.graph_control = controlGRAPH(self, uart_terminal)
        self.graph_control.pack(expand=True, fill=tk.BOTH)

        # Ajout du conteneur de contrôle du PIC
        pic_control = controlPIC(self, uart_terminal)
        pic_control.pack(expand=True, fill=tk.BOTH)

        # Bouton de connexion
        connect_button = Button(bottom_right_frame, text="Connecter", command=lambda:self.on_connect(uart_terminal, pic_control))
        connect_button.pack(expand=True, fill=tk.BOTH)

        #self.uart_terminal.data_callback = self.on_data_received
        #self.plot_uart_data(uart_terminal.received_data)

    def on_connect(self, uart_terminal, pic_control):
        uart_terminal.connect() # On se connecte au port série
        pic_control.update_buttons_state() # Si le terminal est bien connecté, on rend utilisable les boutons de contrôle
        uart_terminal.send_data('?') # On demande l'état actuel du PIC (Le premier char est toujours ignoré, je ne sais pas pourquoi)
        uart_terminal.send_data('?')

    def plot_uart_data(self, data):
        self.graph_control.plot_uart_data(data)



class controlGRAPH(tk.Frame):
    def __init__(self, parent, uart_terminal):
        super().__init__(parent)
        self.data = [0]*1024
        self.user_input = 0

        self.create_widgets()
        self.plot_uart_data(uart_terminal.received_data)

    def create_widgets(self):
        # Conteneur pour le graphique
        self.graph_frame = tk.Frame(self)
        self.graph_frame.grid(row=0, column=0, sticky="nsew")

        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.ax.set_title('Graphic Displayer')  # Titre
        self.ax.set_xlabel('Time (in µs)')  # Abscisse
        self.ax.set_ylabel('Iteration')  # Ordonnée
        self.ax.grid(True)  # Affichage d'une grille

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # Frame pour les widgets de contrôle
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Bouton pour charger un fichier CSV
        self.b1 = Button(self.control_frame, text="Load CSV", command=self.load_file)
        self.b1.grid(row=0, column=0, padx=5, pady=5)

        # Label pour le choix de fréquence
        self.labelfreq = Label(self.control_frame, text="Enter frequency value:")
        self.labelfreq.grid(row=0, column=1, padx=5, pady=5)

        # Zone de texte (Entry)
        self.entry = Entry(self.control_frame, width=20)
        self.entry.grid(row=0, column=2, padx=5, pady=5)
        self.entry.insert(0, "0")

        # Bouton pour récupérer la valeur saisie
        self.button_confirm = Button(self.control_frame, text="Confirm", command=self.show_entry_value)
        self.button_confirm.grid(row=0, column=3, padx=5, pady=5)

        # Bouton pour tracer l'Exponentielle
        self.button_exp = Button(self.control_frame, text="Add Erlang Fit", command=lambda: add_erlang_fit(self.data, self.canvas, self.ax, self.user_input))
        self.button_exp.grid(row=1, column=0, padx=5, pady=5)

        # Bouton pour tracer la Gaussienne
        self.button_gaussian = Button(self.control_frame, text="Add Gaussian Fit", command=lambda: add_gaussian_fit(self.data, self.canvas, self.ax, self.user_input))
        self.button_gaussian.grid(row=1, column=1, padx=5, pady=5)

        # Bouton pour tracer Poisson
        self.button_poisson = Button(self.control_frame, text="Add Poisson Fit", command=lambda: add_poisson_fit(self.data, self.canvas, self.ax, self.user_input))
        self.button_poisson.grid(row=1, column=2, padx=5, pady=5)

    def load_file(self):
        self.data = open_file(self.canvas, self.ax, self.user_input)
        if self.data is not None:
            print("Data loaded successfully")
        else:
            print("No data loaded")

    def plot_uart_data(self, uart_data):
        print("Plot called")
        self.data = np.add(self.data, uart_data)
        if self.data is not None:
            #plot_data(self.data, self.canvas, self.ax, self.user_input)
            self.ax.clear()
            self.ax.plot(self.data)
            self.canvas.draw()
        else:
            print("Data is null")

    def show_entry_value(self):
        self.user_input = self.entry.get()
        print(f"Frequency value entered: {self.user_input}")









class controlPIC(tk.Frame):
    def __init__(self, parent, uart_terminal):
        super().__init__(parent)
        self.uart_terminal = uart_terminal

        self.buttons = []
        self.create_widgets()
        self.update_buttons_state()

        # Ajouter des labels au conteneur
        self.label1 = ttk.Label(self, text="Function Mode")
        self.label1.grid(row=0, column=0, padx=5, pady=5)
        
        self.label2 = ttk.Label(self, text="K factor")
        self.label2.grid(row=1, column=0, padx=5, pady=5)

    def create_widgets(self):
        # Ajouter des boutons au conteneur
        startMeasures = ttk.Button(self, text="Start", command=self.on_startMeasures_click)
        startMeasures.grid(row=0, column=2, padx=5, pady=5)
        self.buttons.append(startMeasures)
        
        stopMeasures = ttk.Button(self, text="Stop", command=lambda:self.on_stopMeasures_click(self.uart_terminal))
        stopMeasures.grid(row=1, column=2, padx=5, pady=5)
        self.buttons.append(stopMeasures)

        # Selection du Mode de mesure
        self.mode_var = StringVar(self)
        self.mode_var.set("-")
        self.mode_options = ["Erlang", "Poisson"]
        self.mode_menu = OptionMenu(self, self.mode_var, *self.mode_options)
        self.mode_menu.grid(row=0, column=1, padx=5, pady=5)
        self.mode_var.trace_add("write", self.on_mode_select)

        # Création du menu déroulant pour le facteur
        self.factor_var = StringVar(self)
        self.factor_var.set("-")
        self.factor_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.factor_menu = OptionMenu(self, self.factor_var, *self.factor_options)
        self.factor_menu.grid(row=1, column=1, padx=5, pady=5)
        self.factor_var.trace_add("write", self.on_factor_select)    


    # Commande de lancement des mesures
    def on_startMeasures_click(self):
        if self.uart_terminal is not None:  # On vérifie que le terminal existe bien
            mode = self.mode_var.get()
            factor = self.factor_var.get()

            if mode == "Erlang":  # On vérifie que les paramètres sont biens configurés avant lancement
                if "1" <= factor <= "9":
                    self.send_character('g')
                else:
                    messagebox.showinfo("Factor k must be set!")
            elif mode == "Poisson":
                self.send_character('g')
            else:
                messagebox.showinfo("Mode must be set!")
        else:
            messagebox.showinfo("UART Terminal is not initialized!")
    
    # Commande d'arret des mesures
    def on_stopMeasures_click(self, uart_terminal):
        if self.uart_terminal is not None:
            while uart_terminal.get_status == "w": # On attend la fin de la transmission de données avant l'arrêt
                time.sleep(1)
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