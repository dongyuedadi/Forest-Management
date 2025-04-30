import os
import pandas as pd
import numpy as np

# 定义文件路径
file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list = os.listdir(file_path)

# 初始化存储结果的列表
results = []

# 定义计算多样性指数的函数
def calculate_diversity_indices(probability, S):
    shannon_index = -np.sum(probability * np.log(probability))
    simpson_index = 1 - np.sum((probability / np.sum(probability)) ** 2)
    pielou_shannon = shannon_index / np.log(S)
    pielou_simpson = simpson_index / (1 - 1 / S)
    return shannon_index, simpson_index, pielou_shannon, pielou_simpson

# 遍历每个文件
for file_name in name_list:
    file_path_full = os.path.join(file_path, file_name)
    plot_name = file_name.rsplit('.', 1)[0]  # 获取文件名（去掉扩展名）

    # 读取灌木和草本数据
    shrubs_data = pd.read_excel(file_path_full, sheet_name='植被（灌木）调查表')
    herbs_data = pd.read_excel(file_path_full, sheet_name='植被（草本）调查表')

    # 去除空值
    shrubs_data.dropna(subset=['种名'], inplace=True)
    herbs_data.dropna(subset=['种名'], inplace=True)

    # 计算灌木多样性
    shrubs_species = shrubs_data['种名'].unique()
    total_samples = 10 * 10 * 5  # 假设每个样方有10x10个样点，每个样点5个样本
    for species in shrubs_species:
        count = (shrubs_data['种名'] == species).sum()
        probability = count / total_samples
        results.append({
            'plot': plot_name,
            'Categorization': 'Shrubs',
            '种名': species,
            '频率': probability
        })

    # 计算草本多样性
    herbs_species = herbs_data['种名'].unique()
    for species in herbs_species:
        count = (herbs_data['种名'] == species).sum()
        probability = count / total_samples
        results.append({
            'plot': plot_name,
            'Categorization': 'Herbs',
            '种名': species,
            '频率': probability
        })

# 将结果转换为DataFrame
results_df = pd.DataFrame(results)

# 计算多样性指数
def calculate_diversity_indices(group):
    S = len(group['种名'].unique())  # 当前分类的物种数
    probability = group['频率']
    shannon_index = -np.sum(probability * np.log(probability))
    simpson_index = 1 - np.sum((probability / np.sum(probability)) ** 2)
    pielou_shannon = shannon_index / np.log(S)
    pielou_simpson = simpson_index / (1 - 1 / S)
    return pd.Series({
        'shannon_index': shannon_index,
        'simpson_index': simpson_index,
        'pielou_shannon': pielou_shannon,
        'pielou_simpson': pielou_simpson
    })

# 分组计算多样性指数
diversity_indices = results_df.groupby(['plot', 'Categorization']).apply(calculate_diversity_indices).reset_index()


# 计算总的多样性指数（基于所有物种）
total_S = len(results_df['种名'].unique())  # 总的物种数
total_grouped = results_df.groupby('plot')['频率']
results_df['sum_shannon_index'] = total_grouped.transform(lambda x: -np.sum(x * np.log(x)))
results_df['sum_simpson_index'] = total_grouped.transform(lambda x: 1 - np.sum((x / np.sum(x)) ** 2))
results_df['sum_pielou_shannon'] = total_grouped.transform(lambda x: (-np.sum(x * np.log(x))) / np.log(total_S))
results_df['sum_pielou_simpson'] = total_grouped.transform(lambda x: (1 - np.sum((x / np.sum(x)) ** 2)) / (1 - 1 / total_S))
# 合并多样性指数到原始数据
results_df = results_df.merge(diversity_indices, on=['plot', 'Categorization'], how='left')
# 去重并保存结果
unique_results = results_df.drop_duplicates(subset=['plot', 'Categorization'])
unique_results.to_excel(os.path.join(out_path, '多样性指数α多样性.xlsx'), index=False)

# 打印结果
print(unique_results.tail(3))