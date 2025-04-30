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

#角尺度计算
def get_vector_included_angle2(trees_points,ids):
    central_tree_id=ids[0][0]
    last_four_tree_id=ids[0][1:]
    degrees=[]
    for id in last_four_tree_id[0:]:
        first_vec=trees_points[id]-trees_points[central_tree_id]
        x=first_vec[0]
        y=first_vec[1]
        theta=np.math.atan2(y,x)*180.0/np.pi#弧度转化为度
        if theta<0:
            theta+=360.0
        degrees.append(theta)
    degrees.sort()
    angles=[degrees[1]-degrees[0],degrees[2]-degrees[1],degrees[3]-degrees[2],degrees[3]-degrees[0]]
    for i,_ in enumerate(angles):
        if angles[i]>180:
            angles[i]-=360.0

    return angles

#定义角尺度、大小比数、混角度计算函数
def comparision(degree_list):#角尺度
    a=[]
    for i in degree_list:
        if i<72:
            Z=1
        else:
            Z=0
        a.append(Z)
    W=np.sum(a)/4
    return W

#定义大小比
def comparision_DBH(dbhs):#大小比
    b=[]
    dia_list=list(dbhs)
    refrence_dia=dia_list[0]
    for d in dia_list[1:]:
        if d<refrence_dia:
            k=0
        else:
            k=1
        b.append(k)
    M=np.sum(b)/4
    return M

#定义混交度
def mingling(class_list):
    lst=[]
    first=list(class_list)[0]
    for i in class_list[1:]:
        if i==first:
            k=0
        else:
            k=1
        lst.append(k)
    h=np.sum(lst)/4
    return h

file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)
out_df=pd.DataFrame()
#空间结构参数计算
W_list = []
U_list = []
H_list = []
Sps_list = []
Pt_list = []
BH_list = []
X_list=[]
Y_list=[]
for names in name_list:
    data=os.path.join(file_path,names)
    data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    #print(data.head())
    #print(data.dtypes)
    if __name__=='__main__':
        a = 0
        data = data[~data['状态'].isin(['枯立木', '倒木'])].reset_index(drop=True)
        data.loc[:,['X轴', 'Y轴']] = data[['X轴', 'Y轴']].ffill()
        dataSet = data
        tree_points = dataSet[['X轴', 'Y轴']]
        tree_points = tree_points.values
        sps = dataSet['树种']
        diameter = dataSet['胸径']
        idx = []
        for i in range(len(tree_points)):
            a+=1
            ids = get_distance(dataSet, i)
            idx.append(ids)
            distance_list = ids[1]
            angles = get_vector_included_angle2(tree_points, idx[i])
            H = mingling(sps[ids[0]])
            H_list.append(H)
            W = comparision(angles)
            W_list.append(W)
            U = comparision_DBH(diameter[ids[0]])
            U_list.append(U)
            BH_list.append(a)
            # 坐标
            X_list.append(tree_points[ids[0]][0][0])
            Y_list.append(tree_points[ids[0]][0][1])
            #
            Sps_list.append(sps[ids[0][0]])
            basename = names.rsplit('.', 1)[0]
            Pt_list.append(basename)
out_df['Plot'] = Pt_list
out_df['树种']=Sps_list
out_df['角尺度']=W_list
out_df['大小比']=U_list
out_df['混交度']=H_list
out_df['编号']=BH_list
out_df['X轴']=X_list
out_df['Y轴']=Y_list
out_df.to_excel(os.path.join(out_path,'空间结构.xlsx'),index=False)
#去除边缘效应
out_df['X轴'] = pd.to_numeric(out_df['X轴'], errors='coerce')
out_df['Y轴'] = pd.to_numeric(out_df['Y轴'], errors='coerce')

out_df_adj=out_df[(out_df['X轴'] < 90)&(out_df['Y轴'] < 90)&(out_df['X轴'] >10)&
            (out_df['Y轴'] >10)]
out_df_adj=out_df_adj.copy()
#分树种求均值
out_df_adj['树种角尺度均值']=out_df_adj.groupby(['Plot','树种'])['角尺度'].transform('mean')
out_df_adj['树种大小比均值']=out_df_adj.groupby(['Plot','树种'])['大小比'].transform('mean')
out_df_adj['树种混交度均值']=out_df_adj.groupby(['Plot','树种'])['混交度'].transform('mean')

out_df_adj2=out_df_adj.drop_duplicates(subset=['Plot','树种'])
out_df_adj2.to_excel(os.path.join(out_path,'空间结构指数树种均值.xlsx'),index=False)
#分样地求均值
out_df_adj['角尺度均值']=out_df_adj.groupby('Plot')['角尺度'].transform('mean')
out_df_adj['大小比均值']=out_df_adj.groupby('Plot')['大小比'].transform('mean')
out_df_adj['混交度均值']=out_df_adj.groupby('Plot')['混交度'].transform('mean')

out_df_adj1=out_df_adj.drop_duplicates(subset=['Plot'])
out_df_adj1.to_excel(os.path.join(out_path,'空间结构指数样地均值.xlsx'),index=False)

out_df_adj.to_excel(os.path.join(out_path,'空间结构指数.xlsx'),index=False)
print(out_df_adj1,out_df_adj2)















