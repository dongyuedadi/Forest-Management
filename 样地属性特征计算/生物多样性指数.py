import pandas
import pandas as pd
import numpy as np
import os
file_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\path'
out_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out2'
namelist=os.listdir(file_path)

dict_df1={'plot':[],'树种':[],'数量':[]}

for i in namelist:
    file=os.path.join(file_path,i)
    df=pd.read_excel(file)
    tree_names=list(df['树种'].unique())
    for j in tree_names:
        num=len(df.loc[df['树种']==j])
        dict_df1['plot'].append(i)
        dict_df1["树种"].append(j)
        dict_df1['数量'].append(num)
out_df1=pd.DataFrame(dict_df1)
dict_df={'plot':[],'shannon':[],'simpson':[],'pielou_shannon':[],'pielou_simpson':[]}
for i in out_df1['plot'].unique():
    clip=out_df1[out_df1['plot']==i]
    tree_list=clip['树种'].unique()
    dict_df['plot'].append(i)

    H=[]
    D=[]
    for j in tree_list:
        N=np.sum(clip['数量'].values)
        S=len(np.unique(clip['树种']))
        n=np.sum(clip[clip['树种']==j]['数量'].values)
        pi=n/N
        h=pi*np.log(pi)
        H.append(h)
        d=pi*pi
        D.append(d)
    shannon=-np.sum(H)
    simpson=1-np.sum(D)
    pieloush=shannon/np.log(S)
    pielou_simpson=simpson/(1-1/S)
    dict_df['shannon'].append(shannon)
    dict_df['simpson'].append(simpson)
    dict_df['pielou_shannon'].append(pieloush)
    dict_df['pielou_simpson'].append(pielou_simpson)

data=pd.DataFrame(dict_df)
data.to_excel(os.path.join(out_path,'diversity.xlsx'))

