def luoyesong(*args):#落叶松生物量
    w=0.0526*(D**2.5257)+0.0085*(D**2.4815)+0.0168*(D**2.0026)+0.0291*(D**2.2645)
    return w
def hongsong(*args):#红松生物量
    w=0.1087*(D**2.1527)+0.0481*(D**2.0877)+0.0631*(D**1.8343)+0.0305*(D**2.3298)
    return w
def rk():#北亚热带软阔材积
    v=0.01129474+(-0.00351198*D)+0.00052111*D**2
    return v
def yk(D):#北亚热带硬阔材积
    v=0.0519568-0.01152192*D+0.00089433*D**2
    return v

import os
import pandas as pd
import numpy as np
file_path=r"C:\\Users\\hys5637428\\Desktop\\帽儿山蘑菇调查\\path"
file_out=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out2'
name_list=os.listdir(file_path)#遍历路径中所有文件名字，并生成列表
#name_list.sort(key=lambda i:int(re.search("([a-z]*)([0-9]*)",i).group(2)))
out_df={'plot':[],'样地':[],'树种':[],'胸高断面积':[],'树种蓄积':[]}

a=0
for i in name_list:
    a+=1
    data=os.path.join(file_path,i)
    data=pd.read_excel(data)
    #数据清洗
    data=data.copy()
    if data.empty:
        print("DataFrame 是空的")
    elif data['胸径'].isnull().all():
        print("'胸径' 列全是空的或 NaN 值")
    else:
        maxvalue = max(data['胸径'])
        maxvalue = int(maxvalue)+1
    data.dropna(subset=['树高'], inplace=True)
    data = data[data['树高'] != 0]
    data.drop_duplicates()
    data['树种'] = data['树种'].ffill()
    #数据处理
    plotname=data['样地'].unique()
    for nm in plotname:
        df = data.copy()
        listBins = [0, 1] + list(range(3, maxvalue + 2, 2))
        listLabels = list(range(0, maxvalue + 1, 2))
        df['径阶'] = None
        df['径阶'] = pd.cut(df['胸径'], bins=listBins, labels=listLabels, include_lowest=True)
        df=df[df['样地']==nm].copy()
        tree_names=list(df['树种'].unique())
        b=0
        for tree_name in tree_names:
            b+=1
            df_sps = df[df['树种'] ==tree_name].copy()
            area=[]
            timber_volume=[]
            for j in np.unique(df_sps['径阶']):
                if j < 5:
                    print('警告！径阶小于5:{},行索引:{}\n'.format(j,df_sps[df_sps['径阶']==j].index.tolist()))
                    print(df_sps[df_sps['径阶']==j])
                    df_sps.drop(df_sps[df_sps['径阶']==j].index,axis=0,inplace=True)
                else:
                    a = len(df_sps[df_sps['径阶'] == j])
                    d = np.square(int(j) / 2 / 100) * 3.14 * a
                    area.append(d)
                    v=yk(j)
                    v_all=v*a
                    timber_volume.append(v)

            area_sps=sum(area)
            timber_volume_sps=sum(timber_volume)
            out_df['胸高断面积'].append(area_sps)
            out_df['树种蓄积'].append(timber_volume_sps)
            out_df['plot'].append(i)
            out_df['样地'].append(nm)
            out_df['树种'].append(tree_name)
out_df=pd.DataFrame(out_df)

out_df['蓄积']=out_df.groupby(['plot','样地'])['树种蓄积'].transform('sum')
out_df['树种蓄积占比']=round(out_df['树种蓄积']/out_df['蓄积'],2)
out_df.to_excel(os.path.join(file_out,'林分蓄积—树种组成.xlsx'),index=False)