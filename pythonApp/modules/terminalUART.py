import tkinter as tk
from tkinter import scrolledtext, Button, Entry, OptionMenu, StringVar, Label, Frame
import serial
import threading
from serial.tools import list_ports

class UARTTerminal(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # Label pour le titre du terminal
        self.labelUART = tk.Label(self, text="UART Terminal", font=("Arial", 16, "bold"), fg="blue", relief="raised")
        self.labelUART.pack(side=tk.TOP)
        # ScrolledText widget pour afficher les données UART
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Entry et bouton pour saisir et envoyer des données
        self.entry = Entry(self, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, expand=True, fill='x')
        self.send_button = Button(self, text="Envoyer", command=self.send_data_entry)
        self.send_button.pack(side=tk.RIGHT)

        # Menu déroulant pour sélectionner le port COM
        self.port_var = StringVar(self)
        self.ports = self.get_available_ports()
        if self.ports:
            self.port_var.set(self.ports[0])
        else:
            self.ports.append("Aucun port disponible")
            self.port_var.set(self.ports[0])
        self.port_menu = OptionMenu(self, self.port_var, *self.ports)
        self.port_menu.pack(side=tk.LEFT)

        # Baudrate
        self.baudrate_var = StringVar(self)
        self.baudrate_var.set("9600")
        self.baudrate_options = ["9600", "19200", "38400", "57600", "115200"]
        self.baudrate_menu = OptionMenu(self, self.baudrate_var, *self.baudrate_options)
        self.baudrate_menu.pack(side=tk.LEFT)

        # Frame pour le label de statut
        self.status_frame = Frame(self, bd=2, relief="groove")
        self.status_frame.pack(side=tk.LEFT, padx=5, pady=5)

        # Label pour afficher l'état
        self.status_label = Label(self.status_frame, text="Status : Unknown", font=("Arial", 10), width=15, anchor='w')
        self.status_label.pack(side=tk.BOTTOM)

        # Variable déterminant le status du PIC
        self.status = "?"

        # Port série
        self.serial_port = None # Valeur par défaut

        # Tableau pour stocker les données reçues
        self.received_data = [0] * 1024

    def get_available_ports(self):
        ports = [port.device for port in list_ports.comports()]
        return ports

    def connect(self):
        port = self.port_var.get()
        baudrate = int(self.baudrate_var.get())
        if port and port != "No port available":
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            # Démarrer le thread pour lire les données UART
            self.read_thread = threading.Thread(target=self.read_uart)
            self.read_thread.daemon = True
            self.read_thread.start()

    def read_uart(self):
        while True:
            if self.serial_port and self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode('utf-8').strip()
                self.update_text_area(data)
                self.check_status(data)
                self.save_data(data)
                print(self.received_data)

    def check_status(self, data):
        # Vérifiez les valeurs spécifiques et mettez à jour le label
        if data == "w":
            self.status_label.config(text="Status : Writing")
            self.status = "w"
        elif data == "m":
            self.status_label.config(text="Status : Measuring")
            self.status = "m"
        elif data == "i":
            self.status_label.config(text="Status : Idle")
            self.status = "i"

    def get_status(self):
        return self.status

    def update_text_area(self, data):
        self.text_area.insert(tk.END, data + '\n')
        self.text_area.yview(tk.END)

    def save_data(self, data):
        try:
            parts = data.split(';') # On détermine le séparateur
            if len(parts) == 2: # On indique qu'il y a deux valeurs à lire par ligne
                index = int(parts[0]) # La première valeur correspond au numéro de la cellule du tableau
                value = int(parts[1]) # La seconde valeur correspond à la valeur de cette cellule
                if 0 <= index < 1024: # Si le numero de cellule depasse 1024, on ignore la ligne
                    self.received_data[index] = value
        except ValueError:
            # Si le format est incorrect, on ignore la ligne
            pass

    def get_received_data(self): # Fonction pour récupérer les données du tableau
        return self.received_data


    def send_data_entry(self):
        data = self.entry.get()
        self.serial_port.write(data.encode())
        self.entry.delete(0, tk.END)

    def send_data(self, data):
        if self.serial_port is not None:
            self.serial_port.write(data.encode())
            self.entry.delete(0, tk.END)
        else:
            print("Erreur: serial_port n'est pas initialisé.")

    def close(self):
        if self.serial_port:
            self.serial_port.close()