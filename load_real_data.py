
def extract_inclination_angles(file_path):
    # 初始化一个空字典来存储id和inclination angle的映射
    inclination_dict = {}

    # 尝试打开文件并读取内容
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # 使用split()函数分割每行的数据
                parts = line.split()

                # 检查是否有足够的列（至少5列）
                if len(parts) >= 5:
                    # 提取id（第一列）和inclination angle（第五列）
                    # 并将它们转换为适当的类型（id为整数，inclination angle为浮点数）
                    id = int(parts[0])
                    inclination_angle = float(parts[4])

                    # 将这对值存储到字典中
                    inclination_dict[id] = inclination_angle
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 返回填充好的字典
    return inclination_dict


