import os
import pandas as pd
import numpy as np
file_path=r"C:\Users\hys5637428\Desktop\实验\燕安\小兴安岭采伐方案\原始数据\燕安林场2023年40块"
file_out=r'C:\Users\hys5637428\Desktop\实验\燕安\小兴安岭采伐方案'
name_list=os.listdir(file_path)#遍历路径中所有文件名字，并生成列表
#name_list.sort(key=lambda i:int(re.search("([a-z]*)([0-9]*)",i).group(2)))
out_df={'plot':[],'平均胸径':[],'算数平均胸径':[],'加权平均高':[],'林分密度':[]}

a=0
for i in name_list:
    a+=1
    df1=os.path.join(file_path,i)
    df1=pd.read_excel(df1,sheet_name='每木检尺及测高记录表')
    #数据清洗
    data=pd.DataFrame()
    data['胸径']=df1['胸径']
    data['树高']=df1['树高']
    Dominance_Density = len(data['树高'])
    data.dropna(subset=['树高'], inplace=True)
    data.dropna(subset=['胸径'], inplace=True)
    basename = i.rsplit('.', 1)[0]
    print(basename,data['胸径'].dtypes)
    maxvalue = max(data['胸径'])
    maxvalue = int(maxvalue)
    data.drop_duplicates()
    if maxvalue > 5:
        df=data.copy()
        average_DBH=np.mean(df['胸径'])
        count_all=len(df)
        listBins=list(range(0,maxvalue+2,2))
        listLabels=list(range(1,maxvalue+1,2))
        df['径阶']=None
        df['径阶']=pd.cut(df['胸径'],bins=listBins,labels=listLabels,include_lowest=True)
        high=[]
        area=[]
        dbh=[]
        df.dropna(subset=['径阶'], inplace=True)
        for j in np.unique(df['径阶']):
            if j < 5:
                print('警告！径阶小于5:{},行索引:{}\n'.format(j,df[df['径阶']==j].index.tolist()))
                print(df[df['径阶']==j])

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
        out_df['plot'].append(basename)
        out_df['林分密度'].append(Dominance_Density)

out_df=pd.DataFrame(out_df)
out_df.to_excel(os.path.join(file_out,'标准地计算.xlsx'),index=False)
