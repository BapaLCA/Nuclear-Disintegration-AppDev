import csv
from tkinter import filedialog
from tkinter import messagebox
from modules.objects import CustomDialog

def open_file(control_graph):
    if 1 <= int(control_graph.entry.get()) <= 50000:

        answer = messagebox.askyesno("Load new data ?", "Loading a file will erase all existing data currently measured. Do you wish to continue ?")
        if answer:
            filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Opens a file explorer to select a .csv file to read
            if not filepath:
                return  # Ends function here if no file are selected
            control_graph.data = [0] * len(control_graph.data)  # Deletes previous data
            with open(filepath, 'r') as csvfile:  # Open file specified as .csv
                csvreader = csv.reader(csvfile, delimiter=';')  # Definition of the data separator
                for row in csvreader:  # Reading data
                    try:
                        key = int(row[0])  # Reading of indexes
                        value = float(row[1])  # Reading values measured
                        if key > 1024:
                            print(f"Line {row} greater than limit has been ignored.")
                            continue  # Ignores the line if the value goes over 1024
                        control_graph.data[key] = control_graph.data[key]+value  # Append data in the tab data
                    except (ValueError, IndexError) as e:
                        # Log the error and continue
                        print(f"Error processing line : {row}. IndexError: {e}")
                        continue
            uart_data = [0]*1024 # Creates an empty uart data tab to call the plot uart function
            control_graph.plot_uart_data(uart_data) # Update data displayed on graph
    else:
        messagebox.showinfo("Configuration Error", "Frequency must be set between 1 and 50 000 Hz to display!")

def choose_fit(control_graph): # Message box to select which fit function that's currently displayed you want to save to CSV
        if not control_graph.fit_erlang.get() and not control_graph.fit_poisson.get() and not control_graph.fit_gaussian.get() and not control_graph.fit_exponential.get():
            messagebox.showinfo("Saving Data error", "No fit function are currently plotted!")
        else:
            dialog = CustomDialog(control_graph.control_frame, title="Saving fit data", show_choice1=control_graph.fit_erlang.get(), show_choice2=control_graph.fit_gaussian.get(), show_choice3=control_graph.fit_poisson.get(), show_choice4=control_graph.fit_exponential.get())
            if dialog.choice == "Erlang":
                save_to_csv(control_graph.erlang_y)
            if dialog.choice == "Poisson":
                save_to_csv(control_graph.poisson_y)
            if dialog.choice == "Gaussian":
                save_to_csv(control_graph.gaussian_y)
            if dialog.choice == "Exponential":
                save_to_csv(control_graph.exponential_y)

def save_to_csv(data):
    # Open a dialog box to choose the output location
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            # Write the data into CSV format with ';' as separator (Index;Value)
            for i, value in enumerate(data):
                writer.writerow([i, value])
        messagebox.showinfo("Success", f"Data has been saved to {file_path}")

