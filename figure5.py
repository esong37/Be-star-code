"""
当权重值alpha为0时，
生成的恒星数据集的inclination angle分布将近似于sin i 分布，
而position angle分布近似于uniform distribution。
从Figure 4 可得，当数据集内的恒星数量增长时，分布相似程度越高。

Figure 4 表示不同恒星数量的数据集内inclination angle 和position angle分布状况。
"""
import simulation_control as sc
import numpy as np
import matplotlib.pyplot as plt
import bf_search
import test_red_chi as trc

def plot_combined_frequency_bars_inclinations(frequencies_a, star_num, angle_name):
    """
    Plots a combined bar chart for three arrays of frequencies, with 0, 10, ..., 90 as the bin edges.
    Each bin will contain three bars corresponding to the three arrays, with different colors and a legend.
    """
    
    # Setting up the plot
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Bin midpoints for plotting
    bin_edges = range(0, 100, 10)
    bin_mids = [i + 5 for i in bin_edges[:-1]]  # Calculate midpoint for bars
    
    # Plotting each set of frequencies
    #ax.bar(bin_mids, frequencies_a, width=5, label='p vector: [0,1,0]', color='skyblue')
    ax.bar(bin_mids, frequencies_a, width=7, color='skyblue')
    
    # Setting the x-axis to only show the bin edges
    ax.set_xticks(bin_edges)
    ax.set_xticklabels(bin_edges)
    
    # Labels, title, and legend
    ax.set_xlabel(f'{angle_name} angle')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{star_num} stars {angle_name} angle distribution')
    ax.legend(loc='upper right')
    
    # Show plot
    plt.show()

def plot_combined_frequency_bars_positions(frequencies_a, star_num, angle_name):
    """
    Plots a combined bar chart for three arrays of frequencies, with 0, 10, ..., 90 as the bin edges.
    Each bin will contain three bars corresponding to the three arrays, with different colors and a legend.
    """
    
    # Setting up the plot
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Bin midpoints for plotting
    bin_edges = range(0, 200, 20)
    bin_mids = [i + 10 for i in bin_edges[:-1]]  # Calculate midpoint for bars
    
    # Plotting each set of frequencies
    #ax.bar(bin_mids, frequencies_a, width=5, label='p vector: [0,1,0]', color='skyblue')
    ax.bar(bin_mids, frequencies_a, width=15, color='skyblue')
    
    # Setting the x-axis to only show the bin edges
    ax.set_xticks(bin_edges)
    ax.set_xticklabels(bin_edges)
    
    # Labels, title, and legend
    ax.set_xlabel(f'{angle_name} angle')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{star_num} stars {angle_name} angle distribution')
    ax.legend(loc='upper right')
    
    # Show plot
    plt.show()

def create_data():
    alpha = 0
    viewer = np.array([0,0,0])
    num_stars = 10000
    pd = np.random.uniform(-1,1,3)

    in_chi_value_list = []
    in_ks_value_list = []
    po_chi_value_list = []
    po_ks_value_list = []



    for alpha in np.arange(0.0, 1.05, 0.05):
        metaData1, _ = sc.do_cylinder_Simulation(num_stars,alpha, viewer, pd,9)
        metaData2, _ = sc.do_cylinder_Simulation(num_stars,alpha, viewer, pd,9)

        in_chi_value = trc.reset_chi_value_equl_size(metaData1.inclinations,metaData2.inclinations)
        in_ks_value = trc.ks_test(metaData1.inclinations,metaData2.inclinations)

        po_chi_value = trc.reset_chi_value_equl_size(metaData1.positions,metaData2.positions)
        po_ks_value = trc.ks_test(metaData1.positions,metaData2.positions)

        in_chi_value_list.append(in_chi_value)
        in_ks_value_list.append(in_ks_value)
        po_chi_value_list.append(po_chi_value)
        po_ks_value_list.append(po_ks_value)



    np.save("data/figure5/in_chi_value_list.npy",np.array(in_chi_value_list))
    np.save("data/figure5/in_ks_value_list.npy",np.array(in_ks_value_list))
    np.save("data/figure5/po_chi_value_list.npy",np.array(po_chi_value_list))
    np.save("data/figure5/po_ks_value_list.npy",np.array(po_ks_value_list))

    print("complete!!!!!!!!!!!!!")

def plot_data():
    in_chi_value_list = np.load("data/figure5/in_chi_value_list.npy")
    in_ks_value_list = np.load("data/figure5/in_ks_value_list.npy")
    po_chi_value_list = np.load("data/figure5/po_chi_value_list.npy")
    po_ks_value_list = np.load("data/figure5/po_ks_value_list.npy")
    print(in_chi_value_list)
    print(in_ks_value_list)
    print(po_chi_value_list)
    print(po_ks_value_list)






if __name__ == "__main__":
    create_data()
    plot_data()
    pass





    
    