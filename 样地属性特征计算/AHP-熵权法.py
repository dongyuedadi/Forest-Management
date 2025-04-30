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


#空间结构参数计算
if __name__=='__main__':
    file_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查'
    out_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out2'
    W_list = []
    U_list = []
    H_list = []
    C_list=[]
    Sps_list=[]
    Pt_list = []
    PtName=[]

    file = os.path.join(file_path, '模拟样地.xlsx')
    data = pd.read_excel(file)
    #print(data.head())
    #print(data.dtypes)
    plots = data['样地'].unique()
    for plot in plots:
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
            #
            Sps_list.append(sps[ids[0][0]])
            Pt_list.append(plot)

    out_df=pd.DataFrame()
    out_df['PtName'] = PtName
    out_df['样地'] = Pt_list
    out_df['树种']=Sps_list
    out_df['角尺度']=W_list
    out_df['大小比']=U_list
    out_df['混交度']=H_list
    out_df['密集度']=C_list
    out_df.to_excel(os.path.join(out_path,'空间结构.xlsx'),index=False)

dict_Redundancy = {}
for names in ['角尺度', '大小比', '混交度']:
    data_entropy = out_df[names]
    # 计算概率分布
    probabilities = data_entropy.value_counts(normalize=True)
    # 确保probabilities的值不是numpy数组
    probabilities = {k: float(v) for k, v in probabilities.items()}
    # 计算信息熵
    entropy = -sum(prob * np.log(prob)/np.log(len(data_entropy)) for prob in probabilities.values())
    dict_Redundancy[names] = 1 - entropy
print(dict_Redundancy)
pd_SQF=pd.DataFrame(dict_Redundancy.values())

def normalize(vector):
    """将向量归一化，使其元素之和为1。"""
    norm = np.sum(vector)
    return vector / norm
def calculate_weights(matrix):
    """根据成对比较矩阵计算权重。"""
    # 计算特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    # 找出最大特征值的索引
    max_eigenvalue_index = np.argmax(eigenvalues)
    # 获取对应的特征向量
    max_eigenvector = eigenvectors[:, max_eigenvalue_index]
    # 将特征向量归一化，得到权重
    weights = normalize(max_eigenvector.real)  # 只取实部作为权重
    # 计算一致性指标（CI）
    n = matrix.shape[0]  # 矩阵的阶数
    max_eigenvalue = eigenvalues[max_eigenvalue_index].real
    CI = (max_eigenvalue - n) / (n - 1)
    return weights, eigenvalues[max_eigenvalue_index].real,CI  # 返回权重和最大特征值的实部
# 第二步：构建成对比较矩阵
criteria_matrix = np.array([
    [1, 2, 2/3],
    [1/2 , 1, 1/3],
    [3/2, 3, 1]
])
# 第三步：计算准则和选项的权重
criteria_weights, _ ,CI= calculate_weights(criteria_matrix)
#一致性检验
RI=0.8#随机一致性指标查表可得
CR = CI / RI
if CR>0.1:
    print('\n警告！！！\n一致性检验不通过！！！')
else:
    print('\n通过一致性检验\n')
# 第四步：合成权重
final_weights = normalize(criteria_weights)
print('AHP法角尺度, 大小比, 混交度权重分别为：',final_weights)
pd_AHP=pd.DataFrame(final_weights)
print(pd_SQF[:2])
pd_AHP_SQF = 0.4*pd_AHP+0.6*pd_SQF
print('AHP和熵权法综合,角尺度, 大小比, 混交度权重分别为：',pd_AHP_SQF)








