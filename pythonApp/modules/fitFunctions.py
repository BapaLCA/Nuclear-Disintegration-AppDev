import numpy as np
import math
from scipy.optimize import curve_fit
from scipy.stats import poisson
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def erlang_pdf(x, A, k, lambd):
    # Definition of the Erlang distribution function
    return A * (lambd ** k * x ** (k - 1) * np.exp(-lambd * x)) / math.factorial(k - 1)

def add_erlang_fit(ax, data, time, k_value, period):
    # Function to calculate and plot the fitting Erlang function depending on data received
    print(data)
    values = data
    keys = time

    try:
        # Limit X values to the length of the data
        keys = keys[keys <= len(data) * period]
        
        # Adjusting Erlang function to the data with lambd limits
        popt, _ = curve_fit(lambda x, A, lambd: erlang_pdf(x, A, k_value, lambd), keys, values, p0=[max(values), 0.1])
        
        # Recovering the optimal parameters (only lambda, as k is already known)
        A_optimal, lambd_optimal = popt
        
        # Generate points for X axis
        x_data = np.linspace(min(keys), min(len(data) * period, max(keys)), 1000)
        
        # Calculating the points of the Erlang function
        y_data = erlang_pdf(x_data, A_optimal, k_value, lambd_optimal)
        
        # Plotting erlang function
        ax.plot(x_data, y_data, color='red', linewidth=2, label=f'Erlang Fit (k={k_value}, λ={lambd_optimal:.6f}, A={round(A_optimal, 2)})')
    except RuntimeError as e:
        print(f"Erreur d'ajustement pour k={k_value}: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    return x_data, y_data # Returns the fitting X and Y for saving to csv option

def gauss(x, a, x0, sigma):
    # Definition of the Gaussian distribution function
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def add_gaussian_fit(ax, data):
    # Function to calculate and plot the fitting Gaussian function depending on data received
    keys = np.linspace(0, len(data), len(data)) # Generates the X axis matching the data's length
    values = data # Stores the data values

    mean = sum(keys * values) / sum(values)
    sigma = np.sqrt(sum(values * (keys - mean) ** 2) / sum(values))

    popt, pcov = curve_fit(gauss, keys, values, p0=[max(values), mean, sigma])
    
    x_fit = np.linspace(min(keys), min(1024, max(keys)), 1000)
    y_fit = gauss(x_fit, *popt)
    
    ax.plot(x_fit, y_fit, color='green', label='Gaussian Fit')
    return x_fit, y_fit # Returns the fitting X and Y for saving to csv option

def add_poisson_fit(ax, data):
    # Function to calculate and plot the fitting Poisson function depending on data received
    keys = np.linspace(0, len(data), len(data)) # Generates the X axis matching the data's length
    values = data # Stores the data values

    mean = sum(keys * values) / sum(values)
    
    poisson_dist = poisson.pmf(np.arange(len(values)), mean) * sum(values)
    
    ax.plot(keys, poisson_dist, color='red', label='Poisson Fit')
    return keys, poisson_dist # Returns the fitting X and Y for saving to csv option

# Exponential function definition
def exponential(t, a, b):
    return a * np.exp(-b * t)

# Exponential fitting function for graph
def add_exponential_fit(ax, data, interval):
    # Generate the X axis based on time interval
    t_data = np.arange(len(data)) * interval

    # Adjusting parameters based on the exponential function and measured data
    initial_guess = [max(data), 0.1]  # Initial guess for a and b parameters
    params, params_covariance = curve_fit(exponential, t_data, data, p0=initial_guess)

    # Adjusted parameters extraction
    a, b = params

    # Display of parameters (debug)
    #print(f"Adjusted Parameters : a = {a}, b = {b}")

    # Generate points for plotting
    t_fit = np.linspace(min(t_data), max(t_data), 100)
    y_fit = exponential(t_fit, a, b)

    # Plotting adjusted function
    ax.plot(t_fit, y_fit, label='Exponential fit', color='red')

    return t_fit, y_fit # Returns the fitting X and Y for saving to csv option

# Double Exponential function definition
def double_exponential_func(t, a1, b1, a2, b2):
    return a1 * np.exp(-b1 * t) + a2 * np.exp(-b2 * t)

# Double Exponential fitting function for graph
def add_double_exponential_fit(ax, data, interval):
    # Generate the X axis based on interval given
    t_data = np.arange(len(data)) * interval

    # Adjusting parameters based on double exponential definition
    initial_guess = [max(data), 0.1, max(data) / 2, 0.01]  # Initial guess initial for parameters a1, b1, a2, b2
    params, params_covariance = curve_fit(double_exponential_func, t_data, data, p0=initial_guess)

    # Extracting adjusted parameters
    a1, b1, a2, b2 = params

    # Displaying results (debug)
    #print(f"Adjusted parameters : a1 = {a1}, b1 = {b1}, a2 = {a2}, b2 = {b2}")

    # Generates points for plotting
    t_fit = np.linspace(min(t_data), max(t_data), 100)
    y_fit = double_exponential_func(t_fit, a1, b1, a2, b2)

    # Plotting adjusted function
    ax.plot(t_fit, y_fit, label='Exponential fit', color='red')

    return t_fit, y_fit # Returns the fitting X and Y for saving to csv option