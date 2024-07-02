import tkinter as tk
from tkinter import ttk, OptionMenu, StringVar, Label, Button, Entry, messagebox, Checkbutton, Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.terminalUART import *
from modules.fitFunctions import add_erlang_fit, add_poisson_fit, add_gaussian_fit
import numpy as np
import time
import csv
from tkinter import filedialog
from modules.objects import Chronometer, CustomDialog

class controller(tk.Frame):
    def __init__(self, parent, right_frame, uart_terminal):
        super().__init__(parent)

        # Ajout du graphique et des contrôles
        self.graph_control = controlGRAPH(self, uart_terminal)
        self.graph_control.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        self.pic_control = self.graph_control.pic_control

        # Ajout du conteneur de contrôle du PIC
        #self.pic_control = controlPIC(self, uart_terminal, self.graph_control)
        #self.pic_control.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        # Bouton de connexion
        connect_button = Button(right_frame, text="Connect", command=lambda:self.on_connect(uart_terminal, self.pic_control))
        connect_button.pack(expand=True, fill=tk.X, side=tk.BOTTOM)

    def on_connect(self, uart_terminal, pic_control):
        uart_terminal.connect() # On se connecte au port série
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
        self.graph_frame = tk.Frame(self, bg="blue")
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

        # Frame pour les widgets de contrôle
        self.control_frame = tk.Frame(self, bg="lightblue")
        self.control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.control_frame.grid_columnconfigure(0, weight=1)

        # Bouton pour charger un fichier CSV
        self.button_load_csv = Button(self.control_frame, text="Load Data from CSV", command=self.open_file)
        self.button_load_csv.grid(row=0, column=0, padx=5, pady=5)

        # Label pour le choix de fréquence
        self.labelfreq = Label(self.control_frame, text="Enter frequency value:")
        self.labelfreq.grid(row=0, column=2, padx=5, pady=5)

        # Zone de texte (Entry)
        self.entry = Entry(self.control_frame, width=20)
        self.entry.grid(row=0, column=3, padx=5, pady=5)
        self.entry.insert(0, "0")

        # Bouton pour récupérer la valeur saisie
        self.button_confirm = Button(self.control_frame, text="Confirm", command=self.show_entry_value)
        self.button_confirm.grid(row=0, column=4, padx=5, pady=5)

        # Variable pour les checkboxes
        self.fit_erlang = tk.BooleanVar()
        self.fit_gaussian = tk.BooleanVar()
        self.fit_poisson = tk.BooleanVar()

        # Checkboxes pour tracer Erlang, Gaussienne ou/et Poisson
        self.button_exp = Checkbutton(self.control_frame, text="Add Erlang Fit", variable=self.fit_erlang, command=self.update_plot)
        self.button_exp.grid(row=1, column=0, padx=5, pady=5)
        self.button_gaussian = Checkbutton(self.control_frame, text="Add Gaussian Fit", variable=self.fit_gaussian, command=self.update_plot)
        self.button_gaussian.grid(row=1, column=1, padx=5, pady=5)
        self.button_poisson = Checkbutton(self.control_frame, text="Add Poisson Fit", variable=self.fit_poisson, command=self.update_plot)
        self.button_poisson.grid(row=1, column=2, padx=5, pady=5)

        # Disable fit buttons until mode is set
        self.button_exp.config(state=tk.DISABLED)
        self.button_gaussian.config(state=tk.DISABLED)
        self.button_poisson.config(state=tk.DISABLED)

        # Bouton de sauvegarde des données en fichier .csv
        self.button_save_data = Button(self.control_frame, text="Save Data to CSV", command=lambda:self.save_to_csv(self.data))
        self.button_save_data.grid(row=0, column=1, padx=5, pady=5)

        # Bouton de sauvegarde des données de fit function en fichier .csv
        self.button_save_fit = Button(self.control_frame, text="Save Fit to CSV", command=self.choose_fit)
        self.button_save_fit.grid(row=1,column=3,padx=5,pady=5)

        # Données récupérées des fonctions fit
        self.erlang_x = 0
        self.erlang_y = 0
        self.gaussian_x = 0
        self.gaussian_y = 0
        self.poisson_x = 0
        self.poisson_y = 0

        # Bouton pour supprimer toutes les données actuellement chargées
        self.button_clear_data = Button(self.control_frame, text="Clear All Data", command=self.clear_data)
        self.button_clear_data.grid(row=1, column=4, padx=5, pady=5)

        self.pic_control = controlPIC(self, self.uart_terminal, self)
        self.pic_control.grid(row=2, column=0, padx=5, pady=5)

    def plot_uart_data(self, uart_data):
        print("Plot called")
        self.data = np.add(self.data, uart_data)
        uart_data = [0] * len(uart_data)
        self.update_plot()

    def set_factor_k(self, value):
        self.factor_k = int(value)

    def update_plot(self):
        if self.data is not None:
            print("Update plot called")
            print(self.mode)
            if self.mode == "Erlang":
                print("Erlang mode detected")
                # Rescaling
                if self.entry.get() != '0':
                    period = 1/int(self.entry.get())*1000000
                    self.time = np.arange(0, len(self.data) * period, period)
                else:
                    self.time=self.data
                # Filtrer les indices des valeurs non nulles dans self.data
                non_zero_indices = [i for i, value in enumerate(self.data) if value != 0]
                
                if non_zero_indices:
                    # Ajuster les limites de l'axe x pour zoomer sur les valeurs non nulles
                    min_index = min(non_zero_indices)
                    max_index = max(non_zero_indices)
                    
                    self.ax.clear()
                    self.ax.plot(self.time, self.data, label='Measured Data')
                    self.ax.set_title(f"Time elapsed between {self.factor_k+1} atom disintegrations")  # Titre
                    self.ax.set_xlabel('Time (microseconds)')  # Abscisse
                    self.ax.set_ylabel('Iterance')  # Ordonnée
                    self.ax.grid(True)  # Affichage d'une grille
                    
                    if self.fit_erlang.get():
                        self.add_erlang_fit(self.ax, self.data, self.time, self.factor_k, period)
                    if self.fit_gaussian.get():
                        print("No Gaussian fit on Erlang mode")
                    if self.fit_poisson.get():
                        print("No Poisson fit on Erlang mode")
                    
                    self.ax.set_xlim(self.time[min_index], self.time[max_index])
                    self.ax.legend()
                    self.canvas.draw()
                else:
                    print("All data values are zero")
            else:
                print("Default mode detected")
                # Filtrer les indices des valeurs non nulles
                non_zero_indices = [i for i, value in enumerate(self.data) if value != 0]
                
                if non_zero_indices:
                    # Ajuster les limites de l'axe x pour zoomer sur les valeurs non nulles
                    min_index = min(non_zero_indices)
                    max_index = max(non_zero_indices)
                    
                    self.ax.clear()
                    self.ax.plot(self.data, label='Measured Data')
                    self.ax.set_title(f"Number of atom disintegrations measured in {1/int(self.entry.get())*1000} ms")  # Titre
                    self.ax.set_xlabel('Number of atom disintegrations')  # Abscisse
                    self.ax.set_ylabel('Iteration')  # Ordonnée
                    self.ax.grid(True)  # Affichage d'une grille
                    if self.mode == "Poisson":
                        print("Poisson mode detected")
                        if self.fit_erlang.get():
                            print("No Erlang fit when Poisson mode")
                        if self.fit_gaussian.get():
                            self.add_gaussian_fit(self.ax, self.data)
                        if self.fit_poisson.get():
                            self.add_poisson_fit(self.ax, self.data)
                    
                    self.ax.set_xlim(min_index, max_index)
                    self.ax.legend()
                    self.canvas.draw()
        else:
            print("Data is null")

    def show_entry_value(self):
        self.user_input = self.entry.get()
        messagebox.showinfo("Value selected", f"Frequency value entered: {self.user_input} Hz")
        if self.data is not None:
            self.update_plot()

    def add_erlang_fit(self, ax, data, time, k_value, period):
        self.erlang_x, self.erlang_y = add_erlang_fit(ax, data, time, k_value, period)

    def add_gaussian_fit(self, ax, data):
        self.gaussian_x, self.gaussian_y = add_gaussian_fit(ax, data)

    def add_poisson_fit(self, ax, data):
        self.poisson_x, self.poisson_y = add_poisson_fit(ax, data)

    def open_file(self):
        if 1 <= int(self.entry.get()) <= 50000:

            answer = messagebox.askyesno("Load new data ?", "Loading a file will erase all existing data currently measured. Do you wish to continue ?")
            if answer:
                filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Ouverture d'un explorateur de fichier pour sélectionner un fichier csv à lire
                if not filepath:
                    return  # Termine la fonction ici si aucun fichier n'est sélectionné
                self.data = [0] * len(self.data)  # Efface les anciennes données
                with open(filepath, 'r') as csvfile:  # Ouverture du fichier spécifié en tant que csv
                    csvreader = csv.reader(csvfile, delimiter=';')  # Définition du séparateur de données
                    for row in csvreader:  # Lecture des données
                        try:
                            key = int(row[0])  # Lecture des canaux
                            value = float(row[1])  # Lecture des valeurs relevées
                            if key > 1024:
                                print(f"Line {row} greater than limit has been ignored.")
                                continue  # Ignore la ligne si la valeur dépasse 1024
                            self.data[key] = self.data[key]+value  # Affectation des données dans le tableau data
                        except (ValueError, IndexError) as e:
                            # Log the error and continue
                            print(f"Error processing line : {row}. IndexError: {e}")
                            continue
                uart_data = [0]*1024 # Création d'un tableau de données uart vide pour appeler la fonction plot uart
                self.plot_uart_data(uart_data) # On met à jour l'affichage des données
        else:
            messagebox.showinfo("Configuration Error", "Frequency must be set between 1 and 50 000 Hz to display!")

    def save_to_csv(self, data):
        # Ouvrir une boîte de dialogue pour choisir l'emplacement de sauvegarde
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                # Écrire les données avec le format "numéro de cellule;valeur"
                for i, value in enumerate(data):
                    writer.writerow([i, value])
            messagebox.showinfo("Success", f"Data has been saved to {file_path}")

    def clear_data(self):
        answer = messagebox.askyesno("Clear All Data ?", "Do you really wish to remove all measured data ? Action can not be reverted.")
        if answer:
            self.data = [0] * len(self.data)
            #self.fit_erlang = False # Disable all fit functions
            #self.fit_poisson = False
            #self.fit_gaussian = False
            self.ax.clear()
            self.ax.plot(self.data, label='Measured Data')
            self.ax.set_title('Graphic Displayer')  # Titre
            self.ax.set_xlabel('Channel')  # Abscisse
            self.ax.set_ylabel('Iteration')  # Ordonnée
            self.ax.grid(True)  # Affichage d'une grille
            self.canvas.draw()

    def choose_fit(self):
        if not self.fit_erlang.get() and not self.fit_poisson.get() and not self.fit_gaussian.get():
            messagebox.showinfo("Saving Data error", "No fit function are currently plotted!")
        else:
            dialog = CustomDialog(self.control_frame, title="Saving fit data", show_choice1=self.fit_erlang.get(), show_choice2=self.fit_gaussian.get(), show_choice3=self.fit_poisson.get())
            if dialog.choice == "Erlang":
                self.save_to_csv(self.erlang_y)
            if dialog.choice == "Poisson":
                self.save_to_csv(self.poisson_y)
            if dialog.choice == "Gaussian":
                self.save_to_csv(self.gaussian_y)











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
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")

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
        stopMeasures.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.buttons.append(stopMeasures)

        # Selection du Mode de mesure
        self.mode_var = StringVar(self)
        self.mode_var.set("-")
        self.mode_options = ["Erlang", "Poisson"]
        self.mode_menu = OptionMenu(self, self.mode_var, *self.mode_options)
        self.mode_menu.config(width=7)
        self.mode_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.mode_var.trace_add("write", self.on_mode_select)

        # Création du menu déroulant pour le facteur
        self.factor_var = StringVar(self)
        self.factor_var.set("-")
        self.factor_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.factor_menu = OptionMenu(self, self.factor_var, *self.factor_options)
        self.factor_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.factor_var.trace_add("write", self.on_factor_select)
        self.factor_menu.config(state=tk.DISABLED)

        # Chronometre
        self.frame_chrono = Frame(self, bd=2, relief="groove")
        self.chrono = Chronometer(self.frame_chrono, "Time elapsed :")
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
                        self.buttons[1].grid(row=0, column=2, padx=5, pady=5)
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
                    self.buttons[1].grid(row=0, column=2, padx=5, pady=5)
                    self.mode_menu.config(state=tk.DISABLED)
                else:
                    messagebox.showinfo("Configuration error", "Frequence must be set between 1 Hz and 50 000 Hz!")
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
            self.buttons[0].grid(row=0, column=2, padx=5, pady=5)
            self.mode_menu.config(state=tk.NORMAL)
            self.factor_menu.config(state=tk.NORMAL)
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

    def on_mode_select(self, *args):
        mode = self.mode_var.get()
        self.graph_control.mode = mode
        if self.uart_terminal and self.uart_terminal.serial_port:
            if mode == "Erlang":
                self.uart_terminal.send_data('e')
                self.factor_menu.config(state=tk.NORMAL) # On active l'accès au facteur k
                self.graph_control.button_exp.config(state=tk.NORMAL)
                self.graph_control.button_gaussian.config(state=tk.DISABLED)
                self.graph_control.button_poisson.config(state=tk.DISABLED)
            elif mode == "Poisson":
                self.uart_terminal.send_data('p')
                self.factor_menu.config(state=tk.DISABLED) # On desactive l'accès au facteur k
                self.graph_control.button_gaussian.config(state=tk.NORMAL)
                self.graph_control.button_poisson.config(state=tk.NORMAL)
                self.graph_control.button_exp.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not initialized!")

    def send_character(self, char):
        if self.uart_terminal and self.uart_terminal.serial_port:
            self.uart_terminal.send_data(char)
        else:
            messagebox.showinfo("Terminal error", "UART Terminal is not connected!")

    def update_buttons_state(self):
        state = tk.NORMAL if self.uart_terminal and self.uart_terminal.serial_port else tk.DISABLED
        for button in self.buttons:
            button.config(state=state)
        self.factor_menu.config(state=state)
        self.factor_menu.config(state=tk.DISABLED)
        self.mode_menu.config(state=state)