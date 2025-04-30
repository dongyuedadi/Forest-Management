import os
import pandas as pd
import numpy as np
file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)#遍历路径中所有文件名字，并生成列表
out_df={'plot':[],'平均胸径':[],'算数平均胸径':[],'加权平均高':[],'株树密度':[]}

a=0
for i in name_list:
    a+=1
    data=os.path.join(file_path,i)
    data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
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
    #data = data.dropna(subset=['X', 'Y', '树种'])
    data.drop_duplicates()
    #数据处理
    if __name__=='__main__':
        df=data.copy()
        average_DBH=np.mean(df['胸径'])
        tree_names=list(df['树种'].unique())
        count_all=len(df)
        listBins = list(range(5, maxvalue + 2, 2))
        listLabels = list(range(6, maxvalue + 1, 2))
        df['径阶'] = None
        df['径阶'] = pd.cut(df['胸径'], bins=listBins, labels=listLabels, include_lowest=True)
        df.dropna(subset=['径阶'], inplace=True)
        high=[]
        area=[]
        dbh=[]
        for j in np.unique(df['径阶']):
            if j < 5:
                print('警告！径阶小于5:{},行索引:{}\n'.format(j,df[df['径阶']==j].index.tolist()))
                print(df[df['径阶']==j])
                df.drop(df[df['径阶']==j].index,axis=0,inplace=True)
            else:
                h=np.mean(df.loc[df['径阶']==j]['树高'].values)
                a=len(df[df['径阶']==j])
                d=np.square(int(j)/2/100)*3.14*a
                b=np.square(int(j))*a
                dbh.append(b)
                area.append(d)
                c=h*d
                high.append(c)

        if np.sum(area) == 0 or count_all == 0:
            raise ValueError("Total area or total tree count is zero, cannot compute average.")
        H=np.sum(high)/np.sum(area)
        D=np.sqrt(np.sum(dbh)/count_all)
        out_df['平均胸径'].append(round(D,2))
        out_df['算数平均胸径'].append(round(average_DBH,2))
        out_df['加权平均高'].append(round(H,2))
        out_df['株树密度'].append(len(df['胸径']))
        basename = i.rsplit('.', 1)[0]
        out_df['plot'].append(basename)

out_df=pd.DataFrame(out_df)
print(out_df)
out_df.to_excel(os.path.join(out_path,'标准地计算.xlsx'),index=False)
