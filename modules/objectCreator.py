import tkinter as tk
from tkinter import Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def createGraph(x_coord, y_coord, canvas, root):
# Crée une figure matplotlib vide
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_title('Graphic Displayer')  # Titre
    ax.set_xlabel('Time (in µs)')  # Abscisse
    ax.set_ylabel('Iteration')  # Ordonnée
    ax.grid(True)  # Affichage d'une grille

    # Intègre la figure matplotlib dans Tkinter
    figure_canvas = FigureCanvasTkAgg(fig, master=root)
    figure_canvas.draw()
    figure_widget = figure_canvas.get_tk_widget()

    # Place la figure aux coordonnées données
    canvas.create_window(x_coord, y_coord, window=figure_widget, anchor=tk.NW)

    return fig, ax