import pandas as pd

# 读取Excel文件
file_path = r'C:\Users\hys5637428\Desktop\作业\大学生心理素质影响.xlsx'
data = pd.read_excel(file_path)

import numpy as np

df = pd.DataFrame(data)
df.index.name = '学生'  # 将索引列命名为'学生'
print("原始数据后五行：\n", df.tail())

# 提取特征列（排除索引列）
features = df[['家庭环境和家庭教育' , "学校生活环境" , "学校周围环境" , "个人向上发展心理动机"]]  # 类型为DataFrame

# 计算样本均值向量
mean_vector = features.mean()
print("\n样本均值向量：\n", mean_vector)

# 计算样本离差阵（Scatter Matrix）
n = features.shape[0]  # 样本量
centered_data = features - mean_vector  # 中心化数据
scatter_matrix = centered_data.T @ centered_data  # 矩阵乘法
# 等价于 np.dot(centered_data.T, centered_data)
print("\n样本离差阵：\n", scatter_matrix)

# 计算样本协方差矩阵（Covariance Matrix）
covariance_matrix = features.cov()
print("\n样本协方差矩阵：\n", covariance_matrix)

# 验证协方差矩阵 = 离差阵 / (n-1)
print("\n验证协方差矩阵正确性：",
      np.allclose(covariance_matrix, scatter_matrix/(n-1)))  # 应返回True

# 计算样本相关矩阵（Correlation Matrix）
correlation_matrix = features.corr()
print("\n样本相关矩阵：\n", correlation_matrix)


