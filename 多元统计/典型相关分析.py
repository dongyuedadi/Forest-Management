import pandas as pd
import numpy as np
from sklearn.cross_decomposition import CCA
from scipy.stats import chi2
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

# 1. 数据读取
df = pd.read_excel(r"C:\Users\hys5637428\Desktop\文献数据库\Belowground biomass of natural and planted forests in China.xlsx")
df.columns = df.columns.str.replace('[^A-Za-z0-9]+', '_', regex=True)
df_clean = df.dropna()

# 2. 变量分组（根据生态学逻辑）
X_vars = [  # 环境因子组
    'Elevation',
    'Soil_N',
    'Soil_P',
    'MAT',
    'MAP',
    'Annual_average_sunshine_duration'
]

Y_vars = [  # 森林特征组
    'Species_Richness',
    'Forest_Age',
    'Average_DBH',
    'Forest_Density',
    'LA'
]

# 3. 数据标准化
scaler = StandardScaler()
X = scaler.fit_transform(df_clean[X_vars])
Y = scaler.fit_transform(df_clean[Y_vars])

# 4. 典型相关分析
n_components = min(len(X_vars), len(Y_vars))
cca = CCA(n_components=n_components)
cca.fit(X, Y)

# 5. 计算典型变量得分
X_c, Y_c = cca.transform(X, Y)

# 6. 计算典型相关系数
corr = [np.corrcoef(X_c[:, i], Y_c[:, i])[0, 1]
        for i in range(n_components)]

# 7. 打印载荷矩阵（新增部分）=============================================
print("\n=== 环境因子组（X）载荷 ===")
x_loadings = pd.DataFrame(
    cca.x_weights_,
    index=X_vars,
    columns=[f"CC{i+1}" for i in range(n_components)]
)
print(x_loadings.round(3))

print("\n=== 森林特征组（Y）载荷 ===")
y_loadings = pd.DataFrame(
    cca.y_weights_,
    index=Y_vars,
    columns=[f"CC{i+1}" for i in range(n_components)]
)
print(y_loadings.round(3))

# 8. 初始化结果数据框
result_df = pd.DataFrame(
    index=[f"Dimension {i + 1}" for i in range(n_components)],
    columns=['Canonical_Correlation', 'Wilks_Lambda',
             'Chi_Square', 'DF', 'p_value']
)

# 填充初始值
result_df['Canonical_Correlation'] = corr
n = X.shape[0]
p = len(X_vars)
q = len(Y_vars)

# 9. Bartlett卡方检验计算
for k in range(n_components):
    lam = np.prod([1 - r ** 2 for r in corr[k:]])
    df = (p - k) * (q - k)
    chi_stat = - (n - 1 - (p + q + 1) / 2) * np.log(lam)
    p_val = chi2.sf(chi_stat, df)

    result_df.iloc[k, 1:] = [lam, chi_stat, df, p_val]

print("\n典型相关分析结果:")
print(result_df.round(4))
# 计算环境因子对林分特征的效应量
effect_size = np.corrcoef(X_c[:,0], Y_c[:,0])[0,1]**2
print(f"第一典型变量解释方差: {effect_size:.1%}")
# 计算第二典型变量的相关系数平方（效应量）
effect_size_2 = np.corrcoef(X_c[:, 1], Y_c[:, 1])[0, 1]**2
print(f"第二典型变量解释方差: {effect_size_2:.1%}")

# 10. 可视化第一对典型变量
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_c[:, 0], Y_c[:, 0],
                      c=df_clean['Elevation'],
                      cmap='viridis',
                      alpha=0.7,
                      edgecolor='k')
plt.colorbar(scatter, label='Elevation (m)')
plt.xlabel(f'X Canonical Variable 1 (r={corr[0]:.2f})')
plt.ylabel(f'Y Canonical Variable 1 (r={corr[0]:.2f})')
plt.title('First Canonical Pair with Elevation')
plt.grid(ls='--', alpha=0.5)
plt.tight_layout()
plt.show()
