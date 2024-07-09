import numpy as np
from modules.fitFunctions import add_erlang_fit, add_poisson_fit, add_gaussian_fit
from tkinter import messagebox

def handle_erlang_mode(control_graph):
    print("Erlang mode detected")
    # Rescaling
    if control_graph.entry.get() != '0':
        period = 1/int(control_graph.entry.get())*1000000
        control_graph.time = np.arange(0, len(control_graph.data) * period, period)
    else:
        control_graph.time = control_graph.data

    # Filtrer les indices des valeurs non nulles dans control_graph.data
    non_zero_indices = [i for i, value in enumerate(control_graph.data) if value != 0]

    if non_zero_indices:
        # Ajuster les limites de l'axe x pour zoomer sur les valeurs non nulles
        min_index = min(non_zero_indices)
        max_index = max(non_zero_indices)

        control_graph.ax.clear()
        control_graph.ax.plot(control_graph.time, control_graph.data, label='Measured Data')
        control_graph.ax.set_title(f"Time elapsed between {control_graph.factor_k+1} atom disintegrations")  # Titre
        control_graph.ax.set_xlabel('Time (microseconds)')  # Abscisse
        control_graph.ax.set_ylabel('Iterance')  # Ordonnée
        control_graph.ax.grid(True)  # Affichage d'une grille

        if control_graph.fit_erlang.get():
            handle_add_erlang_fit(control_graph, control_graph.ax, control_graph.data, control_graph.time, control_graph.factor_k, period)
        if control_graph.fit_gaussian.get():
            print("No Gaussian fit on Erlang mode")
        if control_graph.fit_poisson.get():
            print("No Poisson fit on Erlang mode")

        control_graph.ax.set_xlim(control_graph.time[min_index], control_graph.time[max_index])
        control_graph.ax.legend()
        control_graph.canvas.draw()
    else:
        print("All data values are zero")

def handle_piscine_mode(control_graph):
    # Rescaling
    period = control_graph.delay
    control_graph.time = np.arange(0, len(control_graph.data) * period, period)
    # Filtrer les indices des valeurs non nulles dans control_graph.data
    non_zero_indices = [i for i, value in enumerate(control_graph.data) if value != 0]

    if non_zero_indices:
        # Ajuster les limites de l'axe x pour zoomer sur les valeurs non nulles
        min_index = min(non_zero_indices)
        max_index = max(non_zero_indices)

        control_graph.ax.clear()
        control_graph.ax.plot(control_graph.time, control_graph.data, label='Measured Data')
        control_graph.ax.set_title(f"Number of atom disintegrations measured VS Time elapsed")  # Titre
        control_graph.ax.set_xlabel('Time (seconds)')  # Abscisse
        control_graph.ax.set_ylabel('Number of disintegrations')  # Ordonnée
        control_graph.ax.grid(True)  # Affichage d'une grille

        if control_graph.fit_erlang.get():
            print("No Erlang fit on Pool mode")
        if control_graph.fit_gaussian.get():
            print("No Gaussian fit on Pool mode")
        if control_graph.fit_poisson.get():
            print("No Poisson fit on Pool mode")

        control_graph.ax.set_xlim(control_graph.time[min_index], control_graph.time[max_index])
        control_graph.ax.legend()
        control_graph.canvas.draw()

def handle_default_mode(control_graph):
    print("Default mode detected")
    # Filtrer les indices des valeurs non nulles
    non_zero_indices = [i for i, value in enumerate(control_graph.data) if value != 0]

    if non_zero_indices:
        # Ajuster les limites de l'axe x pour zoomer sur les valeurs non nulles
        min_index = min(non_zero_indices)
        max_index = max(non_zero_indices)

        control_graph.ax.clear()
        control_graph.ax.plot(control_graph.data, label='Measured Data')
        control_graph.ax.set_title(f"Number of atom disintegrations measured in {1/int(control_graph.entry.get())*1000} ms")  # Titre
        control_graph.ax.set_xlabel('Number of atom disintegrations')  # Abscisse
        control_graph.ax.set_ylabel('Iteration')  # Ordonnée
        control_graph.ax.grid(True)  # Affichage d'une grille
        
        if control_graph.mode == "Poisson":
            print("Poisson mode detected")
            if control_graph.fit_erlang.get():
                print("No Erlang fit when Poisson mode")
            if control_graph.fit_gaussian.get():
                handle_add_gaussian_fit(control_graph, control_graph.ax, control_graph.data)
            if control_graph.fit_poisson.get():
                handle_add_poisson_fit(control_graph, control_graph.ax, control_graph.data)

        control_graph.ax.set_xlim(min_index, max_index)
        control_graph.ax.legend()
        control_graph.canvas.draw()

def update_plot(control_graph):
    if control_graph.data is not None:
        print("Update plot called")
        print(control_graph.mode)
        if control_graph.mode == "Erlang":
            handle_erlang_mode(control_graph)
        elif control_graph.mode == "Piscine":
            handle_piscine_mode(control_graph)
        else:
            handle_default_mode(control_graph)
    else:
        print("Data is null")

def handle_add_erlang_fit(graph_control, ax, data, time, k_value, period):
    graph_control.erlang_x, graph_control.erlang_y = add_erlang_fit(ax, data, time, k_value, period)

def handle_add_gaussian_fit(graph_control, ax, data):
    graph_control.gaussian_x, graph_control.gaussian_y = add_gaussian_fit(ax, data)

def handle_add_poisson_fit(graph_control, ax, data):
    graph_control.poisson_x, graph_control.poisson_y = add_poisson_fit(ax, data)

def clear_data(control_graph):
    answer = messagebox.askyesno("Clear All Data ?", "Do you really wish to remove all measured data ? Action can not be reverted.")
    if answer:
        control_graph.reset_tab(control_graph.data)
        control_graph.data = [0] * len(control_graph.data)
        print(control_graph.fit_erlang.get())
        control_graph.fit_erlang.set(False)
        print(control_graph.fit_erlang.get())
        control_graph.fit_poisson.set(False)
        control_graph.fit_gaussian.set(False)
        control_graph.ax.clear()
        control_graph.ax.plot(control_graph.data, label='Measured Data')
        control_graph.ax.set_title('Graphic Displayer')  # Titre
        control_graph.ax.set_xlabel('Channel')  # Abscisse
        control_graph.ax.set_ylabel('Iteration')  # Ordonnée
        control_graph.ax.grid(True)  # Affichage d'une grille
        control_graph.canvas.draw()