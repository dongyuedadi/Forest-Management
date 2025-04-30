import os
import pandas as pd
import numpy as np
file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)

out_df={'plot':[],'树种':[],'径阶':[],'株树':[]}
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
        listBins =list(range(5, maxvalue + 2, 2))
        listLabels = list(range(6, maxvalue + 1, 2))
        df['径阶'] = None
        df['径阶'] = pd.cut(df['胸径'], bins=listBins, labels=listLabels, include_lowest=True)
        df.dropna(subset=['径阶'], inplace=True)
        tree_names=list(df['树种'].unique())
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
                    out_df['树种'].append(tree_name)
                    out_df['径阶'].append(j)
                    out_df['株树'].append(a)
                    basename = i.rsplit('.', 1)[0]
                    out_df['plot'].append(basename)

out_df=pd.DataFrame(out_df)
print(out_df)
out_df.to_excel(os.path.join(out_path,'林分株树各径阶分布.xlsx'),index=False)