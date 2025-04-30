import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler

# 提取特征数据，从`林分密度`到`优势草本占比`列
# 读取数据
file_path = 'C:/Users/hys5637428/Desktop/多功能性-数据.xlsx'
df = pd.read_excel(file_path)
X = df.loc[:, '林分密度':'优势草本占比']
# 计算变量之间的相关系数矩阵
correlation_matrix = X.corr()

# 查看相关系数矩阵
print(correlation_matrix)
# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 将标准化后的数据转换回 DataFrame 格式
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# 计算每个变量的 VIF 值
vif = pd.DataFrame()
vif["Variable"] = X_scaled_df.columns
vif["VIF"] = [variance_inflation_factor(X_scaled_df.values, i) for i in range(X_scaled_df.shape[1])]

# 筛选出 VIF 值大于 10 的变量（显著相关的变量）
significant_vars = vif[vif['VIF'] > 10]

print("各变量的 VIF 值：")
print(vif)
print("\n存在显著多重共线性的变量：")
print(significant_vars)