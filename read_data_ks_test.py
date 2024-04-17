import load_real_data as lrd
import numpy as np
import bf_search
import load_db
import vector_operations as vo
import matplotlib.pyplot as plt

def plot_box_and_bar(array1, array2, array3):
    # 创建一个画布，并设置大小
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 18))
    
    # 设置每个子图的标题
    titles = ['Recovered Alpha', 'Recovered theta', 'Recovered phi']
    
    # 遍历数组和对应的轴（axes）
    for i, data in enumerate([array1, array2, array3]):
        # 箱型图
        axes[i, 0].boxplot(data)
        axes[i, 0].set_title(f'Boxplot of {titles[i]}')
        axes[i, 0].set_ylabel('Value')
        
        # 计算条形图的数据
        # 使用np.histogram计算数据的分布，这里使用10个bins
        counts, bins = np.histogram(data, bins=10)
        # 计算条形的宽度
        width = np.diff(bins)
        # 中心点
        centers = (bins[:-1] + bins[1:]) / 2
        
        # 条形统计图
        axes[i, 1].bar(centers, counts, width=width, edgecolor='black')
        axes[i, 1].set_title(f'Bar plot of {titles[i]}')
        axes[i, 1].set_xlabel('Value')
        axes[i, 1].set_ylabel('Frequency')
    
    # 调整子图间距
    plt.tight_layout()
    plt.show()


# Get the quantities in different bins
def get_bins(hist_data,num_bins):
    hist, _ = np.histogram(hist_data, bins=num_bins)
    return hist


def find_correlation(db_path,file_path):
    # 使用示例
    inclination_dict = lrd.extract_inclination_angles(file_path)
    db_metadata = load_db.get_metaData(db_path)
    
    inclination_angle_list = list(inclination_dict.values())

    inclination_distribution = get_bins(inclination_angle_list,9)

    print(inclination_distribution)

    match_metadata_ids = bf_search.brute_force_search_ks_inclination(inclination_distribution,db_metadata)

    ks_value  = match_metadata_ids[0][0]

    alpha_list = []
    theta_list = []
    phi_list = []

    for item in match_metadata_ids:
        alpha_list.append(item[1].alpha)

        pd = item[1].preferred_direction
        theta,phi = vo.vector_to_angles(pd)
        theta_list.append(theta)
        phi_list.append(phi)

    np.save('data/real/alpha_list.npy',np.array(alpha_list))
    np.save('data/real/theta_list.npy',np.array(theta_list))
    np.save('data/real/phi_list.npy',np.array(phi_list))

def plot_data():
    alpha_list = np.load("data/real/alpha_list.npy")
    theta_list = [180 - angle if angle > 90 else angle for angle in np.load("data/real/theta_list.npy")]
    phi_list = [angle - 180 if angle > 180 else angle for angle in np.load("data/real/phi_list.npy")]


    print(alpha_list)
    print(theta_list)
    print(phi_list)

    plot_box_and_bar(alpha_list, theta_list, phi_list)



if __name__ == "__main__":
    file_path = "IncResults_merged_18mar22_v92.dat"
    db_path = 'data_library_t100_a11_s1000.db'
    #find_correlation(db_path,file_path)

    plot_data()