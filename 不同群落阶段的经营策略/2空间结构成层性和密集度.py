import pandas as pd
import numpy as np
import os
#挑选距离参照树最近的四株相邻木
def get_distance(data,inX):#inX=0
    dataSet=data
    tree_points=dataSet[['X轴','Y轴']]
    tree_points=tree_points.values

    dataSetSize=dataSet.shape[0]#获取行数
    tree=tree_points[inX]#随机当前树
    diffMat=np.tile(tree,(dataSetSize,1))-tree_points#使当前树与其他树做减法
    sqDiffMat=diffMat**2
    sqDiftances=sqDiffMat.sum(axis=1)
    distances=np.sqrt(sqDiftances)
    sortedDistIndicies=distances.argsort()
    return [sortedDistIndicies[0:5],distances[sortedDistIndicies[0:5]]]
def crowding(crowd_list,distance_list):#计算密集性
    lst=[]
    first = list(crowd_list)[0]
    for i, j in zip(crowd_list[1:], distance_list[1:]):
        if i+first>j:
            Z=1
        else:
            Z=0
        lst.append(Z)
    CW=np.sum(lst)/4
    return CW
def layers(height):#计算成层性
    c=[]
    hei_list=list(height)
    refrence_dia=hei_list[0]
    for d in hei_list[1:]:
        if abs(d-hei_list[0])>=5:
            k=1
        else:
            k=0
        c.append(k)
    lay=np.sum(c)/4
    return lay

file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)
out_df=pd.DataFrame()
C_list=[]
Lay_list=[]
Sps_list=[]
Number_list=[]
Plot_list=[]
X_list=[]
Y_list=[]
for names in name_list:
    data=os.path.join(file_path,names)
    data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    #print(data.head())
    #print(data.dtypes)
    if __name__=='__main__':
        a = 0
        data = data[~data['状态'].isin(['枯立木', '倒木'])]
        data = data[~data['树种'].isin(['空牌'])]
        data['状态'] = data['状态'].fillna('正常')
        data = data[data['状态'].isin(['正常','丛生'])]
        data.loc[:,['东', '南','西','北']] = data[['东', '南','西','北']].ffill()
        data = data.reset_index(drop=True)
        dataSet = data
        tree_points = dataSet[['X轴', 'Y轴']]
        tree_points = tree_points.values
        sps = dataSet['树种']
        height = dataSet['树高']
        # 选择指定列
        specified_columns = ['东', '南', '西', '北']
        selected_data = dataSet[specified_columns]
        # 对每一行的指定列求均值
        row_means = selected_data.mean(axis=1)
        # 将均值添加到原始DataFrame作为一个新列
        dataSet['crowding_average'] = row_means
        crowd_list = dataSet['crowding_average']
        # 填充空值，使得冠幅为0是密集度为1，即最大密集度
        dataSet['crowding_average'].fillna(100, inplace=True)
        idx = []
        for i in range(len(tree_points)):
            a+=1
            ids = get_distance(dataSet, i)
            idx.append(ids)
            distance_list = ids[1]
            C = crowding(crowd_list[ids[0]], distance_list)
            C_list.append(C)
            Lay= layers(height[ids[0]])
            Lay_list.append(Lay)
            # 树种
            Sps_list.append(sps[ids[0][0]])
            # 坐标
            X_list.append(tree_points[ids[0]][0][0])
            Y_list.append(tree_points[ids[0]][0][1])
            Number_list.append(a)
            basename = names.rsplit('.', 1)[0]
            Plot_list.append(basename)

out_df['Plot']=Plot_list
out_df['编号']=Number_list
out_df['密集度']=C_list
out_df['成层性']=Lay_list
out_df['树种']=Sps_list
out_df['X轴']=X_list
out_df['Y轴']=Y_list
out_df.to_excel(os.path.join(out_path,'密集度和成层性.xlsx'),index=False)
#去除边缘效应
out_df['X轴'] = pd.to_numeric(out_df['X轴'], errors='coerce')
out_df['Y轴'] = pd.to_numeric(out_df['Y轴'], errors='coerce')
out_df_adj=out_df[(out_df['X轴'] < 90)&(out_df['Y轴'] < 90)&(out_df['X轴'] >10)&
            (out_df['Y轴'] >10)]
out_df_adj=out_df_adj.copy()
#求各树种
out_df_adj['树种密集度均值']=out_df_adj.groupby(['Plot','树种'])['密集度'].transform('mean')
out_df_adj['树种成层性均值']=out_df_adj.groupby(['Plot','树种'])['成层性'].transform('mean')
out_df_adj2=out_df_adj.drop_duplicates(subset=['Plot','树种'])
out_df_adj2.to_excel(os.path.join(out_path,'密集度和成层性树种均值.xlsx'),index=False)
#求样地均值
out_df_adj['密集度均值']=out_df_adj.groupby('Plot')['密集度'].transform('mean')
out_df_adj['成层性均值']=out_df_adj.groupby('Plot')['成层性'].transform('mean')
out_df_adj1=out_df_adj.drop_duplicates(subset=['Plot'])
out_df_adj1.to_excel(os.path.join(out_path,'密集度和成层性样地均值.xlsx'),index=False)
print(out_df_adj1,out_df_adj2)