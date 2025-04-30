import os
import pandas as pd
import numpy as np
file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list = os.listdir(file_path)
out_df={'plot':[],'灌木盖度':[],'灌木平均高':[],'株树密度':[]}

a=0
for i in name_list:
    a+=1
    data = os.path.join(file_path, i)
    data = pd.read_excel(data, sheet_name='植被（灌木）调查表')
    #数据清洗
    data=data.copy()
    # 使用 & 运算符来组合两个条件，确保两行代码都满足时才保留该行
    data = data.dropna(subset=['盖度（%）', '平均高（cm）'])
    data = data.dropna(how='all')
    basename = i.rsplit('.', 1)[0]
    out_df['plot'].append(basename)
    Shrubcover=np.sum(data['盖度（%）'])/100
    out_df['灌木盖度'].append(Shrubcover)
    Shrubheight=np.sum(data['平均高（cm）'])/100
    out_df['灌木平均高'].append(Shrubheight)
    Stand_density = np.sum(data['株数'])
    out_df['株树密度'].append(Stand_density)

out_df=pd.DataFrame(out_df)
print(out_df)
out_df.to_excel(os.path.join(out_path,'灌木盖度.xlsx'))