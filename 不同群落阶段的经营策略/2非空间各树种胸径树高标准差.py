import os
import pandas as pd
import numpy as np
file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list = os.listdir(file_path)
out_df={'Plot':[],'树种':[],'胸径方差':[],'胸径标准差':[],'树高方差':[],'树高标准差':[]}

a=0
for i in name_list:
    a+=1
    data = os.path.join(file_path, i)
    data = pd.read_excel(data, sheet_name='每木检尺及测高记录表')
    #数据清洗
    data=data.copy()
    data = data[~data['状态'].isin(['枯立木', '倒木'])]
    data = data[(data['树高'] != '无') & (data['树高'] != 0)]
    data= data[(data['胸径'] != '无') & (data['胸径'] != 0)]
    tree_names = list(data['树种'].unique())
    # 数据处理
    for sps in tree_names:
        df = data[data['树种'] == sps].copy()
        for j in ['胸径', '树高']:
            # 计算方差
            variance_diameter = df[f'{j}'].var()
            out_df[f'{j}方差'].append(variance_diameter)
            # 计算标准差
            std_diameter = np.std(df[f'{j}'])
            out_df[f'{j}标准差'].append(std_diameter)
        basename = i.rsplit('.', 1)[0]
        out_df['Plot'].append(basename)
        out_df['树种'].append(sps)



out_df=pd.DataFrame(out_df)
print(out_df)
out_df.to_excel(os.path.join(out_path,'各树种树高胸径标准差.xlsx'))