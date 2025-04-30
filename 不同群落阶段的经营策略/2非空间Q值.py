import os
import pandas as pd
import numpy as np
file_path=r"C:\\Users\\hys5637428\\Desktop\\不同阶段经营模式\\path"
name_list=os.listdir(file_path)

a=0
Q_list=[]
Q={'样地':[],'Q值':[]}
for i in name_list:
    a+=1
    data=os.path.join(file_path,i)
    data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    #数据清洗
    data=data.copy()
    data = data[~data['状态'].isin(['枯立木', '倒木'])]
    if data.empty:
        print("DataFrame 是空的")
    elif data['胸径'].isnull().all():
        print("'胸径' 列全是空的或 NaN 值")
    else:
        maxvalue = max(data['胸径'])
        maxvalue = int(maxvalue)
    data.drop_duplicates()
    #数据处理
    df = data.copy()
    listBins = list(range(5, maxvalue + 2, 2))
    listLabels = list(range(6, maxvalue + 1, 2))
    df['径阶'] = None
    df['径阶'] = pd.cut(df['胸径'], bins=listBins, labels=listLabels, include_lowest=True)
    unique_Bins = list(np.unique(df['径阶']))
    unique_Bins_len = len(unique_Bins)
    for j in range(0, unique_Bins_len - 1):
        k = j + 1
        j = unique_Bins[j]
        k = unique_Bins[k]
        if len(df[df['径阶'] == k])>0:
            q = len(df[df['径阶'] == j]) / len(df[df['径阶'] == k])
            Q_list.append(round(q, 2))

    basename = i.rsplit('.', 1)[0]
    Q['Q值'].append(np.mean(Q_list))
    Q['样地'].append(basename)
Q = pd.DataFrame(Q)
print(Q)
file_out=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
Q.to_excel(os.path.join(file_out,'Q值.xlsx'),index=False)