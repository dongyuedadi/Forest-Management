import pandas as pd
import numpy as np

data_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\材积表.xlsx'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\公式.xlsx'
data=pd.read_excel(data_path)
data=data.fillna(0)
out_pd=pd.DataFrame()
district=[]
sps_list=[]
volume_list=[]
Height_list=[]
Ship_list=[]
for i in data['地区'].unique():
    df=data[data['地区']==i]
    for j in df['序号'].unique():
        df_vol=df[df['序号']==j]
        district.append(i)
        sps=df_vol['树种'].values[0]
        sps_list.append(sps)
        a1=df_vol['a1'].values[0]
        b1=df_vol['b1'].values[0]
        c1=df_vol['c1'].values[0]
        a2=df_vol['a2'].values[0]
        b2=df_vol['b2'].values[0]
        a3=df_vol['a3'].values[0]
        b3=df_vol['b3'].values[0]
        if c1!=0:
            volume=f'V={a1}*D^{b1}*H^{c1}'
        else:
            volume=f'V={a1}*D^{b1}'
        if a2!=0:
            Height=f'H=1.3+{a2}*exp(-{b2}/D)'
        else:
            Height='无'
        if a3!=0:
            Ship=f'{a3}+{b3}*D围'
        else:
            Ship='无'
        volume_list.append(volume)
        Height_list.append(Height)
        Ship_list.append(Ship)
out_pd['地区']=district
out_pd['树种']=sps_list
out_pd['材积公式']=volume_list
out_pd['树高曲线']=Height_list
out_pd['轮围']=Ship_list
out_pd.to_excel(out_path)