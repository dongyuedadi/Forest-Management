import pandas as pd
import os
import numpy as np

# 读取数据
file_path = r"C:\Users\hys5637428\Desktop\模型拟合"
index_file = os.path.join(file_path, '使用数据(1).xls')
# 加载Excel文件到DataFrame
data_index = pd.read_excel(index_file,sheet_name='Sheet2')
def quantify_slope(slope):
    if slope < 5:
        return 3
    elif 5 <= slope < 15:
        return 2
    elif 15 <= slope < 25:
        return 1
    else:  # slope >= 25
        return 0.5
# 定义坡向量化的函数
def quantify_aspect(aspect):
    aspect_map = {
        '北': 3,
        '东北': 2.5,
        '西北': 2.5,
        '无坡向': 2,
        '东南': 1.5,
        '西南': 1.5,
        '南': 1
    }
    return aspect_map.get(aspect, np.nan)  # 如果aspect不在映射中，返回NaN（可以根据需要处理）
# 应用量化函数并生成新列
data_index['坡度量化值'] = data_index['坡度'].apply(quantify_slope)
data_index['坡向量化值'] = data_index['坡向'].apply(quantify_aspect)
vary_name=['树高', '胸径', '生物量', '林分密度', '草本平均高', '灌木平均高', '林分平均高', '植被总盖度', '腐殖质层厚度',  '落叶厚度','坡度量化值','坡向量化值','枯立木蓄积']
vary_value=['平均树高', '平均直径', '生物量', '株数', '草本平均高', '灌木平均高', '平均树高', '植被总覆盖', '腐殖层厚度',  '枯枝叶厚度','坡度量化值','坡向量化值','m枯']
vary_max=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12]
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12]:
    j = vary_value[i]
    vary_max[i]=data_index[f'{j}'].max()
def calculate_multifunctionality_index(data_index, stage):
    # 筛选数据
    data = data_index[data_index['判别式2分组'] == stage]
    for i in [0,1,2,3,4,5,6,7,8,9,10,11,12]:
        j=vary_value[i]
        k=vary_name[i]
        carbon = np.mean(data[f'{j}'])
        volum_value = 1-(vary_max[i] - carbon) / vary_max[i]
        print(f'演替阶段{stage}{vary_name[i]}:', volum_value)

for stage in [1, 2, 3]:
    calculate_multifunctionality_index(data_index, stage)
    diversity_data_index=data_index[data_index['判别式2分组'] == stage]
    simpson=diversity_data_index['simpson'].mean()
    print('simpon:',simpson)



