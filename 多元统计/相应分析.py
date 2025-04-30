import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

# 中文显示配置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 数据预处理
df = pd.read_excel(r"C:\Users\hys5637428\Desktop\文献数据库\Belowground biomass of natural and planted forests in China.xlsx")
df.columns = df.columns.str.replace('[^A-Za-z0-9]+', '_', regex=True)

# 2. 数据清洗与分箱
selected_vars = ['Elevation', 'Forest_Age']
df_clean = df[selected_vars].dropna().copy()

# 分箱处理
df_clean['Elevation_bin'] = pd.qcut(df_clean['Elevation'], q=3,
                                   labels=['Low', 'Mid', 'High'],
                                   duplicates='drop')
df_clean['Forest_Age_bin'] = pd.qcut(df_clean['Forest_Age'], q=3,
                                    labels=['Young', 'Mature', 'Old'],
                                    duplicates='drop')

# 3. 构建列联表
contingency_table = pd.crosstab(
    df_clean['Elevation_bin'],
    df_clean['Forest_Age_bin'],
    margins=False
)

# 4. 卡方检验
chi2, p, dof, expected = chi2_contingency(contingency_table)
print(f"卡方值: {chi2:.2f}, p值: {p:.4f}")

# 5. 对应分析计算
std_residuals = (contingency_table - expected) / np.sqrt(expected + 1e-6)
svd = TruncatedSVD(n_components=2)
svd.fit(std_residuals)
# 获取坐标
row_coords = svd.transform(std_residuals)
col_coords = svd.components_.T * svd.singular_values_
print('row_coords', row_coords)
print('col_coords', col_coords)
# 6. 可视化（修复参数错误）
plt.figure(figsize=(10, 8))

# 绘制行点（海拔分箱）
for i in range(len(contingency_table.index)):
    x, y = row_coords[i, 0], row_coords[i, 1]
    plt.scatter(
        x, y,
        s=150,  # 固定大小参数
        marker='s',
        edgecolor='k',
        c=['#e41a1c','#377eb8','#4daf4a'][i],
        label=f'Elevation: {contingency_table.index[i]}'
    )
    plt.text(x+0.02, y+0.03, contingency_table.index[i],
            fontsize=12, ha='left', va='bottom')

# 绘制列点（林龄分箱）
for i in range(len(contingency_table.columns)):
    x, y = col_coords[i, 0], col_coords[i, 1]
    plt.scatter(
        x, y,
        s=150,  # 固定大小参数
        marker='D',
        edgecolor='k',
        c=['#ff7f00','#984ea3','#999999'][i],
        label=f'Forest Age: {contingency_table.columns[i]}'
    )
    plt.text(x+0.02, y+0.03, contingency_table.columns[i],
            fontsize=12, ha='left', va='bottom')

# 坐标轴标注
plt.xlabel(f"维度 1 ({svd.explained_variance_ratio_[0]*100:.1f}%)", fontsize=12)
plt.ylabel(f"维度 2 ({svd.explained_variance_ratio_[1]*100:.1f}%)", fontsize=12)
print(f"维度 1 ({svd.explained_variance_ratio_[0]*100:.1f}%)")
print(f"维度 2 ({svd.explained_variance_ratio_[1]*100:.1f}%)")
# 辅助元素
plt.axhline(0, color='gray', ls=':', alpha=0.7)
plt.axvline(0, color='gray', ls=':', alpha=0.7)
plt.grid(alpha=0.3)
plt.title("海拔与林龄对应分析双标图\np值={:.3f}".format(p), fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()