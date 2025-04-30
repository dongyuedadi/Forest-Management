import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False
from scipy.stats import chi2_contingency

# 计算种间联结系数，这里使用Jaccard指数
def jaccard_index(series1, series2):
    intersection = (series1 & series2).sum()
    union = (series1 | series2).sum()
    return intersection / union if union != 0 else 0

file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)

for i in name_list:
    data=os.path.join(file_path,i)
    tree_data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    # 划分带
    tree_data['备注']=tree_data['备注'].ffill()
    #去除空值
    tree_data.dropna(subset=['树种'], inplace=True)
    tree_data.drop_duplicates(subset=['备注','树种'], inplace=True)

    df = pd.DataFrame()
    df['树种']=tree_data['树种']
    df['带']=tree_data['备注']

    # 创建一个树种的二进制矩阵（存在为1，不存在为0）
    tree_matrix = pd.crosstab(df['带'], df['树种'])
    # 初始化一个空的DataFrame来存储种间联结系数
    association_matrix = pd.DataFrame(index=tree_matrix.columns, columns=tree_matrix.columns)
    # 填充种间联结系数矩阵
    for i in tree_matrix.columns:
        for j in tree_matrix.columns:
            if i != j:
                association_matrix.loc[i, j] = jaccard_index(tree_matrix[i], tree_matrix[j])

    # 使用seaborn生成热图
    # 确保没有 NaN 值（用 0 替换 NaN）
    association_matrix = association_matrix.fillna(0)
    # 强制转换数据类型为 float
    association_matrix = association_matrix.astype(float)
    plt.figure(figsize=(12, 10))
    sns.heatmap(association_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('树种种间联结热图 (Jaccard指数)')
    plt.xlabel('树种')
    plt.ylabel('树种')
    plt.show()

