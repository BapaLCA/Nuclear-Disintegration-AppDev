import csv
from collections import defaultdict
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Button
import matplotlib.pyplot as plt

# Définition globale pour être utilisée par d'autres fonctions
data = defaultdict(list)

def exit():
    quit()  # Pour fermer l'application

def open_file(canvas, ax, freq):
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Ouverture d'un explorateur de fichier pour sélectionner un fichier csv à lire
    if not filepath:
        return  # Termine la fonction ici si aucun fichier n'est sélectionné
    global data  # Utilise la variable globale data
    data.clear()  # Efface les anciennes données
    with open(filepath, 'r') as csvfile:  # Ouverture du fichier spécifié en tant que csv
        csvreader = csv.reader(csvfile, delimiter=';')  # Définition du séparateur de données
        for row in csvreader:  # Lecture des données
            try:
                key = int(row[0])  # Lecture des canaux
                value = int(row[1])  # Lecture des valeurs relevées
                if key > 1024:
                    print(f"Line {row} greater than limit has been ignored.")
                    continue  # Ignore la ligne si la valeur dépasse 1024
                data[key].append(value)  # Affectation des données dans le tableau data
            except (ValueError, IndexError) as e:
                # Log the error and continue
                print(f"Error processing line : {row}. IndexError: {e}")
                continue
    plot_data(data, canvas, ax, freq)  # Appel de la fonction d'affichage des données
    return data # On récupère les données dans la fonction qui l'a appelée

def plot_data(data, canvas, ax, freq):
    keys = list(data.keys())  # Échelle horizontale (canaux)
    values = [sum(data[key]) for key in keys]  # On somme les valeurs des canaux entre elles pour les combiner
    
    # Transformation des canaux en temps (20 microsecondes par canal)
    scaled_keys = [key * 1000000/freq for key in keys]

    # On filtre les valeurs pour savoir jusqu'où elles ne sont pas nulles
    non_zero_keys = [key for key, value in zip(scaled_keys, values) if value != 0]
    
    if not non_zero_keys:
        return  # Si toutes les valeurs sont nulles, on ne trace rien

    # On définit l'intervalle où les valeurs sont non nulles pour zoomer
    x_min = min(non_zero_keys)
    x_max = max(non_zero_keys)

    ax.clear()  # Effacer le graphique précédent
    ax.bar(scaled_keys, values, width=20)  # Tracer en graphique à barre des valeurs, avec une largeur adaptée
    ax.set_xlim(x_min, x_max)  # On utilise l'intervalle défini pour zoomer
    ax.set_title('Graph Displayer')
    ax.set_xlabel('Time (in µs)')
    ax.set_ylabel('Iterations')
    ax.grid(True)  # Affichage de la grille

    canvas.draw()  # On met à jour le canvas pour afficher le graphique
