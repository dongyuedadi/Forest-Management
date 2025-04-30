import os
import pandas as pd
import numpy as np

file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list = os.listdir(file_path)

# 初始化一个空的列表来存储每个文件的DataFrame
all_data_frames = []
for file_name in name_list:
    data_path = os.path.join(file_path, file_name)
    data = pd.read_excel(data_path, sheet_name='30cm以下幼树幼苗')
    # 清洗数据，移除'树种'列为'无'且'株树'为0的行
    df = data[(data['树种'] != '无') & (data['株树'] != 0)]
    # 计算各树种的株树总和
    tree_counts = df.groupby('树种')['株树'].sum().to_dict()
    # 计算总数
    total_count = sum(tree_counts.values())
    # 计算并构建各树种所占比例的字典
    tree_proportions = {species: count / total_count for species, count in tree_counts.items()}
    # 创建一个DataFrame来存储当前文件的结果
    temp_df = pd.DataFrame.from_dict(tree_counts, orient='index', columns=['树种株树和'])
    #orient='index'：这个参数指定字典的键应该用作DataFrame的索引（行标签），而字典的值则填充到指定的列中
    temp_df['树种比例'] = temp_df.index.map(tree_proportions)
    #map(tree_proportions)：map函数用于将索引（树种名称）映射到tree_proportions字典中相应的值（树种比例）。这样，每个树种都会得到一个与之对应的比例值
    basename = file_name.rsplit('.', 1)[0]
    temp_df['plot'] = basename
    temp_df.reset_index(inplace=True)  # 将索引重置为列，索引现在变为'树种'
    temp_df.rename(columns={'index': '树种'}, inplace=True)  # 将列名'index'改为'树种'
    # 将当前文件的DataFrame添加到列表中
    all_data_frames.append(temp_df)
# 使用pd.concat合并所有DataFrame
final_df = pd.concat(all_data_frames, ignore_index=True)
# 打印输出或保存到文件
print(final_df)
final_df.to_excel(os.path.join(out_path, '30cm以下株树比例.xlsx'), index=False)
