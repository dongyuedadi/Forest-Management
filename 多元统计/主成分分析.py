import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据（注意转义问题）
file_path = r'C:\Users\hys5637428\Desktop\毕业论文\工作簿1.xlsx'
df = pd.read_excel(file_path, index_col='植物属名')  # 关键修改：将森林类型设为索引

# 数据清洗（处理特殊符号和缺失值）
df = df.replace('—', 0).astype(float)
# 数据标准化
x_std = StandardScaler().fit_transform(df.values)

# 主成分分析
pca = PCA(n_components=2)
principal_components = pca.fit_transform(x_std)

# 构建结果数据框
loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i+1}' for i in range(2)],
    index=df.columns  # 植物属名称作为特征
)

explained_var = pca.explained_variance_ratio_
components_df = pd.DataFrame(
    principal_components,
    columns=[f'PC{i+1}' for i in range(2)],
    index=df.index  # 森林类型作为样本标签
)

# 结果输出
print("================= 主成分分析报告 =================")
print("\n一、方差解释比例：")
print(pd.DataFrame(explained_var,
                  index=loadings.columns,
                  columns=['方差贡献率']))

print("\n二、主成分组成因素（因子载荷矩阵）：")
print(loadings)

print("\n三、森林类型主成分得分：")
print(components_df)

# 可视化（森林类型分布）

plt.figure(figsize=(12, 8))
plt.scatter(principal_components[:,0], principal_components[:,1], s=150)

# 标注森林类型
for i, forest in enumerate(df.index):
    plt.annotate(forest,
                (principal_components[i,0]+0.1, principal_components[i,1]+0.1),
                fontsize=9)

# 绘制特征载荷箭头
for j, feature in enumerate(df.columns):
    plt.arrow(0, 0,
             loadings.loc[feature, 'PC1']*8,  # 箭头长度缩放系数
             loadings.loc[feature, 'PC2']*8,
             color='r',
             alpha=0.5,
             head_width=0.1)
    plt.text(loadings.loc[feature, 'PC1']*8.5,
            loadings.loc[feature, 'PC2']*8.5,
            feature,
            color='darkred')

plt.xlabel(f'PC1 ({explained_var[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({explained_var[1]*100:.1f}%)')
plt.title('森林类型主成分空间分布（含特征载荷向量）')
plt.grid(True)
plt.show()

# 特征重要性分析
print("\n四、关键特征解读：")
top_features = loadings.abs().sum(axis=1).sort_values(ascending=False)[:5]
print(f"最具解释力的植物属：{', '.join(top_features.index.tolist())}")