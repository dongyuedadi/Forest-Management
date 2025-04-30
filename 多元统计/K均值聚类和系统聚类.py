import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 数据加载与预处理
df = pd.read_excel(r"C:\Users\hys5637428\Desktop\土壤性质结果.xlsx")

# 选择特征变量
variables = ['SOM_mean', 'TN_mean','TP_mean','TK_mean','BD_mean']
X = df[variables]

# 标准化处理
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# 2. 系统聚类核心逻辑
def hierarchical_clustering(data, labels):
    # 计算链接矩阵
    Z = linkage(data, method='ward', optimal_ordering=True)
    # 自动确定最佳聚类数
    last_merges = Z[-10:, 2]
    diffs = np.diff(last_merges)[::-1]
    optimal_clusters = diffs.argmax() + 2
    # 获取聚类标签
    hc_labels = fcluster(Z, optimal_clusters, criterion='maxclust')
    # 打印系统聚类结果
    print("\n=== 系统聚类结果 ===")
    cluster_report = pd.DataFrame({
        '区域': labels,
        'Cluster': hc_labels
    })
    print(cluster_report.groupby('Cluster')['区域'].value_counts().unstack().fillna(0).astype(int))

    return hc_labels


# 3. K均值聚类核心逻辑
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
def kmeans_clustering(data, labels):
    # 肘部法选择最佳K值
    best_k = elbow_method(X_scaled, max_clusters=8)
    kmeans = KMeans(n_clusters=best_k, n_init=10, random_state=42)
    km_labels = kmeans.fit_predict(data)

    # 打印K均值聚类结果
    print("\n=== K均值聚类结果 ===")
    cluster_report = pd.DataFrame({
        '区域': labels,
        'Cluster': km_labels
    })
    print(cluster_report.groupby('Cluster')['区域'].value_counts().unstack().fillna(0).astype(int))

    return km_labels


# 4. 执行聚类分析
if __name__ == "__main__":
    # 系统聚类
    hc_labels = hierarchical_clustering(X_scaled, df['区域'].values)

    # K均值聚类
    km_labels = kmeans_clustering(X_scaled, df['区域'].values)

