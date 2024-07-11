import tkinter as tk
from tkinter import ttk, OptionMenu, StringVar, Label, Button, Entry, messagebox, Checkbutton, Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.terminalUART import *
from modules.plotManaging import update_plot, clear_data
from modules.fileManaging import open_file, save_to_csv
import numpy as np
import time
import csv
from tkinter import filedialog
from modules.objects import Chronometer, CustomDialog

class controller(tk.Frame):
    def __init__(self, parent, right_frame, uart_terminal):
        super().__init__(parent)

        # Configurer la grille principale pour qu'elle s'étende et redimensionne les widgets
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Ajout du graphique et des contrôles
        self.graph_control = controlGRAPH(self, uart_terminal)
        self.graph_control.grid(row=0, column=0, sticky="nsew")

        # On donne au controller l'accès au pic_control
        self.pic_control = self.graph_control.pic_control

        # Bouton de connexion dans le right_frame
        self.connect_button = tk.Button(uart_terminal, text="Connect", command=lambda:self.on_connect(uart_terminal, self.pic_control))
        self.connect_button.grid(row=3, column=3, sticky="ew")
        self.connect_button.config(width=10)

    def on_connect(self, uart_terminal, pic_control):
        uart_terminal.connect() # On se connecte au port série
        self.connect_button.config(state=tk.DISABLED)
        self.connect_button.config(text="Connected")
        pic_control.update_buttons_state() # Si le terminal est bien connecté, on rend utilisable les boutons de contrôle
        uart_terminal.send_data('?') # On demande l'état actuel du PIC (Le premier char est toujours ignoré, je ne sais pas pourquoi)
        uart_terminal.send_data('?')
        if uart_terminal.check_status!='i': # Si le PIC est actuellement en train d'écrire lors du démarrage de l'appli, on demande son arrêt
            uart_terminal.send_data('s')

    def plot_uart_data(self, data):
        self.graph_control.plot_uart_data(data)



class controlGRAPH(tk.Frame):
    def __init__(self, parent, uart_terminal):
        super().__init__(parent)
        self.uart_terminal = uart_terminal
        self.data = [0]*1024
        self.time = [0]*1024
        self.user_input = 0
        self.factor_k = 1
        self.delay = 10
        self.mode = "-"

        self.create_widgets()
        self.plot_uart_data(uart_terminal.received_data)

    def create_widgets(self):
        # Configurer la grille pour qu'elle s'étende et redimensionne les widgets
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Conteneur pour le graphique
        self.graph_frame = tk.Frame(self, bg="lightblue")
        self.graph_frame.grid(row=0, column=0, sticky="nsew")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)
        self.ax.set_title('Graphic Displayer')  # Titre
        self.ax.set_xlabel('Channel')  # Abscisse
        self.ax.set_ylabel('Iteration')  # Ordonnée
        self.ax.grid(True)  # Affichage d'une grille

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Conteneur pour les widgets de contrôle
        self.control_frame = tk.Frame(self, bg="lightblue")
        self.control_frame.grid(row=1, column=0, sticky="ew")
        self.control_frame.grid_rowconfigure(0, weight=1)
        self.control_frame.grid_rowconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)
        self.control_frame.grid_columnconfigure(3, weight=1)
        self.control_frame.grid_columnconfigure(4, weight=1)

        # Conteneur pour les widgets de choix de la fréquence
        self.frame_freq = tk.Frame(self.control_frame, bd=2, bg="lightblue", relief="ridge")
        self.frame_freq.grid(row=0, column=2, columnspan=2, sticky="w")
        self.frame_freq.grid_rowconfigure(0, weight=1)
        self.frame_freq.grid_columnconfigure(0, weight=1)
        self.frame_freq.grid_columnconfigure(1, weight=1)
        self.frame_freq.grid_columnconfigure(2, weight=1)
        # Label pour le choix de fréquence
        self.labelfreq = Label(self.frame_freq, text="Enter frequency value:", relief="groove",font=("Arial", 10), width=16, anchor='w')
        self.labelfreq.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        # Zone de texte (Entry)
        self.entry = Entry(self.frame_freq, width=20)
        self.entry.grid(row=0, column=1, padx=0, pady=0, sticky="w")
        self.entry.insert(0, "0")
        # Bouton pour récupérer la valeur saisie
        self.button_confirm = Button(self.frame_freq, text="Confirm", command=self.show_entry_value)
        self.button_confirm.grid(row=0, column=2, padx=0, pady=5, sticky="w")

        # Bouton pour charger un fichier CSV
        self.button_load_csv = Button(self.control_frame, text="Load Data from CSV", command=lambda:open_file(self))
        self.button_load_csv.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Bouton de sauvegarde des données en fichier .csv
        self.button_save_data = Button(self.control_frame, text="Save Data to CSV", command=lambda:save_to_csv(self.data))
        self.button_save_data.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Variable pour les checkboxes
        self.fit_erlang = tk.BooleanVar()
        self.fit_gaussian = tk.BooleanVar()
        self.fit_poisson = tk.BooleanVar()
        self.fit_exponential = tk.BooleanVar()

        # Checkboxes pour tracer Erlang, Gaussienne ou/et Poisson
        self.button_exp = Checkbutton(self.control_frame, text="Add Erlang Fit", variable=self.fit_erlang, command=lambda:update_plot(self))
        self.button_exp.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.button_gaussian = Checkbutton(self.control_frame, text="Add Gaussian Fit", variable=self.fit_gaussian, command=lambda:update_plot(self))
        self.button_gaussian.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.button_poisson = Checkbutton(self.control_frame, text="Add Poisson Fit", variable=self.fit_poisson, command=lambda:update_plot(self))
        self.button_poisson.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.button_exponential = Checkbutton(self.control_frame, text="Add Exponential Fit", variable=self.fit_exponential, command=lambda:update_plot(self))
        self.button_exponential.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Disable fit buttons until mode is set
        self.button_exp.config(state=tk.DISABLED)
        self.button_gaussian.config(state=tk.DISABLED)
        self.button_poisson.config(state=tk.DISABLED)
        self.button_exponential.config(state=tk.DISABLED)

        # Bouton de sauvegarde des données de fit function en fichier .csv
        self.button_save_fit = Button(self.control_frame, text="Save Fit to CSV", command=self.choose_fit)
        self.button_save_fit.grid(row=1,column=4,padx=5,pady=5, sticky="w")

        # Données récupérées des fonctions fit
        self.erlang_x = 0
        self.erlang_y = 0
        self.gaussian_x = 0
        self.gaussian_y = 0
        self.poisson_x = 0
        self.poisson_y = 0
        self.exponential_x = 0
        self.exponential_y = 0

        # Bouton pour supprimer toutes les données actuellement chargées
        self.button_clear_data = Button(self.control_frame, text="Clear All Data", command=lambda:clear_data(self))
        self.button_clear_data.grid(row=1, column=5, padx=5, pady=5, sticky="w")

        self.pic_control = controlPIC(self, self.uart_terminal, self)
        self.pic_control.grid(row=2, column=0, padx=5, pady=5)

    def plot_uart_data(self, uart_data):
        print("Plot called")
        self.data = np.add(self.data, uart_data)
        self.reset_tab(uart_data)
        update_plot(self)

    def reset_tab(self, tab):
        for i in range(len(tab)):
            tab[i]=0

    def set_factor_k(self, value):
        self.factor_k = int(value)

    def set_delay(self, value):
        self.delay = int(value)

    def show_entry_value(self):
        if "1" <= self.entry.get() <= "50000":
            self.user_input = self.entry.get()
            messagebox.showinfo("Value selected", f"Frequency value entered: {self.user_input} Hz")
            if self.data is not None:
                update_plot(self)
        else:
            messagebox.showinfo("Configuration error", "Frequency must be set between 1 Hz and 50 000 Hz!")

    def choose_fit(self):
        if not self.fit_erlang.get() and not self.fit_poisson.get() and not self.fit_gaussian.get():
            messagebox.showinfo("Saving Data error", "No fit function are currently plotted!")
        else:
            dialog = CustomDialog(self.control_frame, title="Saving fit data", show_choice1=self.fit_erlang.get(), show_choice2=self.fit_gaussian.get(), show_choice3=self.fit_poisson.get())
            if dialog.choice == "Erlang":
                save_to_csv(self.erlang_y)
            if dialog.choice == "Poisson":
                save_to_csv(self.poisson_y)
            if dialog.choice == "Gaussian":
                save_to_csv(self.gaussian_y)
            if dialog.choice == "Piscine":
                save_to_csv(self.exponential_y)











class controlPIC(tk.Frame):
    def __init__(self, parent, uart_terminal, graph_control):
        super().__init__(parent)
        self.uart_terminal = uart_terminal
        self.graph_control = graph_control

        self.buttons = []
        self.create_widgets()
        self.update_buttons_state()

        # Ajouter des labels au conteneur
        self.label1 = ttk.Label(self, text="Function Mode")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.label2 = ttk.Label(self, text="K factor")
        #self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.label3 = ttk.Label(self, text="Measure Delay")
        #self.label3.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Configurer la grille pour qu'elle s'étende et redimensionne les widgets
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def create_widgets(self):
        # Ajouter des boutons au conteneur
        startMeasures = ttk.Button(self, text="Start", command=self.on_startMeasures_click)
        startMeasures.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.buttons.append(startMeasures)
        
        stopMeasures = ttk.Button(self, text="Stop", command=lambda:self.on_stopMeasures_click(self.uart_terminal))
        #stopMeasures.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.buttons.append(stopMeasures)

        # Selection du Mode de mesure
        self.mode_var = StringVar(self)
        self.mode_var.set("-")
        self.mode_options = ["Erlang", "Poisson", "Piscine"]
        self.mode_menu = OptionMenu(self, self.mode_var, *self.mode_options)
        self.mode_menu.config(width=7)
        self.mode_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.mode_var.trace_add("write", self.on_mode_select)

        # Création du menu déroulant pour le facteur
        self.factor_var = StringVar(self)
        self.factor_var.set("-")
        self.factor_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.factor_menu = OptionMenu(self, self.factor_var, *self.factor_options)
        #self.factor_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.factor_var.trace_add("write", self.on_factor_select)
        #self.factor_menu.config(state=tk.DISABLED)

        # Création du menu déroulant pour le Delay
        self.delay_var = StringVar(self)
        self.delay_var.set("-")
        self.delay_options = ["1", "3", "5", "10", "15", "20"]
        self.delay_menu = OptionMenu(self, self.delay_var, *self.delay_options)
        #self.delay_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.delay_var.trace_add("write", self.on_delay_select)
        #self.delay_menu.config(state=tk.DISABLED)

        # Bouton pour reset le nombre de mesures du mode piscine
        self.reset_pool_button = Button(self, text="Reset Pool Count", command=self.reset_pool_count)

        # Invisible button to keep the Controller size stable upon mode selection
        self.invisible_button = Button(self, borderwidth=1, height=1, width=1)
        #self.invisible_button.grid(row=1, column=1, padx=5, pady=6)

        # Chronometre
        self.frame_chrono = Frame(self, bd=2, relief="groove")
        self.chrono = Chronometer(self.frame_chrono, "Time elapsed :", self.update_pool_data)
        self.frame_chrono.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
  


    # Commande de lancement des mesures
    def on_startMeasures_click(self):
        if self.uart_terminal is not None:  # On vérifie que le terminal existe bien
            mode = self.mode_var.get()
            factor = self.factor_var.get()
            freq = int(self.graph_control.entry.get())

            if mode == "Erlang":  # On vérifie que les paramètres sont biens configurés avant lancement
                if "1" <= factor <= "9":
                    if(1 <= freq <= 50000):
                        self.send_character('g')
                        self.chrono.start()
                        self.buttons[0].grid_forget()
                        self.buttons[1].grid(row=0, column=2, padx=5, pady=5, sticky="ew")
                        self.mode_menu.config(state=tk.DISABLED)
                        self.factor_menu.config(state=tk.DISABLED)
                    else:
                        messagebox.showinfo("Configuration error", "Frequence must be set between 1 Hz and 50 000 Hz!")
                else:
                    messagebox.showinfo("Configuration error", "Factor k must be set!")
            elif mode == "Poisson":
                if(1 <= freq <= 50000):
                    self.send_character('g')
                    self.chrono.start()
                    self.buttons[0].grid_forget()
                    self.buttons[1].grid(row=0, column=2, padx=5, pady=5, sticky="ew")
                    self.mode_menu.config(state=tk.DISABLED)
                else:
                    messagebox.showinfo("Configuration error", "Frequence must be set between 1 Hz and 50 000 Hz!")
            elif mode == "Piscine":
                if("1" <= self.delay_var.get() <= "9"):
                    self.send_character('g')
                    self.chrono.start()
                    self.buttons[0].grid_forget()
                    self.buttons[1].grid(row=0, column=2, padx=5, pady=5, sticky="ew")
                    self.mode_menu.config(state=tk.DISABLED)
                    self.delay_menu.config(state=tk.DISABLED)
                    self.reset_pool_button.config(state=tk.DISABLED)
                else:
                    messagebox.showinfo("Configuration error", "Measure Delay must be set!")
            else:
                messagebox.showinfo("Configuration error", "Mode must be set!")
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not initialized!")
    
    # Commande d'arret des mesures
    def on_stopMeasures_click(self, uart_terminal):
        if self.uart_terminal is not None:
            while uart_terminal.get_status == "w": # On attend la fin de la transmission de données avant l'arrêt
                time.sleep(1)
            self.send_character('s')
            self.chrono.stop()
            self.buttons[1].grid_forget()
            self.buttons[0].grid(row=0, column=2, padx=5, pady=5, sticky="ew")
            self.mode_menu.config(state=tk.NORMAL)
            self.factor_menu.config(state=tk.NORMAL)
            self.delay_menu.config(state=tk.NORMAL)
            self.reset_pool_button.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not initialized!")

    # Commande de selection du facteur k pour le mode de mesure Erlang
    def on_factor_select(self, *args):
        factor = self.factor_var.get()
        if self.uart_terminal is not None:
            self.uart_terminal.send_data('k')
            self.uart_terminal.send_data(factor)
            self.graph_control.set_factor_k(factor)
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not initialized!")

    # Commande de selection du facteur k pour le mode de mesure Erlang
    def on_delay_select(self, *args):
        delay = self.delay_var.get()
        self.graph_control.delay = delay
        if self.uart_terminal is not None:
            self.uart_terminal.send_data('o')
            self.uart_terminal.send_data(delay)
            self.graph_control.set_delay(delay)
            self.chrono.update_time = int(delay)
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not initialized!")

    def on_mode_select(self, *args):
        mode = self.mode_var.get()
        self.graph_control.mode = mode
        if self.uart_terminal and self.uart_terminal.serial_port:
            if mode == "Erlang":
                self.uart_terminal.send_data('e')
                self.factor_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # On active l'accès au facteur k
                self.graph_control.button_exp.config(state=tk.NORMAL)
                self.graph_control.button_gaussian.config(state=tk.DISABLED)
                self.graph_control.button_poisson.config(state=tk.DISABLED)
                self.graph_control.button_exponential.config(state=tk.DISABLED)
                self.reset_pool_button.grid_forget()
                self.delay_menu.grid_forget()
                self.label3.grid_forget()
                self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
                self.chrono.mode = "-"
                self.graph_control.fit_erlang.set(False)
                self.graph_control.fit_gaussian.set(False)
                self.graph_control.fit_poisson.set(False)
                self.graph_control.fit_exponential.set(False)
            elif mode == "Poisson":
                self.uart_terminal.send_data('p')
                self.factor_menu.grid_forget() # On desactive l'accès au facteur k
                self.graph_control.button_gaussian.config(state=tk.NORMAL)
                self.graph_control.button_poisson.config(state=tk.NORMAL)
                self.graph_control.button_exp.config(state=tk.DISABLED)
                self.graph_control.button_exponential.config(state=tk.DISABLED)
                self.delay_menu.grid_forget()
                self.label3.grid_forget()
                self.label2.grid_forget()
                self.reset_pool_button.grid_forget()
                self.chrono.mode = "-"
                self.graph_control.fit_erlang.set(False)
                self.graph_control.fit_gaussian.set(False)
                self.graph_control.fit_poisson.set(False)
                self.graph_control.fit_exponential.set(False)
            elif mode == "Piscine":
                self.uart_terminal.send_data('o')
                self.factor_menu.grid_forget() # On desactive l'accès au facteur k
                self.graph_control.button_gaussian.config(state=tk.DISABLED)
                self.graph_control.button_poisson.config(state=tk.DISABLED)
                self.graph_control.button_exp.config(state=tk.DISABLED)
                self.graph_control.button_exponential.config(state=tk.NORMAL)
                self.label2.grid_forget()
                self.label3.grid(row=1, column=0, padx=5, pady=5, sticky="w")
                self.factor_menu.grid_forget()
                self.reset_pool_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
                self.delay_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
                self.chrono.mode = "Piscine"
                self.graph_control.fit_erlang.set(False)
                self.graph_control.fit_gaussian.set(False)
                self.graph_control.fit_poisson.set(False)
                self.graph_control.fit_exponential.set(False)
                self.reset_pool_count()
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not initialized!")

    def send_character(self, char):
        if self.uart_terminal and self.uart_terminal.serial_port:
            self.uart_terminal.send_data(char)
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not connected!")
    
    def update_pool_data(self):
        self.send_character("u")

    def update_buttons_state(self):
        state = tk.NORMAL if self.uart_terminal and self.uart_terminal.serial_port else tk.DISABLED
        for button in self.buttons:
            button.config(state=state)
        self.mode_menu.config(state=state)

    def reset_pool_count(self):
        self.send_character('r')