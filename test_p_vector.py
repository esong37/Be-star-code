"""
for different p vector and same alpha, find if the distribution of position angle looks similar or not 
"""

import simulation_control as sc
import numpy as np
import matplotlib.pyplot as plt

def plot_combined_frequency_bars_positions(frequencies_a, frequencies_b, angle_name):
    """
    Plots a combined bar chart for three arrays of frequencies, with 0, 10, ..., 90 as the bin edges.
    Each bin will contain three bars corresponding to the three arrays, with different colors and a legend.
    """
    
    # Setting up the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Bin midpoints for plotting
    bin_edges = range(0, 200, 20)
    bin_mids = [i + 10 for i in bin_edges[:-1]]  # Calculate midpoint for bars
    
    # Calculate positions for a, b, and c bars
    a_positions = [x - 2.5 for x in bin_mids]
    b_positions = [x + 2.5 for x in bin_mids]
    
    # Plotting each set of frequencies
    ax.bar(a_positions, frequencies_a, width=5, label='p vector: [0,1,0]', color='skyblue')
    ax.bar(b_positions, frequencies_b, width=5, label='p vector: [1,0,0]', color='salmon')
    
    # Setting the x-axis to only show the bin edges
    ax.set_xticks(bin_edges)
    ax.set_xticklabels(bin_edges)
    
    # Labels, title, and legend
    ax.set_xlabel(f'{angle_name} angle')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{angle_name} angle distribution \nalpha = 0.8')
    ax.legend(loc='upper right')
    
    # Show plot
    plt.show()

def plot_combined_frequency_bars_inclinations(frequencies_a, frequencies_b, angle_name):
    """
    Plots a combined bar chart for three arrays of frequencies, with 0, 10, ..., 90 as the bin edges.
    Each bin will contain three bars corresponding to the three arrays, with different colors and a legend.
    """
    
    # Setting up the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Bin midpoints for plotting
    bin_edges = range(0, 100, 10)
    bin_mids = [i + 5 for i in bin_edges[:-1]]  # Calculate midpoint for bars
    
    # Calculate positions for a, b, and c bars
    a_positions = [x - 1.25 for x in bin_mids]
    b_positions = [x + 1.25 for x in bin_mids]
    
    # Plotting each set of frequencies
    ax.bar(a_positions, frequencies_a, width=2.5, label='p vector: [0,1,0]', color='skyblue')
    ax.bar(b_positions, frequencies_b, width=2.5, label='p vector: [1,0,0]', color='salmon')
    
    # Setting the x-axis to only show the bin edges
    ax.set_xticks(bin_edges)
    ax.set_xticklabels(bin_edges)
    
    # Labels, title, and legend
    ax.set_xlabel(f'{angle_name} angle')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{angle_name} angle distribution \nalpha = 0.8')
    ax.legend(loc='upper right')
    
    # Show plot
    plt.show()

"""
different p vector, random rotation axes
"""

if __name__ == "__main__":
    star_num = 10000
    viewer = np.array([0,0,0])

    pd1 = np.array([0,1,0])
    pd2 = np.array([1,0,0])
    

    alpha = 0.8

    metaData1, _ = sc.do_cylinder_Simulation(star_num,alpha, viewer, pd1,9)
    metaData2, _ = sc.do_cylinder_Simulation(star_num,alpha, viewer, pd2,9)

    print(metaData1.positions)
    print(metaData2.positions)

    plot_combined_frequency_bars_inclinations(metaData1.inclinations, metaData2.inclinations, "Inclination")
    plot_combined_frequency_bars_positions(metaData1.positions, metaData2.positions,"Position")




    
