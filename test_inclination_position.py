import vector_operations as vo
import simulation_control as sc
import numpy as np
import matplotlib.pyplot as plt
import star_simulation as ss
import math
from scipy.integrate import quad
from scipy.stats import chisquare
from scipy.stats import ks_2samp
# Function to generate random coordinates



def plot_histogram(data):
    """
    This function takes an array of numbers as input and plots a histogram of the data.
    """
    plt.hist(data, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Input Data')
    plt.show()

def plot_histogram_fixed_bins(data,bins,title):
    plt.hist(data, bins=bins, color='#007acc', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value Range')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {title} with Fixed Bins')
    plt.xticks(bins)
    plt.show()


def plot_sphere_with_points(points):
    """
    Plots a sphere with radius 1 centered at (0,0,0) in 3D space,
    and displays a list of points on the sphere.
    
    Parameters:
    - points: A list of numpy arrays, each representing a point [x,y,z] in 3D space.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Define sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Plot sphere
    ax.plot_surface(x, y, z, color='b', alpha=0.3)
    
    # Plot points
    for point in points:
        ax.scatter(point[0], point[1], point[2], color='r', s=10)
    
    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set aspect ratio to equal for 3D plot
    ax.set_box_aspect([1,1,1])  # Equal aspect ratio
    
    plt.show()


def generate_sine_distributed_array(n, numStars):
    total_degrees = 90
    radians_per_degree = math.pi / 180

    interval_size = total_degrees * radians_per_degree / n

    def sin_integral(x1, x2):
        result, _ = quad(np.sin, x1, x2)
        return result
    
    areas_scaled = [sin_integral(i * interval_size, (i+1) * interval_size) * numStars for i in range(n)]

    return areas_scaled

def data_amount_difference(num_stars,test_number):
    viewer = np.array([0,0,0])
    pd = np.array([0,0,1])
    alpha = 0

    in_bins = np.arange(0,95,10)
    po_bins = np.arange(0,185,20)

    # chi square test
    excepted_sin_list = generate_sine_distributed_array(9,num_stars)
    
    chi2_list = []
    ks_list = []

    for i in range(test_number):
        metadata, stars = sc.do_cylinder_Simulation(num_stars, alpha, viewer,pd,9)

        inclination_list = []
        position_list = []
        for star in stars:
            inclination_list.append(star.i)
            position_list.append(star.p)
        in_chi2, p_c = chisquare(metadata.inclinations, f_exp=excepted_sin_list)
        in_ks, p_k = ks_2samp(metadata.inclinations, excepted_sin_list)

        chi2_list.append(in_chi2)
        ks_list.append(in_ks)
        # print and plot
        """
        print(f"inclination bins: {metadata.inclinations}")
        print(f"excepted inclination bins: {excepted_sin_list}")
        print(f"position bins: {metadata.positions}")

        # plot the inclinations and positions distribution
        plot_histogram_fixed_bins(inclination_list,in_bins,f"inclination (chi2: {round(in_chi2,4)})")
        plot_histogram_fixed_bins(position_list,po_bins,"position")
        """ 
    print("-----------")
    return chi2_list, ks_list

def plot_prediction_boxplots(prediction_dict,xlabel,ylabel, title):
    key_values = list(prediction_dict.keys())
    value_lists = list(prediction_dict.values())
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(value_lists, labels=[str(key) for key in key_values])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    num_test = 100
    chi2_result = {}
    ks_result = {}
    for num_star in np.array([10,100,500,1000,5000,10000]):
        chi2_list, ks_list = data_amount_difference(num_star,num_test)
        chi2_result[num_star] = chi2_list
        ks_result[num_star] = ks_list
        
    plot_prediction_boxplots(chi2_result,"num stars","chi2 value", "distribution of chi2 value for different number of sample")
    plot_prediction_boxplots(ks_result,"num stars","ks value", "distribution of ks value for different number of sample")
    


    




