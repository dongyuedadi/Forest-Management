import os
import pandas as pd
import numpy as np
file_path=r"C:\\Users\\hys5637428\\Desktop\\帽儿山蘑菇调查\\path"
name_list=os.listdir(file_path)

a=0
Q={'name':[],'样地':[],'径阶':[],'Q值':[]}
for i in name_list:
    a+=1
    data=os.path.join(file_path,i)
    data=pd.read_excel(data,sheet_name='检尺')
    #数据清洗
    data=data.copy()
    if data.empty:
        print("DataFrame 是空的")
    elif data['胸径'].isnull().all():
        print("'胸径' 列全是空的或 NaN 值")
    else:
        maxvalue = max(data['胸径'])
        maxvalue = int(maxvalue)
    data.dropna(subset=['树高'], inplace=True)
    data = data[data['树高'] != 0]
    data.drop_duplicates()
    #数据处理
    plotname=data['样地'].unique()

    for nm in plotname:
        df=data.copy()
        df=df[df['样地']==nm]
        listBins=[0,1]+list(range(3,maxvalue+2,2))
        listLabels=list(range(0,maxvalue+1,2))
        df['径阶']=None
        df['径阶']=pd.cut(df['胸径'],bins=listBins,labels=listLabels,include_lowest=True)
        unique_Bins=list(np.unique(df['径阶']))
        unique_Bins_len=len(unique_Bins)
        for j in range(0,unique_Bins_len-1):
            k=j+1
            j=unique_Bins[j]
            k=unique_Bins[k]
            q = len(df[df['径阶'] == j])/ len(df[df['径阶'] == k])
            Q['径阶'].append(j)
            Q['Q值'].append(round(q, 2))
            Q['样地'].append(round(nm, 0))
            basename = i.rsplit('.', 1)[0]
            Q['name'].append(basename)

Q = pd.DataFrame(Q)
file_out=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
Q.to_excel(os.path.join(file_out,'Q值.xlsx'),index=False)