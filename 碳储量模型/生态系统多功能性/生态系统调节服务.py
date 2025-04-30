import pandas as pd
import os
import numpy as np

# 读取数据
# 读取数据
file_path = r"C:\Users\hys5637428\Desktop\模型拟合"
index_file = os.path.join(file_path, '使用数据(1).xls')
# 加载Excel文件到DataFrame
data_index = pd.read_excel(index_file,sheet_name='Sheet2')
vary_name = ['碳储量', '枯枝叶厚度', '腐殖层厚度', '草本盖度', '灌木盖度', '林分密度']
vary_value = ['碳储量', '枯枝叶厚度', '腐殖层厚度', '草本覆盖度', '灌木覆盖度', '株数']
vary_max=[0, 1, 2, 3, 4, 5]
for i in [0, 1, 2, 3, 4, 5]:
    j = vary_value[i]
    vary_max[i]=data_index[f'{j}'].max()

def calculate_multifunctionality_index(data_index, stage):
    # 筛选数据
    production_max=data_index['碳储量'].max()
    data = data_index[data_index['判别式2分组'] == stage]
    production_value =np.mean( data['碳储量增量'] / production_max)
    print(f'演替阶段{stage}植被固碳量:',production_value)
    for i in [0,1,2,3,4,5]:
        j=vary_value[i]
        k=vary_name[i]
        carbon = np.mean(data[f'{j}'])
        volum_value = 1-(vary_max[i] - carbon) / vary_max[i]
        print(f'演替阶段{stage}{vary_name[i]}:', volum_value)

for stage in [1, 2, 3]:
    calculate_multifunctionality_index(data_index, stage)




