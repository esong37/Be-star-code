import numpy as np
import simulation_control as sc
import bf_search
import vector_operations as vo
import time
import matplotlib.pyplot as plt

# get a list of thetas and phis
def theta_phi_recovery(alpha, num, pd, db_metaDatas):
    num_stars = 1000
    viewer = np.array([0,0,0])
    red_chi_range = 100

    num_matched = 3

    # get 100 recover theta and phis
    recover_theta = []
    recover_phi = []

    for i in range(num):
        print(f"-----------alpha: {alpha}, pd: {pd}, location: {i}-------------")
        metaData, stars = sc.do_cylinder_Simulation(num_stars, alpha, viewer, pd, 9)
        matched_ids = bf_search.brute_force_search_matched(metaData.inclinations, metaData.positions, db_metaDatas,red_chi_range)
        # if get nothing recovery, jump over this loop 
        if not len(matched_ids) > 0:
            continue
        count = 0
        for obj in matched_ids: 
            # only get the first best three predicted preferred direction
            if count < num_matched:
                predict_pd = obj[2].preferred_direction
                theta, phi = vo.vector_to_angles(predict_pd)
                if theta > 90: theta = 180 - theta
                if phi > 180: phi = phi - 180
                recover_theta.append(theta) 
                recover_phi.append(phi)

                count += 1

    # 把inclinations 变为0至90
    return recover_theta, recover_phi

# generate a npy file for each alpha test
def create_pd_test_data(db_path):
    num_test_times = 100
    db_metaDatas = bf_search.get_metaData(db_path)


    start_time = time.perf_counter()
    pd = np.random.uniform(-1, 1, 3)

    alpha_array = np.arange(0, 1.05, 0.05)

    theta, phi = vo.vector_to_angles(pd)

    if theta > 90: theta = 180 - theta
    if phi > 180: phi = phi - 180

    np.save(f'data/theta_phi/pd.npy', pd)

    print(f"thetaL: {theta}")
    print(f"phi: {phi}")



    for alpha in alpha_array:
        rec_thetas, rec_phis = theta_phi_recovery(alpha, num_test_times, pd, db_metaDatas)
        np.save(f'data/theta_phi/pd_theta_{alpha:.2f}.npy', rec_thetas)
        np.save(f'data/theta_phi/pd_phi_{alpha:.2f}.npy', rec_phis)

    end_time = time.perf_counter() #####################
    print(f"Execution time each alpha for {num_test_times} times: {end_time - start_time} seconds")

# plot average alpha +- standard error
# plot standard error changing
# plot percentage error changing
def plot_prediction_boxplots(prediction_dict,y_line_value,y_line_label,xlabel,ylabel,title):
    key_value = list(prediction_dict.keys())
    value_list = list(prediction_dict.values())
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(value_list, labels=[str(alpha) for alpha in key_value])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)


    plt.axhline(y=y_line_value, alpha = 0.5,color='r', linestyle='-', label=y_line_label)
    plt.legend(loc='upper right')

    plt.show()



if __name__ == "__main__":
    #db_path = 'data_library_t100_a11_s1000.db'
    #create_pd_test_data(db_path)
    
    pd = np.load(f'data/theta_phi/pd.npy')
    print(pd)


    recovered_thetas = {}
    recovered_phis = {}
    
    pd_theta, pd_phi = vo.vector_to_angles(pd)

    alpha_array = np.arange(0, 1.05, 0.05)
    for alpha in alpha_array:
        rec_thetas = np.load(f'data/theta_phi/pd_theta_{alpha:.2f}.npy')
        rec_phis = np.load(f'data/theta_phi/pd_phi_{alpha:.2f}.npy')
        alpha = round(alpha,2)
        recovered_thetas[alpha] = rec_thetas
        recovered_phis[alpha] = rec_phis


    plot_prediction_boxplots(recovered_thetas,pd_theta,"preferred direction theta","Alpha Value","Recovered theta value",f"Recovered theta for Different Apha\n preferred direction theta: {round(pd_theta,2)}, phi: {round(pd_phi,2)}")
    plot_prediction_boxplots(recovered_phis,pd_phi,"preferred direction phi","Alpha Value","Recovered phi value",f"Recovered phi for Different Apha\n preferred direction theta: {round(pd_theta,2)}, phi: {round(pd_phi,2)}")
    

    



