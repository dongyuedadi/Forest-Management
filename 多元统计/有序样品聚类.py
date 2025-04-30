import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def elbow_method(data, max_clusters=10):

    wcss = []
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, n_init=10, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)

    # 自动检测拐点
    deltas = np.diff(wcss)
    acceleration = np.diff(deltas)
    optimal_k = np.argmin(acceleration)

    # 可视化
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), wcss, 'b-', marker='o')
    plt.axvline(x=optimal_k, color='r', linestyle='--')
    plt.title('肘部法则 - K值选择')
    plt.xlabel('聚类数 K')
    plt.ylabel('组内平方和 (WCSS)')
    plt.grid(True)
    plt.show()

    return optimal_k
# 读取数据
df = pd.read_excel(r'C:\Users\hys5637428\Desktop\伊春土壤分层数据.xlsx')

# 选择特征列
features = ['SOM', 'TN', 'TP', 'BD']  # 根据实际列名调整
X = df[features].copy()

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 创建顺序约束矩阵（保证相邻样本才能合并）
n_samples = len(df)
connectivity = np.zeros((n_samples, n_samples))
for i in range(n_samples-1):
    connectivity[i, i+1] = 1
    connectivity[i+1, i] = 1

# 执行有序层次聚类
cluster = AgglomerativeClustering(
    n_clusters=elbow_method(X_scaled),           # 聚类数量
    metric='euclidean',   # 距离度量
    linkage='ward',         # 连接方法
    connectivity=connectivity  # 顺序约束
)
df['Cluster'] = cluster.fit_predict(X_scaled)


# 打印聚类统计特征
print("\n聚类特征统计：")
stats = df.groupby('Cluster')[features].agg(['mean', 'std'])
print(stats.round(2))

# 保存结果
df.to_excel(r'C:\Users\hys5637428\Desktop\伊春土壤分层聚类结果.xlsx', index=False)
print("\n聚类结果已保存至Excel文件")