import tkinter as tk
from tkinter import scrolledtext, Button, Entry, OptionMenu, StringVar, Label, Frame, messagebox
import serial
import threading
from serial.tools import list_ports

class UARTTerminal(tk.Frame):
    def __init__(self, master, data_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.data_callback = data_callback  # Callback to notify the controller

        # Configurer la grille principale pour qu'elle s'étende et redimensionne les widgets
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Label for the UART terminal title
        self.labelUART = tk.Label(self, text="UART Terminal", font=("Arial", 16, "bold"), fg="blue", relief="raised")
        self.labelUART.grid(row=0, column=0, columnspan=5, sticky="ew")

        # ScrolledText widget to display UART data
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.grid(row=1, column=0, columnspan=5, sticky="nsew")

        # Entry and button to input and send data
        self.entry = Entry(self, font=("Arial", 12))
        self.entry.grid(row=2, column=0, columnspan=4, sticky="ew")
        self.send_button = Button(self, text="Send", command=self.send_data_entry)
        self.send_button.grid(row=2, column=4, sticky="ew")

        # Menu for selecting the COM port
        self.port_var = StringVar(self)
        self.ports = self.get_available_ports()
        if self.ports:
            self.port_var.set(self.ports[0])
        else:
            self.ports.append("No port available")
            self.port_var.set(self.ports[0])
        self.port_menu = OptionMenu(self, self.port_var, *self.ports)
        self.port_menu.config(width=15)
        self.port_menu.grid(row=3, column=0, sticky="ew")

        # Refresh button to update the list of available ports
        self.refresh_button = Button(self, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_button.grid(row=3, column=1, sticky="ew")

        # Baudrate selection menu
        self.baudrate_var = StringVar(self)
        self.baudrate_var.set("9600")
        self.baudrate_options = ["9600", "19200", "38400", "57600", "115200"]
        self.baudrate_menu = OptionMenu(self, self.baudrate_var, *self.baudrate_options)
        self.baudrate_menu.config(width=15)
        self.baudrate_menu.grid(row=3, column=2, sticky="ew")

        # Frame for the status label
        self.status_frame = Frame(self, bd=2, relief="groove")
        self.status_frame.grid(row=3, column=4, padx=5, pady=5, sticky="ew")

        # Status label to display the current status
        self.status_label = Label(self.status_frame, text="Status : Unknown", font=("Arial", 10), width=15, anchor='w')
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Variable to track the status of the PIC
        self.status = "?"

        # Serial port
        self.serial_port = None  # Default value

        # Array to store received data
        self.received_data = [0] * 1024

        

        # Configurer les lignes et colonnes de la grille pour qu'elles s'étendent avec la fenêtre
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def get_available_ports(self):
        ports = [port.device for port in list_ports.comports()]
        return ports

    def refresh_ports(self):
        """Refresh the list of available serial ports in the dropdown menu."""
        self.ports = self.get_available_ports()
        menu = self.port_menu['menu']
        menu.delete(0, 'end')
        if self.ports:
            for port in self.ports:
                menu.add_command(label=port, command=lambda value=port: self.port_var.set(value))
            self.port_var.set(self.ports[0])
        else:
            menu.add_command(label="No port available", command=lambda: self.port_var.set("No port available"))
            self.port_var.set("No port available")

    def connect(self):
        print("Button connect clicked")
        port = self.port_var.get()
        baudrate = int(self.baudrate_var.get())
        if port and port != "No port available":
            
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            # Start the thread to read UART data
            self.read_thread = threading.Thread(target=self.read_uart)
            self.read_thread.daemon = True
            self.read_thread.start()
            messagebox.showinfo("UART Terminal", f"Successfully connected to port {self.port_var.get()}")

    def read_uart(self):
        while True:
            if self.serial_port and self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode('utf-8').strip()
                self.update_text_area(data)
                self.check_status(data)
                self.save_data(data)

    def check_status(self, data):
        # Check specific values and update the label
        if data == "w":
            self.status_label.config(text="Status : Writing")
            self.status = "w"
        elif data == "m":
            self.status_label.config(text="Status : Measuring")
            self.status = "m"
        elif data == "i":
            self.status_label.config(text="Status : Idle")
            self.status = "i"
        elif data == "d":
            self.data_callback(self.received_data)  # Notify the controller
            self.status_label.config(text="Status : Done Writing")
            self.status = "d"

    def get_status(self):
        return self.status

    def update_text_area(self, data):
        self.text_area.insert(tk.END, data + '\n')
        self.text_area.yview(tk.END)

    def save_data(self, data):
        try:
            parts = data.split(';')
            if len(parts) == 2:
                index = int(parts[0])
                value = int(parts[1])
                if 0 <= index < 1024:
                    self.received_data[index] = value
        except ValueError:
            # Ignore the line if the format is incorrect
            pass

    def get_received_data(self):
        return self.received_data

    def send_data_entry(self):
        data = self.entry.get()
        if self.serial_port is not None:
            self.serial_port.write(data.encode())
            self.entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Terminal error", "Serial port is not initialized!")

    def send_data(self, data):
        if self.serial_port is not None:
            self.serial_port.write(data.encode())
            self.entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Terminal error", "Serial port is not initialized!")

    def close(self):
        if self.serial_port:
            self.serial_port.close()