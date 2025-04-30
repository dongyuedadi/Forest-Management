def Pinus_koraiensis(D):#红松材积
    H= 1.3 + 30.09177 * np.exp(-16.3698 / D)
    Dw= -0.08197754 + 1.00135 * D
    v=6.3527721e-05 * Dw ** 1.9435455 * H ** 0.89689361
    return v
def Picea(D):#云杉
    H = 1.3 + 32.21942 * np.exp(-17.06452 / D)
    Dw = -0.03871096 + 0.9971613 * D
    v=6.1859978e-05 * Dw ** 1.85577513 * H ** 1.0070547
    return v

def Abies(D):#冷杉
    H=1.3+30.63747*np.exp(-14.82347/D)
    Dw=-0.08269092+0.998732*D
    v=6.1859978e-05*Dw**1.85577513*H**1.0070547
    return v
def Larix(D):#落叶松
    v = 0.0006576508 * D** 2.018535
    return v
def Fraxinus(D):#水曲柳
    H=1.3+24.84302*np.exp(-10.26841/D)
    Dw=-0.1340759+0.9904621*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Juglans (D):#胡桃楸
    H = 1.3 + 24.84302 * np.exp(-10.26841 / D)
    Dw = -0.1340759 + 0.9904621 * D
    v = 4.1960698e-05 * Dw ** 1.9094595 * H ** 1.0413892
    return v
def Phellodendron(D):#黄菠萝
    H = 1.3 + 24.84302 * np.exp(-10.26841 / D)
    Dw = -0.1340759 + 0.9904621 * D
    v = 4.1960698e-05 * Dw ** 1.9094595 * H ** 1.0413892
    return v
def Tilia (D):#紫椴
    H=1.3+23.83062*np.exp(-11.08188/D)
    Dw=-0.3178201+0.993646*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Juglans (D):#色木槭
    H = 1.3 + 19.66254 * np.exp(-8.601885 / D)
    Dw = -0.1948627 + 0.9913445 * D
    v = 4.1960698e-05 * Dw ** 1.9094595 * H ** 1.0413892
    return v
def Ulmus (D):#榆树
    H=1.3+24.17011*np.exp(-12.04452/D)
    Dw=-0.09734+0.9870044*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Quercus (D):#蒙古栎
    H=1.3+17.75595*np.exp(-7.737241/D)
    Dw=0.2083972+0.9771802*D
    v=6.1125534e-05*Dw**1.8810091*H**0.94462565
    return v
def Betula_costata (D):#枫桦
    H=1.3+24.01214*np.exp(-8.630002/D)
    Dw=-0.1172836+0.9899376*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Betula_davurica (D):#黑桦
    H=1.3+20.4484*np.exp(-8.399443/D)
    Dw=0.02539258+0.9797975*D
    v=5.2786451e-05*Dw**1.7947313*H**1.0712623
    return v
def Betula_platyphylla (D):#白桦
    H=1.3+26.4656*np.exp(-8.740813/D)
    Dw=-0.1689837+1.006111*D
    v=5.1935163e-05*Dw**1.8586884*H**1.0038941
    return v
def Populus_davidiana (D):#山杨
    H=1.3+27.60532*np.exp(-9.567569/D)
    Dw=-0.2641493+1.009529*D
    v=5.3474319e-05*Dw**1.8778994*H**0.99982785
    return v
def Populus(D):#大青杨
    H=1.3+26.51351*np.exp(-10.29054/D)
    Dw=-0.02728948+0.990946*D
    v=5.3474319e-05*Dw**1.8778994*H**0.99982785
    return v
def broadleaf(D):#杂木材积？？？
    Dw=-0.41226+0.97241*D
    H=25.791498-378.521967/(Dw+17)
    v=0.00004331*Dw**1.73738556*H**1.22688346
    return v

import os
import pandas as pd
import numpy as np
file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)

out_df={'Plot':[],'树种':[],'径阶':[],'径阶蓄积':[]}
a=0
for i in name_list:
    a+=1
    data=os.path.join(file_path,i)
    data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    #数据清洗
    data=data.copy()
    data = data[~data['状态'].isin(['枯立木', '倒木'])]
    if data['胸径'].isnull().all():
        print("'胸径' 列全是空的或 NaN 值")
    else:
        maxvalue = max(data['胸径'])
        maxvalue = int(maxvalue)+1

    if __name__=='__main__':
        df = data.copy()
        listBins = list(range(5, maxvalue + 4, 4))
        listLabels = list(range(7, maxvalue + 2, 4))
        df['径阶'] = pd.cut(df['胸径'], bins=listBins, labels=listLabels, include_lowest=True)
        df.dropna(subset='径阶', inplace=True)
        tree_names=list(df['树种'].unique())
        print(tree_names)
        b=0
        for tree_name in tree_names:
            b+=1
            df_sps = df[df['树种'] ==tree_name].copy()
            area=[]
            timber_volume=[]
            for j in np.unique(df_sps['径阶']):
                if j < 4:
                    print('警告！径阶小于4:{},行索引:{}\n'.format(j,df_sps[df_sps['径阶']==j].index.tolist()))
                    print(df_sps[df_sps['径阶']==j])
                    continue
                else:
                    a = len(df_sps[df_sps['径阶'] == j])
                    D=j
                    if tree_name=='红松':
                        v = Pinus_koraiensis(D)
                    elif tree_name=='水曲柳':
                        v=Fraxinus(D)
                    elif tree_name=='红皮云杉'or tree_name=='鱼鳞云杉':
                        v=Picea(D)
                    elif tree_name=='冷杉'or tree_name=='辽东冷杉':
                        v=Abies(D)
                    elif tree_name=='大青杨':
                        v=Populus(D)
                    elif tree_name=='落叶松':
                        v=Larix(D)
                    elif tree_name=='胡桃楸':
                        v=Juglans(D)
                    elif tree_name=='黄菠萝':
                        v=Phellodendron(D)
                    elif tree_name=='色木':
                        v=Juglans(D)
                    elif tree_name == '春榆' or tree_name == '裂叶榆':
                        v=Ulmus(D)
                    elif tree_name=='枫桦':
                        v=Betula_costata(D)
                    elif tree_name=='柞树':
                        v=Quercus(D)
                    elif tree_name=='黑桦':
                        v=Betula_davurica(D)
                    elif tree_name=='紫椴':
                        v=Tilia(D)
                    elif tree_name=='白桦':
                        v=Betula_platyphylla(D)
                    elif tree_name=='山杨':
                        v=Populus_davidiana(D)
                    else:
                        v=broadleaf(D)
                    v_all=v*a

                basename = i.rsplit('.', 1)[0]
                out_df['Plot'].append(basename)
                out_df['树种'].append(tree_name)
                out_df['径阶'].append(j)
                out_df['径阶蓄积'].append(v_all)

out_df=pd.DataFrame(out_df)
print(out_df.isnull().sum())
out_df.to_excel(os.path.join(out_path,'各径阶林分蓄积.xlsx'),index=False)

# 定义一个函数来根据径阶分类
def classify_diameter_class(diameter):
    if diameter <= 12:
        return '小径木'
    elif 12 < diameter <= 24:
        return '中径木'
    else:
        return '大径木'
df=out_df.copy()
# 应用分类函数到径阶列，并创建一个新列来存储分类结果
df['分类'] = df['径阶'].apply(classify_diameter_class)

# 创建一个空的DataFrame来存储每个Plot的大中小径木的蓄积
result = pd.DataFrame(columns=['Plot','树种', '小径木蓄积', '中径木蓄积', '大径木蓄积'])
# 遍历每个Plot，计算大中小径木的蓄积
Plots = df['Plot'].unique()
Plot_list=[]
sps_list=[]
small_diameter_volume_list=[]
medium_diameter_volume_list=[]
large_diameter_volume_list=[]
for Plot in Plots:
    Plot_data = df[df['Plot'] == Plot]
    for sps in Plot_data['树种'].unique():
        Plot_data_sps = Plot_data[Plot_data['树种'] == sps]
        small_diameter_volume = Plot_data_sps[Plot_data_sps['分类'] == '小径木']['径阶蓄积'].sum()
        medium_diameter_volume = Plot_data_sps[Plot_data_sps['分类'] == '中径木']['径阶蓄积'].sum()
        large_diameter_volume = Plot_data_sps[Plot_data_sps['分类'] == '大径木']['径阶蓄积'].sum()
        Plot_list.append(Plot)
        sps_list.append(sps)
        small_diameter_volume_list.append(small_diameter_volume)
        medium_diameter_volume_list.append(medium_diameter_volume)
        large_diameter_volume_list.append(large_diameter_volume)


result['Plot'] = Plot_list
result['树种'] = sps_list
result['小径木蓄积']=small_diameter_volume_list
result['中径木蓄积']=medium_diameter_volume_list
result['大径木蓄积']=large_diameter_volume_list
print(result)
result.to_excel(os.path.join(out_path,'树种大中小径木蓄积.xlsx'),index=False)
