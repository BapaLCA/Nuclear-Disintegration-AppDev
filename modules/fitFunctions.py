from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import math
from scipy.stats import poisson
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def erlang_pdf(x, A, k, lambd):
    """Définition de la formule de la distribution d'Erlang."""
    return A * (lambd ** k * x ** (k - 1) * np.exp(-lambd * x)) / math.factorial(k - 1)

def add_erlang_fit(data, canvas, ax, selected_value, freq):
    """Fonction pour l'affichage de l'exponentielle correspondant à la distribution d'Erlang."""
    k_value = selected_value.get()  # On récupère la valeur de k dans le menu déroulant
    keys = list(data.keys())
    values = [sum(data[key]) for key in keys]
    
    # Mise à l'échelle de l'axe des temps
    scaled_keys = [key * 20 for key in keys]  # 20 microsecondes par canal
    
    try:
        # Ajustement de la courbe d'Erlang aux données
        popt, _ = curve_fit(lambda x, A, lambd: erlang_pdf(x, A, k_value, lambd), scaled_keys, values, p0=[max(values), 0.1])
        
        # Récupération des paramètres optimaux (lambd seulement, k est connu)
        A_optimal, lambd_optimal = popt
        
        # Générer des points pour l'axe x
        x_data = np.linspace(min(scaled_keys), max(scaled_keys), 1000)
        
        # Calculer les valeurs de la fonction d'Erlang
        y_data = erlang_pdf(x_data, A_optimal, k_value, lambd_optimal)
        
        # Tracé des données expérimentales et de l'ajustement de la courbe d'Erlang
        ax.plot(x_data, y_data, color='red', linewidth=2, label=f'Distribution d\'Erlang (k={k_value}, λ={lambd_optimal * 1000000:.2f}, A={A_optimal})')
        ax.legend()
    except RuntimeError as e:
        print(f"Erreur d'ajustement pour k={k_value}: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    
    canvas.draw()  # Redessiner le canvas

    
def gauss(x, a, x0, sigma): #definition de la formule generale d'une Gausienne
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def add_gaussian_fit(data, canvas, ax, freq):
    if not data:
        return
    
    keys = np.array(list(data.keys())) # Echelle horizontale (canaux)
    values = np.array([sum(data[key]) for key in keys]) # On somme les valeurs des canaux entre elles pour les combiner

    # Mise à l'échelle de l'axe des temps
    scaled_keys = [key * 1000000/freq for key in keys]

    mean = sum(scaled_keys * values) / sum(values)
    sigma = np.sqrt(sum(values * (scaled_keys - mean) ** 2) / sum(values))

    popt, pcov = curve_fit(gauss, scaled_keys, values, p0=[max(values), mean, sigma])
    
    x_fit = np.linspace(min(scaled_keys), max(scaled_keys), 1000)
    y_fit = gauss(x_fit, *popt)
    
    ax.plot(x_fit, y_fit, color='green', label='Gaussienne ajustée')
    ax.legend()
    canvas.draw()
    
def add_poisson_fit(data, canvas, ax, freq):
    keys = np.array(list(data.keys())) # Echelle horizontale (canaux)
    values = np.array([sum(data[key]) for key in keys]) # On somme les valeurs des canaux entre elles pour les combiner

    # Mise à l'échelle de l'axe des temps
    scaled_keys = [key * 1000000/freq for key in keys]

    # Estimation de la moyenne de la distribution de Poisson
    mean = sum(scaled_keys * values) / sum(values)
    
    # Génération des valeurs de la distribution de Poisson
    poisson_dist = poisson.pmf(scaled_keys, mean) * sum(values)
    
    ax.plot(keys, poisson_dist, color='blue', label='Distribution de Poisson')
    ax.legend()
    canvas.draw()
