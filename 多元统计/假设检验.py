import numpy as np
import pandas as pd
from scipy import stats
# 读取Excel文件
file_path = r'C:\Users\hys5637428\Desktop\作业\大学生心理素质影响.xlsx'
data = pd.read_excel(file_path)
df = pd.DataFrame(data)
df.index.name = '学生'

# 参数设置
mu0 = np.array([7, 5, 4, 8])    # 假设的总体均值向量
alpha = 0.05                    # 显著性水平
features = df[['家庭环境和家庭教育' , "学校生活环境" , "学校周围环境" , "个人向上发展心理动机"]]

# 计算关键统计量
n = features.shape[0]            # 样本量
p = features.shape[1]            # 变量数 p=4
sample_mean = features.mean().values  # 样本均值向量 [84.2, 83.4, 80.6, 78.2]
S = features.cov().values        # 样本协方差矩阵 (4x4)

# 检验计算 ------------------------------------------------
# 1. 计算均值偏差向量
delta = sample_mean - mu0        # [84.2-7, 83.4-5, 80.6-4, 78.2-8] = [77.2, 78.4, 76.6, 70.2]

# 2. 计算Hotelling's T²统计量
S_inv = np.linalg.inv(S)        # 协方差矩阵的逆
T_squared = n * delta.T @ S_inv @ delta  # 矩阵运算计算T²值

# 3. 转换为F统计量
F_stat = (T_squared * (n - p)) / (p * (n - 1))

# 4. 计算临界值和p值
F_crit = stats.f.ppf(1 - alpha, p, n - p)  # 临界值
p_value = 1 - stats.f.cdf(F_stat, p, n - p)

# 结果输出 ------------------------------------------------
print(f"样本均值向量: {sample_mean.round(2)}")
print(f"假设均值向量: {mu0}")
print("\n-- 检验统计量 --")
print(f"Hotelling's T² = {T_squared:.2f}")
print(f"F统计量 = {F_stat:.2f} (自由度={p}, {n-p})")
print(f"临界值 F_crit({alpha}) = {F_crit:.2f}")
print(f"p值 = {p_value:.5f}")

print("\n-- 检验结论 --")
if F_stat > F_crit:
    print(f"拒绝H0 (F统计量 > 临界值)")
else:
    print(f"未能拒绝H0")
if p_value < alpha:
    print(f"拒绝H0 (p值 < α)")
else:
    print(f"未能拒绝H0 (p值 ≥ α)")