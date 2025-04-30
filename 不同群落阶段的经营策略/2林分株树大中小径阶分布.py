import os
import pandas as pd
import numpy as np
file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)

out_df={'Plot':[],'树种':[],'径阶':[],'径阶株树':[]}
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
                basename = i.rsplit('.', 1)[0]
                out_df['Plot'].append(basename)
                out_df['树种'].append(tree_name)
                out_df['径阶'].append(j)
                out_df['径阶株树'].append(a)

out_df=pd.DataFrame(out_df)
print(out_df.isnull().sum())
out_df.to_excel(os.path.join(out_path,'各径阶林分株树.xlsx'),index=False)

# 定义一个函数来根据径阶分类
def classify_diameter_class(diameter):
    if diameter <= 12:
        return '小径木'
    elif 12 < diameter <= 24:
        return '中径木'
    elif 24 < diameter<=34:
        return '大径木'
    else:
        return '特大径木'
df=out_df.copy()
# 应用分类函数到径阶列，并创建一个新列来存储分类结果
df['分类'] = df['径阶'].apply(classify_diameter_class)

# 创建一个空的DataFrame来存储每个plot的大中小径木的蓄积
result = pd.DataFrame(columns=['Plot', '小径木株树', '中径木株树', '大径木株树', '特大径木'])
# 遍历每个plot，计算大中小径木的蓄积
plots = df['Plot'].unique()
plot_list=[]
small_diameter_volume_list=[]
medium_diameter_volume_list=[]
large_diameter_volume_list=[]
super_diameter_volume_list=[]
for plot in plots:
    plot_data = df[df['Plot'] == plot]
    small_diameter_volume = plot_data[plot_data['分类'] == '小径木']['径阶株树'].sum()
    medium_diameter_volume = plot_data[plot_data['分类'] == '中径木']['径阶株树'].sum()
    large_diameter_volume = plot_data[plot_data['分类'] == '大径木']['径阶株树'].sum()
    super_diameter_volume = plot_data[plot_data['分类'] == '特大径木']['径阶株树'].sum()
    plot_list.append(plot)
    small_diameter_volume_list.append(small_diameter_volume)
    medium_diameter_volume_list.append(medium_diameter_volume)
    large_diameter_volume_list.append(large_diameter_volume)
    super_diameter_volume_list.append(super_diameter_volume)
result['Plot'] = plot_list
result['小径木株树']=small_diameter_volume_list
result['中径木株树']=medium_diameter_volume_list
result['大径木株树']=large_diameter_volume_list
result['特大径木']=super_diameter_volume_list
result['活立木总株树']=result['小径木株树']+result['中径木株树']+result['大径木株树']+result['特大径木']
print(result)
result.to_excel(os.path.join(out_path,'林分大中小径木株树.xlsx'),index=False)
