import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置随机种子以确保结果可重复
np.random.seed(42)

# 模拟数据
n_samples = 100  # 样地数量
n_functions = 3  # 功能数量
time_points = [1, 5, 10]  # 时间点
thresholds = np.linspace(0, 1, 100)  # 阈值范围

# 定义功能权重
weights = np.array([0.4, 0.3, 0.3])  # 木材生产、固碳功能、生物多样性

# 模拟不同时间点的功能值
def simulate_function_values(n_samples, n_functions, time_points):
    data = {}
    for t in time_points:
        # 随时间变化，功能值逐渐增加
        values = np.random.uniform(low=0.5 * t, high=1.0 * t, size=(n_samples, n_functions))
        # 标准化到0-1范围
        values = (values - np.min(values, axis=0)) / (np.max(values, axis=0) - np.min(values, axis=0))
        data[t] = values
    return data

# 计算多功能性
def calculate_multifunctionality(data, weights, thresholds):
    multifunctionality = {}
    for t, values in data.items():
        mf = []
        for threshold in thresholds:
            # 计算达到阈值的功能数量
            above_threshold = (values >= threshold).astype(int)
            # 加权求和
            mf.append(np.sum(above_threshold * weights, axis=1).mean())
        multifunctionality[t] = mf
    return multifunctionality

# 模拟功能值
data = simulate_function_values(n_samples, n_functions, time_points)

# 计算多功能性
multifunctionality = calculate_multifunctionality(data, weights, thresholds)

# 绘制图3：多功能性随阈值的变化
plt.figure(figsize=(10, 6))
for t, mf in multifunctionality.items():
    plt.plot(thresholds, mf, label=f'Year {t}')
plt.xlabel('Threshold')
plt.ylabel('Multifunctionality')
plt.title('Multifunctionality vs. Threshold')
plt.legend()
plt.grid(True)
plt.show()

# 绘制图4：多功能性随时间的动态变化
plt.figure(figsize=(10, 6))
for i, threshold in enumerate([0.3, 0.5, 0.7]):
    mf_values = [multifunctionality[t][i * 10] for t in time_points]  # 选择特定阈值下的多功能性
    plt.plot(time_points, mf_values, label=f'Threshold = {threshold}')
plt.xlabel('Time (Years)')
plt.ylabel('Multifunctionality')
plt.title('Multifunctionality Over Time at Different Thresholds')
plt.legend()
plt.grid(True)
plt.show()