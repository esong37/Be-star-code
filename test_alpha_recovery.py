import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import simulation_control as sc
import bf_search
import time
import load_db

# random stars, random preferred direction, test recover alpha value
def single_alpha_recover(alpha,num_test,meta_data_list,num_matched = 3,num_stars=1000):

    viewer = np.array([0,0,0])
    reduced_chi_range = 100
    recover_alphas = []

    # for each alpha reocver, do 100 times to calculate standard error
    for i in range(num_test):
        print(f"location: {alpha}_{i}")
        preferred_direction = np.random.uniform(-1, 1, 3)
        metaData, stars_ = sc.do_cylinder_Simulation(num_stars,alpha, viewer, preferred_direction, 9)

        match_ids = bf_search.brute_force_search_matched(metaData.inclinations,metaData.positions,meta_data_list,reduced_chi_range)
        # if get nothing recovery, jump over this loop 
        if not len(match_ids) > 0:
            continue
        recover_alpha_list = []
        for obj in match_ids: 
            # only get the first three alpha
            if len(recover_alpha_list) < num_matched:
                recover_alpha_list.append(obj[2].alpha)

        # get the average of first three
        recover_alphas.append(np.mean(recover_alpha_list))
    return np.array(recover_alphas)

# generate a npy file for each alpha test
def create_alpha_test_data(test_num,db_path):
    """
    100: 380s
    """
    
    meta_data_list = load_db.get_metaData(db_path)

    start_time = time.perf_counter()
    alpha_array = np.arange(0, 1.05, 0.05)
    for alpha in alpha_array:
        recover_alphas = single_alpha_recover(alpha,test_num,meta_data_list,num_matched = 3,num_stars=1000)
        np.save(f'data/alphas/alpha_{alpha:.2f}.npy', recover_alphas)

    end_time = time.perf_counter() #####################
    print(f"Execution time each alpha for {test_num} times: {end_time - start_time} seconds")


# read and get all alpha data {alpha: [all predicted alpha value]}
def get_all_alpha_data():
    alpha_array = np.arange(0.0,1.05,0.05)

    all_alpha_data = {}


    for alpha in alpha_array:
        all_alpha_data[round(alpha,2)] = np.load(f"data/alphas/alpha_{alpha:.2f}.npy")

    return all_alpha_data

# calculate standard error for each alpha
def get_standard_error(array):
    standard_deviation = np.std(array, ddof=1)
    sample_size = len(array)
    # Standard Error
    SE = standard_deviation / np.sqrt(sample_size)
    return SE

# calculate the mean square error and mean average error for each alpha
def MSE_MAE(alpha, alpha_data):
    alpha_array = np.array(alpha_data)
    n = len(alpha_array)
    # MAE
    mae = np.abs(alpha_array - alpha).mean()
    # MSE
    mse = ((alpha_array - alpha) ** 2).mean()
    return mae, mse

# plot average alpha +- standard error
# plot standard error changing
# plot percentage error changing
def plot_prediction_boxplots(prediction_dict):
    alpha_values = list(prediction_dict.keys())
    prediction_lists = list(prediction_dict.values())
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(prediction_lists, labels=[str(alpha) for alpha in alpha_values])
    plt.xlabel('Alpha')
    plt.ylabel('Recovered alpha value')
    plt.title('Recovered Boxplots for Different Apha')
    plt.grid(True)
    plt.show()

# Plots the alpha values and their standard deviations for all predicted values in a dictionary.
def plot_alpha_standard_deviation(prediction_dict):
    alpha_values = list(prediction_dict.keys())
    standard_erros = []
    mean_alpha = []
    percent_errors = []

    for alpha, predictions in prediction_dict.items():
        sd = get_standard_error(predictions)
        standard_erros.append(sd)
        mean_alpha.append(np.mean(np.array(predictions)))
        percent_errors.append(sd/alpha)
        print(sd)
    plt.figure(figsize=(10, 6))
    plt.errorbar(alpha_values, mean_alpha, yerr=standard_erros, ecolor='r', capsize=5, linestyle='-', color='b')
    plt.xlabel('Alpha')
    plt.ylabel('Mean Alpha Value')
    plt.title('Mean Alpha Value ± Standard Error')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.errorbar(alpha_values, standard_erros, capsize=5, linestyle='-', color='b')
    plt.xlabel('Alpha')
    plt.ylabel('Standard Error')
    plt.title('Variation of Standard Error with Alpha value')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.errorbar(alpha_values, percent_errors, capsize=5, linestyle='-', color='b')
    plt.xlabel('Alpha')
    plt.ylabel('Percent Error')
    plt.title('Variation of Percent Error with Alpha value')
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    db_path = 'data_library_t100_a11_s1000.db'
    test_num = 100 # do 100 test for each alpha

    # create data set and store in folder
    create_alpha_test_data(test_num,db_path)

    # get all data from data folder
    prediction_dict = get_all_alpha_data()

    # display the first three graph
    plot_alpha_standard_deviation(prediction_dict)

    # display the box plot
    plot_prediction_boxplots(prediction_dict)
