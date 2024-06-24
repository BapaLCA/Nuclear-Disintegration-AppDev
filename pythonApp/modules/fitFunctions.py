# erlang_fit.py
import numpy as np
import math
from scipy.optimize import curve_fit
from scipy.stats import poisson

def erlang_pdf(x, A, k, lambd):
    # Définition de la formule de la distribution d'Erlang
    return A * (lambd ** k * x ** (k - 1) * np.exp(-lambd * x)) / math.factorial(k - 1)

def add_erlang_fit(ax, data, k_value):
    # Fonction pour l'affichage de l'exponentielle correspondant à la distribution d'Erlang.
    values = data
    scaled_keys = np.linspace(0, len(data), len(data)) #* 20  # 20 microsecondes par canal

    try:
        # Limiter les valeurs x à 1024
        scaled_keys = scaled_keys[scaled_keys <= 1024]
        values = values[:len(scaled_keys)]
        
        # Ajustement de la courbe d'Erlang aux données
        popt, _ = curve_fit(lambda x, A, lambd: erlang_pdf(x, A, k_value, lambd), scaled_keys, values, p0=[max(values), 0.1])
        
        # Récupération des paramètres optimaux (lambd seulement, k est connu)
        A_optimal, lambd_optimal = popt
        
        # Générer des points pour l'axe x
        x_data = np.linspace(min(scaled_keys), min(1024, max(scaled_keys)), 1000)
        
        # Calculer les valeurs de la fonction d'Erlang
        y_data = erlang_pdf(x_data, A_optimal, k_value, lambd_optimal)
        
        # Tracé des données expérimentales et de l'ajustement de la courbe d'Erlang
        ax.plot(x_data, y_data, color='red', linewidth=2, label=f'Erlang Fit (k={k_value}, λ={lambd_optimal:.2f}, A={round(A_optimal, 2)})')
    except RuntimeError as e:
        print(f"Erreur d'ajustement pour k={k_value}: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    return x_data, y_data

def gauss(x, a, x0, sigma):
    # Définition de la formule générale d'une gaussienne
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def add_gaussian_fit(ax, data):
    
    scaled_keys = np.linspace(0, len(data), len(data)) #* 20  # 20 microsecondes par canal
    values = data

    mean = sum(scaled_keys * values) / sum(values)
    sigma = np.sqrt(sum(values * (scaled_keys - mean) ** 2) / sum(values))

    popt, pcov = curve_fit(gauss, scaled_keys, values, p0=[max(values), mean, sigma])
    
    x_fit = np.linspace(min(scaled_keys), min(1024, max(scaled_keys)), 1000)
    y_fit = gauss(x_fit, *popt)
    
    ax.plot(x_fit, y_fit, color='green', label='Gaussian Fit')

def add_poisson_fit(ax, data):
    scaled_keys = np.linspace(0, len(data), len(data)) #* 20  # 20 microsecondes par canal
    values = data

    mean = sum(scaled_keys * values) / sum(values)
    
    poisson_dist = poisson.pmf(np.arange(len(values)), mean) * sum(values)
    
    ax.plot(scaled_keys, poisson_dist, color='yellow', label='Poisson Fit')
