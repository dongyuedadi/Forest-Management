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
def crowding(crowd_list,distance_list):
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
C_list=[]
W_list = []
U_list = []
H_list = []
Sps_list = []
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
        sps = dataSet['树种']
        diameter = dataSet['胸径']
        idx = []
        for i in range(len(tree_points)):
            a += 1
            ids = get_distance(dataSet, i)
            idx.append(ids)
            distance_list = ids[1]
            angles = get_vector_included_angle2(tree_points, idx[i])
            #混交度
            H = mingling(sps[ids[0]])
            H_list.append(H)
            #角尺度
            W = comparision(angles)
            W_list.append(W)
            #大小比
            U = comparision_DBH(diameter[ids[0]])
            U_list.append(U)
            #密集度
            C = crowding(crowd_list[ids[0]], distance_list)
            C_list.append(C)
            #树种
            Sps_list.append(sps[ids[0][0]])
            #坐标
            X_list.append(tree_points[ids[0]][0][0])
            Y_list.append(tree_points[ids[0]][0][1])
            #编号
            Number_list.append(a)
            #样地
            basename = names.rsplit('.', 1)[0]
            Plot_list.append(basename)

out_df['Plot']=Plot_list
out_df['编号']=Number_list
out_df['密集度']=C_list
out_df['树种']=Sps_list
out_df['角尺度']=W_list
out_df['大小比']=U_list
out_df['混交度']=H_list
out_df['Y轴']=Y_list
out_df['X轴']=X_list
# 根据规则更新'角尺度参数'列的值
conditions = [
    (out_df['角尺度'] == 0),
    (out_df['角尺度'] == 0.25),
    (out_df['角尺度'] == 0.5),
    (out_df['角尺度'] == 0.75),
    (out_df['角尺度'] == 1)
]
values = [1, 0.75, 0.5, 0.375, 0.25]
out_df['角尺度参数'] =None
out_df['角尺度参数'] = np.select(conditions, values, default=out_df['角尺度参数'])
out_df['角尺度参数'] = pd.to_numeric(out_df['角尺度参数'], errors='coerce')
# 根据规则更新'混交度参数'列的值
conditions = [
    (out_df['混交度'] == 0),
    (out_df['混交度'] == 0.25),
    (out_df['混交度'] == 0.5),
    (out_df['混交度'] == 0.75),
    (out_df['混交度'] == 1)
]
values = [1, 0.97, 0.93, 0.89, 0.85]
out_df['混交度参数'] =None
out_df['混交度参数'] = np.select(conditions, values, default=out_df['角尺度参数'])
out_df['混交度参数'] = pd.to_numeric(out_df['混交度参数'], errors='coerce')
#定义竞争指数
out_df['竞争指数'] =None
out_df['竞争指数']=np.sqrt((out_df['大小比']*out_df['密集度']*out_df['混交度参数']*out_df['角尺度参数']))
print(out_df[out_df['树种']=='大青杨']['大小比'])
#去除边缘效应
out_df['X轴'] = pd.to_numeric(out_df['X轴'], errors='coerce')
out_df['Y轴'] = pd.to_numeric(out_df['Y轴'], errors='coerce')

out_df_adj=out_df[(out_df['X轴'] < 90)&(out_df['Y轴'] < 90)&(out_df['X轴'] >10)&
            (out_df['Y轴'] >10)]
out_df_adj=out_df_adj.copy()
#分树种求均值
out_df_adj['树种竞争指数均值']=out_df_adj.groupby(['Plot','树种'])['竞争指数'].transform('mean')

out_df_adj2=out_df_adj.drop_duplicates(subset=['Plot','树种'])
out_df_adj2.to_excel(os.path.join(out_path,'竞争指数树种均值.xlsx'),index=False)
#分样地求均值
out_df_adj['竞争指数均值']=out_df_adj.groupby('Plot')['竞争指数'].transform('mean')

out_df_adj1=out_df_adj.drop_duplicates(subset=['Plot'])
out_df_adj1.to_excel(os.path.join(out_path,'竞争指数样地均值.xlsx'),index=False)

out_df_adj.to_excel(os.path.join(out_path,'竞争指数.xlsx'),index=False)
#print(out_df_adj1,out_df_adj2)