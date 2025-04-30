import pandas as pd
import numpy as np
import sympy as sp

data_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\东北东部山区蓄积方程参数.xlsx'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\蓄积导数公式.xlsx'
data=pd.read_excel(data_path,sheet_name='黑龙江省（哑变量）')
out_pd=pd.DataFrame()
stand=[]
district=[]
volume_list=[]
Derivative_list=[]
for i in data['林分类型'].unique():
    df=data[data['林分类型']==i]
    for j in df['区域'].unique():
        df_vol=df[df['区域']==j]

        a0=df_vol['a0'].values[0]
        a1=df_vol['a1'].values[0]
        k0=df_vol['k0'].values[0]
        k1=df_vol['k1'].values[0]
        c=df_vol['c'].values[0]
        d0=df_vol['d0'].values[0]
        d1=df_vol['d1'].values[0]
        VOL= f'({a0} * (SCI** {a1}) * (1 - np.exp((-{k0}) * ((SDI / 10000) ** {k1}) * t)) ** {c})* TH* ({d0} / (TH+ {d1}))'
        # 定义符号变量
        SCI, SDI, TH, t = sp.symbols('SCI SDI TH t')
        # 定义函数，注意使用sp.exp而不是np.exp
        f =(a0 * (SCI** a1) * (1 - sp.exp((-k0) * ((SDI / 10000) ** k1) * t)) ** c)* TH* (d0 / (TH+ d1))
        # 求导
        df_dt = sp.diff(f, t)
        volume_list.append(VOL)
        stand.append(i)
        district.append(j)
        Derivative_list.append(df_dt)

out_pd['林分类型']=stand
out_pd['区域']=district
out_pd['蓄积公式']=volume_list
out_pd['导数']=Derivative_list
out_pd.to_excel(out_path)
