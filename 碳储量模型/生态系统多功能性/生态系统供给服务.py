import pandas as pd
import os
import numpy as np

# 读取数据
file_path = r"C:\Users\hys5637428\Desktop\模型拟合"
index_file = os.path.join(file_path, '使用数据(1).xls')
production_max=45
volum_max=338
# 加载Excel文件到DataFrame
data_index = pd.read_excel(index_file,sheet_name='Sheet2')
def calculate_multifunctionality_index(data_index, stage):
    # 筛选数据
    production_max=data_index['生物量'].max()
    data = data_index[data_index['判别式2分组'] == stage]
    production_value =np.mean( data['生物量增量'] / production_max)
    print(f'演替阶段{stage}生产力、木材生产力:',production_value)
    mvolum=data['m活']
    volum = np.mean(mvolum)
    volum_value =1- (volum_max - volum) / volum_max
    print(volum_value)

for stage in [1, 2, 3]:
    calculate_multifunctionality_index(data_index, stage)


