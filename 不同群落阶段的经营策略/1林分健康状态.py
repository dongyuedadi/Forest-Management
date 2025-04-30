import os
import pandas as pd

file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)

probability_list=[]
plot_list=[]
condition_list=[]
for i in name_list:
    data=os.path.join(file_path,i)
    data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    data['状态']=data['状态'].fillna('正常')
    Condition=data['状态'].unique()
    data_entropy = data['状态']
    total = len(data['状态'])
    for names in Condition:
        count = (data['状态'] == names).sum()
        probability = count / total
        probability_list.append(probability)
        condition_list.append(names)
        basename = i.rsplit('.', 1)[0]
        plot_list.append(basename)

Forest_health=pd.DataFrame()
Forest_health['plot']=plot_list
Forest_health['condition']=condition_list
Forest_health['probability']=probability_list
print(Forest_health)
Forest_health.to_excel(os.path.join(out_path,'林分健康.xlsx'))