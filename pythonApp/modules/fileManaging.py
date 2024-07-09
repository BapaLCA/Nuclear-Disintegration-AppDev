import csv
from tkinter import filedialog
from tkinter import messagebox

def open_file(control_graph):
    if 1 <= int(control_graph.entry.get()) <= 50000:

        answer = messagebox.askyesno("Load new data ?", "Loading a file will erase all existing data currently measured. Do you wish to continue ?")
        if answer:
            filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Ouverture d'un explorateur de fichier pour sélectionner un fichier csv à lire
            if not filepath:
                return  # Termine la fonction ici si aucun fichier n'est sélectionné
            control_graph.data = [0] * len(control_graph.data)  # Efface les anciennes données
            with open(filepath, 'r') as csvfile:  # Ouverture du fichier spécifié en tant que csv
                csvreader = csv.reader(csvfile, delimiter=';')  # Définition du séparateur de données
                for row in csvreader:  # Lecture des données
                    try:
                        key = int(row[0])  # Lecture des canaux
                        value = float(row[1])  # Lecture des valeurs relevées
                        if key > 1024:
                            print(f"Line {row} greater than limit has been ignored.")
                            continue  # Ignore la ligne si la valeur dépasse 1024
                        control_graph.data[key] = control_graph.data[key]+value  # Affectation des données dans le tableau data
                    except (ValueError, IndexError) as e:
                        # Log the error and continue
                        print(f"Error processing line : {row}. IndexError: {e}")
                        continue
            uart_data = [0]*1024 # Création d'un tableau de données uart vide pour appeler la fonction plot uart
            control_graph.plot_uart_data(uart_data) # On met à jour l'affichage des données
    else:
        messagebox.showinfo("Configuration Error", "Frequency must be set between 1 and 50 000 Hz to display!")

def save_to_csv(data):
    # Ouvrir une boîte de dialogue pour choisir l'emplacement de sauvegarde
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            # Écrire les données avec le format "numéro de cellule;valeur"
            for i, value in enumerate(data):
                writer.writerow([i, value])
        messagebox.showinfo("Success", f"Data has been saved to {file_path}")

