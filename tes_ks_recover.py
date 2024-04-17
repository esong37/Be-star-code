import numpy as np
import simulation_control as sc
import load_db
import bf_search as bf
import vector_operations as vo
import time
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  

# ks for single alpha
def ks_single_alpha_test(db_metadatas,alpha,test_num,num_matched):
    star_num = 1000
    viewer = np.array([0,0,0])

    recovery_theta_list = []
    recovery_phi_list = []
    recover_alpha_list = []

    pd = np.random.uniform(-1,1,3) # random preferred direction
    for i in range(test_num):
        
        metaData, _ = sc.do_cylinder_Simulation(star_num,alpha,viewer,pd,9)
        theta, phi = vo.vector_to_angles(pd)
        print(f"\n\n---------------alpha: {alpha} | {i} | pd: theta({round(theta,4)}), phi({(round(phi,4))})--------------")

        match_ids = bf.brute_force_search_ks(metaData.inclinations,metaData.positions, db_metadatas)[:num_matched]

        
        for obj in match_ids: 
            recover_alpha_list.append(obj[2].alpha)

            m_pd = obj[2].preferred_direction
            theta, phi = vo.vector_to_angles(m_pd)

            recovery_theta_list.append(theta)
            recovery_phi_list.append(phi)


    alpha_file_path = f"data/ks_recovery_test/alpha/alpha-alpha_{alpha}_t{test_num}_m{num_matched}.npy"
    theta_file_path = f"data/ks_recovery_test/theta/theta-alpha_{alpha}_t{test_num}_m{num_matched}.npy"
    phi_file_path = f"data/ks_recovery_test/phi/phi-alpha_{alpha}_t{test_num}_m{num_matched}.npy"
    pd_file_path = f"data/ks_recovery_test/pd/pd-alpha_{alpha}_t{test_num}_m{num_matched}.npy"
    np.save(alpha_file_path,recover_alpha_list)
    np.save(theta_file_path,recovery_theta_list)
    np.save(phi_file_path,recovery_phi_list)
    np.save(pd_file_path,pd)


def generate_ks_recovery_test_data(alpha_list, test_num,num_matched_each_search):

    db_path = 'data_library_t100_a11_s1000.db'
    db_metadatas = load_db.get_metaData(db_path)

    for alpha in alpha_list:
        ks_single_alpha_test(db_metadatas,alpha,test_num,num_matched_each_search)



def load_ks_data_file(alpha_list,test_num,num_matched):
    alpha_dic = {}
    theta_dic = {}
    phi_dic = {}
    pd_dic = {}


    for alpha in alpha_list:
        alpha  = round(alpha,2)
        

        alpha_file_path = f"data/ks_recovery_test/alpha/alpha-alpha_{alpha}_t{test_num}_m{num_matched}.npy"
        theta_file_path = f"data/ks_recovery_test/theta/theta-alpha_{alpha}_t{test_num}_m{num_matched}.npy"
        phi_file_path = f"data/ks_recovery_test/phi/phi-alpha_{alpha}_t{test_num}_m{num_matched}.npy"
        pd_file_path = f"data/ks_recovery_test/pd/pd-alpha_{alpha}_t{test_num}_m{num_matched}.npy"

        alpha_dic[alpha] = np.load(alpha_file_path)
        theta_dic[alpha] = [180 - angle if angle > 90 else angle for angle in np.load(theta_file_path)]
        phi_dic[alpha] = [angle - 180 if angle > 180 else angle for angle in np.load(phi_file_path)]
        pd_dic[alpha] = np.load(pd_file_path)

    return alpha_dic, theta_dic,phi_dic,pd_dic


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

# plot average alpha +- standard error
# plot standard error changing
# plot percentage error changing
def plot_prediction_boxplots_with_value(prediction_dict, value,title):
    alpha_values = list(prediction_dict.keys())
    prediction_lists = list(prediction_dict.values())
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(prediction_lists, labels=[str(alpha) for alpha in alpha_values])
    
    # 绘制每个期望值的红色横线
    for alpha, y_value in value.items():
        if alpha in alpha_values:
            x_index = alpha_values.index(alpha) + 1  # +1 因为boxplot的索引从1开始
            plt.hlines(y_value, x_index - 0.25, x_index + 0.25, colors='red', linestyles='solid', linewidth=1)
    
    plt.xlabel('Alpha')
    plt.ylabel(f'Recovered {title} value')
    plt.title(f'Recovered {title} for Different Alpha')
    plt.grid(True)
    
    # 在图的右上角加上角标说明
    legend_line = Line2D([0], [0], color='red', lw=2)
    plt.legend([legend_line],[f'Expected {title} value'], loc='upper right')
    
    plt.show()


def do_KS_test(alpha_dic, theta_dic,phi_dic,pd_dic):

    alpha_list = list(alpha_dic.keys())

    #plot_prediction_boxplots(alpha_dic) # recovered alpha value

    theta_value = {}
    phi_value = {}

    for alpha in list(pd_dic.keys()):
        theta,phi = vo.vector_to_angles(pd_dic[alpha])
        theta_value[alpha] = 180 - theta if theta > 90 else theta
        phi_value[alpha] = phi - 180 if phi > 180 else phi

    plot_prediction_boxplots_with_value(theta_dic,theta_value,"theta")
    plot_prediction_boxplots_with_value(phi_dic,phi_value,"phi")

        
if __name__ == "__main__":
    # alpha = 0.4 done!
    alpha_list = np.array([0.4,0.6,0.8])
    start_time = time.perf_counter()

    test_num = 20 # test n times for each alpha
    num_matched = 5 # find the first n matched data

    #generate_ks_recovery_test_data(alpha_list, test_num,num_matched)
    alpha_dic, theta_dic,phi_dic,pd_dic = load_ks_data_file(alpha_list,test_num,num_matched)
    do_KS_test(alpha_dic, theta_dic,phi_dic,pd_dic)

    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time} seconds")

