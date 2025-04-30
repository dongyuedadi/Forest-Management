import pandas as pd
import numpy as np
import os
#挑选距离参照树最近的四株相邻木
def get_distance(data,inX):#inX=0
    dataSet=data
    tree_points=dataSet[['X','Y']]
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
#定义密集度
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

#定义材积公式
def yk(D):#北亚热带硬阔材积
    v=0.0519568-0.01152192*D+0.00089433*D**2
    return v
#空间结构参数计算
if __name__=='__main__':
    file_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\path'
    out_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out2'
    W_list = []
    U_list = []
    H_list = []
    C_list=[]
    Sps_list=[]
    Pt_list = []
    BH_list=[]
    VOL_list=[]

    file = os.path.join(file_path, '模拟样地经营前.xlsx')
    data = pd.read_excel(file)
    #print(data.head())
    #print(data.dtypes)
    plots = data['样地'].unique()
    for plot in plots:
        a = 0
        dataSet = data[data['样地'] == plot].reset_index(drop=True)
        tree_points = dataSet[['X', 'Y']]
        tree_points = tree_points.values
        sps = dataSet['树种']
        diameter = dataSet['胸径']
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
            angles = get_vector_included_angle2(tree_points, idx[i])
            H = mingling(sps[ids[0]])
            H_list.append(H)
            W = comparision(angles)
            W_list.append(W)
            U = comparision_DBH(diameter[ids[0]])
            U_list.append(U)
            C = crowding(crowd_list[ids[0]], distance_list)
            C_list.append(C)
            BH_list.append(a)
            #计算材积
            vol=yk(dataSet.loc[ids[0][0]]['胸径'])
            VOL_list.append(vol)
            #
            Sps_list.append(sps[ids[0][0]])
            Pt_list.append(plot)

    out_df=pd.DataFrame()
    out_df['样地'] = Pt_list
    out_df['树种']=Sps_list
    out_df['角尺度']=W_list
    out_df['大小比']=U_list
    out_df['混交度']=H_list
    out_df['密集度']=C_list
    out_df['编号']=BH_list
    out_df['材积']=VOL_list
    out_df.to_excel(os.path.join(out_path,'空间结构.xlsx'),index=False)


def bar_probility(out_df,names):
    plots = out_df['样地'].unique()
    all_data = []  # 初始化一个空列表来存储每个样地的DataFrame
    for plot in plots:
        data = out_df.loc[out_df['样地'] == plot]
        values_of_interest = [0, 0.25, 0.5, 0.75, 1]
        # 计算每个值在 data[names] 中出现的次数
        value_counts = data[names].value_counts().reindex(values_of_interest, fill_value=0).to_dict()
        # 初始化一个字典来存储每个值的概率
        prob_distribution = {value: count / len(data[names]) for value, count in value_counts.items()}
        # 创建一个DataFrame来存储当前样地的概率分布
        data1 = [[key, value] for key, value in prob_distribution.items()]
        df_plot = pd.DataFrame(data1, columns=[names, 'probability'])
        df_plot['样地'] = plot  # 将样地名添加到DataFrame中
        # 将当前样地的DataFrame添加到列表中
        all_data.append(df_plot)

    # 使用pd.concat()将列表中的所有DataFrame合并成一个
    df_all = pd.concat(all_data, ignore_index=True)
    # 打印合并后的DataFrame
    from matplotlib import pyplot as plt
    plt.figure(figsize=(8, 6))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False
    bars1 = df_all.loc[df_all['样地'] == 1, 'probability'].copy()
    bars2 = df_all.loc[df_all['样地'] == 2, 'probability'].copy()
    barWidth = 0.25
    r1 = [1, 3, 5, 7, 9]
    r2 = [x + barWidth for x in r1]
    plt.bar(r1, bars1, color='r', width=barWidth, edgecolor='black')
    plt.bar(r2, bars2, color='g', width=barWidth, edgecolor='black')
    plt.yticks(fontsize=15)
    plt.xticks([r + barWidth / 2 for r in r1], [0, 0.25, 0.5, 0.75, 1],fontsize=15)
    plt.title(names,fontsize=15)
    #plt.show()

    return df_all


for names in ['角尺度', '大小比', '混交度']:
    df_probility=bar_probility(out_df, names)
    df_probility.to_excel(os.path.join(out_path, f'{names}.xlsx'), index=False)

#样地总体情况
print('角尺度',out_df[out_df['样地']==2]['角尺度'].mean())
print('大小比',out_df[out_df['样地']==2]['大小比'].mean())
print('混交度',out_df[out_df['样地']==2]['混交度'].mean())

#主要树种情况
hunjiaodu_list=[]
daxiaobiaodu_list=[]
jiaochidu_list=[]
spsnanmes_list=[]
for spsnanmes in ['红松','胡桃楸','黄菠萝','春榆','柞树','白桦','水曲柳','紫椴']:
    h=out_df[(out_df['样地'] == 2) & (out_df['树种'] == spsnanmes)]['混交度'].mean()
    d=out_df[(out_df['样地'] == 2) & (out_df['树种'] == spsnanmes)]['大小比'].mean()
    j=out_df[(out_df['样地'] == 2) & (out_df['树种'] == spsnanmes)]['角尺度'].mean()
    hunjiaodu_list.append(h)
    daxiaobiaodu_list.append(d)
    jiaochidu_list.append(j)
    spsnanmes_list.append(spsnanmes)
zhuyaoshuzong_df=pd.DataFrame()
zhuyaoshuzong_df['树种']=spsnanmes_list
zhuyaoshuzong_df['角尺度']=jiaochidu_list
zhuyaoshuzong_df['大小比']=daxiaobiaodu_list
zhuyaoshuzong_df['混交度']=hunjiaodu_list
zhuyaoshuzong_df.to_excel(os.path.join(out_path,'主要树种空间结构.xlsx'),index=False)













