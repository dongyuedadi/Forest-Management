import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 设置字体和路径
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'

# 读取数据
name_list = os.listdir(file_path)
tree_data = []

for i in name_list:
    data_path = os.path.join(file_path, i)
    df = pd.read_excel(data_path, sheet_name='每木检尺及测高记录表')
    tree_counts = df['树种'].value_counts()
    tree_data.extend(list(zip(tree_counts.index, tree_counts.values)))

# 将数据转换为DataFrame并排序
tree_df = pd.DataFrame(tree_data, columns=['树种', '多度'])
tree_df = tree_df.sort_values(by='多度', ascending=False).reset_index(drop=True)

# 定义生态位优先模型函数
def niche_model(i, k):
    return k * (1 - k)**(i - 1)

# 准备数据用于拟合
i_values = np.arange(1, len(tree_df) + 1)  # 假设数据已经按照优势度顺序排列
y_values = tree_df['多度'].values

# 使用非线性优化来拟合模型
popt, pcov = curve_fit(niche_model, i_values, y_values, p0=[0.5])  # 初始猜测k=0.5
k_fitted = popt[0]

# 打印拟合的k值
print(f"拟合的k值: {k_fitted}")

# 生成拟合曲线的数据
i_fit = np.linspace(1, len(tree_df), 100)  # 用于绘制平滑曲线的点
y_fit = niche_model(i_fit, k_fitted)

# 绘制原始数据和拟合曲线
plt.figure(figsize=(10, 6))
plt.bar(tree_df['树种'], tree_df['多度'], label='实际数据')
plt.plot(tree_df['树种'], y_fit[:len(tree_df)], 'r--', label='拟合曲线')  # 注意这里我们只取前len(tree_df)个点来匹配实际数据长度
plt.xlabel('树种')
plt.ylabel('多度')
plt.title('各树种多度分布及拟合曲线')
plt.xticks(rotation=45, ha='right')  # 旋转x轴标签并右对齐
plt.legend()
plt.tight_layout()
plt.show()