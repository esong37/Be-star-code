import numpy as np
from scipy.stats import chisquare
import simulation_control as sc
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

# eliminte the zeros in B(excepted) and sum the first n element less than 100/1000
def reset_chi_value_equl_size(A,B):
    index = 0

    for i in range(len(B)):
        if B[i] == 0 or sum(B[:i]) < 10:
            index = i
    newA = []
    newB = []
    newA.append(sum(A[:index+1]))
    newB.append(sum(B[:index+1]))

    newA.extend(A[index+1:])
    newB.extend(B[index+1:])

    chi2, p = chisquare(newA, f_exp=newB)

    return chi2


# eliminte the zeros in B(excepted) and sum the first n element less than 100/1000
def reset_red_chi_value_equl_size(A,B,df = 9):
    index = 0

    for i in range(len(B)):
        if B[i] == 0 or sum(B[:i]) < 10:
            index = i
    newA = []
    newB = []
    newA.append(sum(A[:index+1]))
    newB.append(sum(B[:index+1]))

    newA.extend(A[index+1:])
    newB.extend(B[index+1:])

    chi2, p = chisquare(newA, f_exp=newB)

    return chi2/df

# adjust the size of B
def red_chi_value(A,B,df=9):
    newB = []
    newB.extend(np.array(B)*(sum(A)/sum(B)))

    chi = reset_red_chi_value_equl_size(A,newB,df = 9)
    return chi

def ks_test(A,B):
    ks, p_k = ks_2samp(A, B)
    return ks


def create_test_data(A_num,test_num,test_id):
    in_chi_list = []
    po_chi_list = []

    in_ks_list = []
    po_ks_list = []

    alpha_list = []
    theta_list = []
    phi_list = []
    alpha = 0.8
    
    for i in range(test_num):
        pd = np.random.uniform(-1, 1, 3)
        mA,_ = sc.do_cylinder_Simulation(A_num,alpha,np.array([0,0,0]),pd,9)
        mB,_ = sc.do_cylinder_Simulation(1000,alpha,np.array([0,0,0]),pd,9)

        in_chi = red_chi_value(mA.inclinations,mB.inclinations)
        po_chi = red_chi_value(mA.positions,mB.positions)

        in_ks = ks_test(mA.inclinations,mB.inclinations)
        po_ks = ks_test(mA.positions,mB.positions)

        in_chi_list.append(in_chi)
        po_chi_list.append(po_chi)

        in_ks_list.append(in_ks)
        po_ks_list.append(po_ks)

    np.save(f'data/ks_test/in-different_total_{A_num}_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy', in_ks_list)
    np.save(f'data/ks_test/po-different_total_{A_num}_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy', po_ks_list)



def plot_combined_histograms_custom_yrange(data1, data2, bins=10, sup_title = 'Custom Combined Histograms with Y-axis Limits', labels=('Data 1', 'Data 2'), edge_color='black', y_range=(0, 300)):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    fig.suptitle(sup_title)

    # If bins is an integer, compute the bin edges for uniformity across histograms
    if isinstance(bins, int):
        combined_data = np.concatenate((data1, data2))
        bin_edges = np.linspace(min(combined_data), max(combined_data), bins + 1)
    else:
        bin_edges = bins

    # Plot histograms with specified bin edges and edge color
    axs[0].hist(data1, bins=bin_edges, alpha=0.7, label=labels[0], edgecolor=edge_color)
    axs[0].set_title(labels[0])
    axs[0].set_xlabel('Reduced chi Value')
    axs[0].set_ylabel('Frequency')
    axs[0].set_xticks(bin_edges)
    axs[0].set_ylim(y_range)

    axs[1].hist(data2, bins=bin_edges, alpha=0.7, label=labels[1], color='orange', edgecolor=edge_color)
    axs[1].set_title(labels[1])
    axs[1].set_xlabel('Reduced chi Value')
    axs[1].set_xticks(bin_edges)
    axs[1].set_ylim(y_range)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def test_on_different_total_number_using_scolling_down(test_num,test_id):
    alpha = 0.8

    #test_different_total(test_num,test_id)

    bins_edges = np.linspace(0, 3.5, 15)  # Creates an array from 0 to 10 with 11 points, giving us 10 bins
    range_min = 0.8
    range_max = 1.2

    in_chi_list = np.load(f"data/chi_test/in-different_total_1000_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")
    po_chi_list = np.load(f"data/chi_test/po-different_total_1000_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")

    in_in_range = np.sum((in_chi_list >= range_min) & (in_chi_list <= range_max))
    po_in_range = np.sum((po_chi_list >= range_min) & (po_chi_list <= range_max))
    plot_combined_histograms_custom_yrange(in_chi_list, po_chi_list, bins=bins_edges, sup_title = f"Reduced chi value between 1000 and 1000 stars \nNumber of R-Chi value in range ({range_min}, {range_max}): inclinations:{in_in_range}, positions:{po_in_range}",labels=('inclinations', 'positions'))

    in_chi_list = np.load(f"data/chi_test/in-different_total_500_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")
    po_chi_list = np.load(f"data/chi_test/po-different_total_500_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")

    in_in_range = np.sum((in_chi_list >= range_min) & (in_chi_list <= range_max))
    po_in_range = np.sum((po_chi_list >= range_min) & (po_chi_list <= range_max))
    plot_combined_histograms_custom_yrange(in_chi_list, po_chi_list, bins=bins_edges, sup_title = f"Reduced chi value between 500 and 1000 stars \nNumber of R-Chi value in range ({range_min}, {range_max}): inclinations:{in_in_range}, positions:{po_in_range}",labels=('inclinations', 'positions'))

    in_chi_list = np.load(f"data/chi_test/in-different_total_100_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")
    po_chi_list = np.load(f"data/chi_test/po-different_total_100_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")

    in_in_range = np.sum((in_chi_list >= range_min) & (in_chi_list <= range_max))
    po_in_range = np.sum((po_chi_list >= range_min) & (po_chi_list <= range_max))
    plot_combined_histograms_custom_yrange(in_chi_list, po_chi_list, bins=bins_edges, sup_title = f"Reduced chi value between 100 and 1000 stars \nNumber of R-Chi value in range ({range_min}, {range_max}): inclinations:{in_in_range}, positions:{po_in_range}",labels=('inclinations', 'positions'))
    

def test_on_different_total_number_using_scolling_down(star_num, test_num,test_id = "ks"):
    alpha = 0.8

    in_ks_list = np.load(f"data/ks_test/in-different_total_{star_num}_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")
    po_ks_list = np.load(f"data/ks_test/po-different_total_{star_num}_1000_alpha{alpha}_excepted_{test_num}_test_{test_id}.npy")

    plot_combined_histograms_custom_yrange(in_ks_list, po_ks_list, bins=10, sup_title = f"ks value between {star_num} and 1000 stars",labels=('inclinations', 'positions'),y_range=(0, 100))



if __name__ == "__main__":   
    test_num = 100
    test_id = "ks"

    

    #create_test_data(100,test_num,test_id)
    #create_test_data(500,test_num,test_id)
    #create_test_data(1000,test_num,test_id)

    test_on_different_total_number_using_scolling_down(100, test_num,test_id = "ks")
    test_on_different_total_number_using_scolling_down(500, test_num,test_id = "ks")
    test_on_different_total_number_using_scolling_down(1000, test_num,test_id = "ks")
