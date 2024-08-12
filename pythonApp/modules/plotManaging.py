import numpy as np
from modules.fitFunctions import add_erlang_fit, add_poisson_fit, add_gaussian_fit, add_exponential_fit, add_double_exponential_fit
from tkinter import messagebox

def handle_erlang_mode(control_graph):
    print("Erlang mode detected")
    # Rescaling
    if control_graph.entry.get() != '0':
        period = 1/int(control_graph.entry.get())*1000000
        control_graph.time = np.arange(0, len(control_graph.data) * period, period)
    else:
        control_graph.time = control_graph.data

    # Filters the none-null values for zooming on graph
    non_zero_indices = [i for i, value in enumerate(control_graph.data) if value != 0]

    if non_zero_indices:
        # Adjust X axis limit to zoom in on none-null values
        min_index = min(non_zero_indices)
        max_index = max(non_zero_indices)

        control_graph.ax.clear()
        control_graph.ax.plot(control_graph.time, control_graph.data, label='Measured Data')
        control_graph.ax.set_title(f"Time elapsed between {control_graph.factor_k+1} nuclei disintegrations")  # Title
        control_graph.ax.set_xlabel('Time (microseconds)')  # X Axis
        control_graph.ax.set_ylabel('Iterance')  # Y Axis
        control_graph.ax.grid(True)  # Display grid

        # Checks if fitting functions are enabled
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
    # Filters the none-null values for zooming on graph
    non_zero_indices = [i for i, value in enumerate(control_graph.data) if value != 0]

    if non_zero_indices:
        # Adjust X axis limit to zoom in on none-null values
        min_index = min(non_zero_indices)
        max_index = max(non_zero_indices)

        control_graph.ax.clear()
        control_graph.ax.plot(control_graph.time, control_graph.data, label='Measured Data')
        control_graph.ax.set_title(f"Number of nuclei decays measured VS Time elapsed")  # Title
        control_graph.ax.set_xlabel('Time (seconds)')  # X axis
        control_graph.ax.set_ylabel('Number of disintegrations')  # Y axis
        control_graph.ax.grid(True)  # Display grid

        # Checks if fitting functions are enabled
        if control_graph.fit_erlang.get():
            print("No Erlang fit on Pool mode")
        if control_graph.fit_gaussian.get():
            print("No Gaussian fit on Pool mode")
        if control_graph.fit_poisson.get():
            print("No Poisson fit on Pool mode")
        if control_graph.fit_exponential.get():
            handle_add_exponential_fit(control_graph, control_graph.ax, control_graph.data)

        control_graph.ax.set_xlim(control_graph.time[min_index], control_graph.time[max_index])
        control_graph.ax.legend()
        control_graph.canvas.draw()

def handle_default_mode(control_graph):
    print("Default mode detected")
    # Filters the none-null values for zooming on graph
    non_zero_indices = [i for i, value in enumerate(control_graph.data) if value != 0]

    if non_zero_indices:
        # Adjust X axis limit to zoom in on none-null values
        min_index = min(non_zero_indices)
        max_index = max(non_zero_indices)

        control_graph.ax.clear()
        control_graph.ax.plot(control_graph.data, label='Measured Data')
        control_graph.ax.set_title(f"Number of nuclei decays measured in {1/int(control_graph.entry.get())*1000} ms")  # Title
        control_graph.ax.set_xlabel('Number of nuclei decays')  # X axis
        control_graph.ax.set_ylabel('Iteration')  # Y axis
        control_graph.ax.grid(True)  # Display grid
        
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
    if control_graph.data is not None: # Checks if the data measure is not null
        print("Update plot called")
        print(control_graph.mode)
        # Calls the corresponding function depending on mode
        if control_graph.mode == "Erlang":
            handle_erlang_mode(control_graph)
        elif control_graph.mode == "Activation":
            handle_piscine_mode(control_graph)
        else: # Uses Poisson mode as default
            handle_default_mode(control_graph)
    else:
        print("Data is null")

def handle_add_erlang_fit(graph_control, ax, data, time, k_value, period):
    graph_control.erlang_x, graph_control.erlang_y = add_erlang_fit(ax, data, time, k_value, period)

def handle_add_gaussian_fit(graph_control, ax, data):
    graph_control.gaussian_x, graph_control.gaussian_y = add_gaussian_fit(ax, data)

def handle_add_poisson_fit(graph_control, ax, data):
    graph_control.poisson_x, graph_control.poisson_y = add_poisson_fit(ax, data)

def handle_add_exponential_fit(graph_control, ax, data):
    graph_control.exponential_x, graph_control.exponential_y = add_exponential_fit(ax, data, graph_control.delay)

def clear_data(control_graph):
    answer = messagebox.askyesno("Clear All Data ?", "Do you really wish to remove all measured data ? Action can not be reverted.")
    if answer:
        # Resets data measured and disables fitting function display
        control_graph.reset_tab(control_graph.data)
        control_graph.fit_erlang.set(False)
        control_graph.fit_poisson.set(False)
        control_graph.fit_gaussian.set(False)
        control_graph.fit_exponential.set(False)
        control_graph.ax.clear()
        # Reset graph parameters to default
        control_graph.ax.plot(control_graph.data, label='Measured Data')
        control_graph.ax.set_title('Graphic Displayer')  # Title
        control_graph.ax.set_xlabel('Channel')  # X axis
        control_graph.ax.set_ylabel('Iteration')  # Y axis
        control_graph.ax.grid(True)  # Display Grid
        control_graph.canvas.draw()