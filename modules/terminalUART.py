import tkinter as tk
from tkinter import scrolledtext, Button, Entry, OptionMenu, StringVar
import serial
import threading
from serial.tools import list_ports

class UARTTerminal(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # ScrolledText widget pour afficher les données UART
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill='both')

        # Entry et bouton pour saisir et envoyer des données
        self.entry = Entry(self, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, expand=True, fill='x')
        self.send_button = Button(self, text="Envoyer", command=self.send_data)
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

        # Port série
        self.serial_port = None

    def get_available_ports(self):
        ports = [port.device for port in list_ports.comports()]
        return ports

    def connect(self):
        port = self.port_var.get()
        baudrate = int(self.baudrate_var.get())
        if port and port != "Aucun port disponible":
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

    def update_text_area(self, data):
        self.text_area.insert(tk.END, data + '\n')
        self.text_area.yview(tk.END)

    def send_data(self, data):
        if self.serial_port:
            self.serial_port.write(data.encode('utf-8'))

    def send_entry_data(self):
        data = self.entry.get()
        self.send_data(data)
        self.entry.delete(0, tk.END)

    def close(self):
        if self.serial_port:
            self.serial_port.close()