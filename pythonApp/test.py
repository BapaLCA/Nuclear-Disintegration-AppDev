import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Définition de la fonction modèle
def double_exponential_func(t, a1, b1, a2, b2):
    return a1 * np.exp(-b1 * t) + a2 * np.exp(-b2 * t)

# Fonction pour ajuster et tracer la courbe exponentielle double
def add_double_exponential_fit(ax, data, interval):
    # Générer l'axe des temps basé sur l'intervalle régulier
    t_data = np.arange(len(data)) * interval

    # Ajustement des paramètres de la fonction modèle aux données
    initial_guess = [max(data), 0.1, max(data) / 2, 0.01]  # Guess initial pour les paramètres a1, b1, a2, b2
    params, params_covariance = curve_fit(double_exponential_func, t_data, data, p0=initial_guess)

    # Extraction des paramètres ajustés
    a1, b1, a2, b2 = params

    # Affichage des résultats
    print(f"Paramètres ajustés : a1 = {a1}, b1 = {b1}, a2 = {a2}, b2 = {b2}")

    # Générer les points pour tracer la courbe ajustée
    t_fit = np.linspace(min(t_data), max(t_data), 100)
    y_fit = double_exponential_func(t_fit, a1, b1, a2, b2)

    # Tracer les données mesurées
    ax.scatter(t_data, data, label='Données mesurées', color='red')
    # Tracer la courbe ajustée
    ax.plot(t_fit, y_fit, label='Ajustement double exponentiel', color='blue')

    # Ajouter des labels et une légende
    ax.set_xlabel('Temps (s)')
    ax.set_ylabel('Valeurs mesurées')
    ax.legend()

# Exemple d'utilisation
# Données d'exemple avec un intervalle de temps régulier choisi (par exemple, 5 secondes)
interval = 5  # Intervalle de temps en secondes
data = np.array([15, 12, 9.5, 7.8, 6.5, 5.3, 4.5, 3.8, 3.2, 2.7])

# Création d'un axe de tracé
fig, ax = plt.subplots(figsize=(10, 6))

# Appel de la fonction pour ajouter l'ajustement double exponentiel au tracé
add_double_exponential_fit(ax, data, interval)

# Afficher le graphique
plt.show()
