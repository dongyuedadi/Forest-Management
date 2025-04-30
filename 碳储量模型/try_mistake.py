import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from scipy.optimize import curve_fit
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# 文件路径
file_path = r'C:\Users\hys5637428\Desktop\模型拟合\使用数据(1).xls'

# 读取数据并删除包含 NaN 的行
data = pd.read_excel(file_path)
df = data[['株数', '目标树2占比', '年龄']].copy()  # 使用 copy() 避免 SettingWithCopyWarning
df.dropna(axis=0, how='any', inplace=True)

# 选择自变量和因变量
X1 = 1-1/df['目标树2占比']  # 自变量 1
X2 = df['年龄']        # 自变量 2
y = np.log(df['株数'])         # 因变量

# 线性回归模型
linear_model = LinearRegression()
linear_model.fit(df[['目标树2占比', '年龄']], y)
y_pred_linear = linear_model.predict(df[['目标树2占比', '年龄']])
mse_linear = mean_squared_error(y, y_pred_linear)
r2_linear = r2_score(y, y_pred_linear)

# 非线性回归模型
def nonlinear_model(X, α, β1, β2):
    X1, X2 = X
    return α*(X2)**β2
X = (df['目标树2占比'], df['年龄'])
params, _ = curve_fit(nonlinear_model, X, y, p0=[1.0, 0.01, 1.0], maxfev=10000)
y_pred_nonlinear = nonlinear_model(X, *params)
mse_nonlinear = mean_squared_error(y, y_pred_nonlinear)
r2_nonlinear = r2_score(y, y_pred_nonlinear)

# 多项式回归模型 (2 次)
degree = 2
poly_model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
poly_model.fit(df[['目标树2占比', '年龄']], y)
y_pred_poly = poly_model.predict(df[['目标树2占比', '年龄']])
mse_poly = mean_squared_error(y, y_pred_poly)
r2_poly = r2_score(y, y_pred_poly)

# 模型比较
print("线性回归模型:")
print(f"系数: {linear_model.coef_}")
print(f"截距: {linear_model.intercept_}")
print(f"均方误差 (MSE): {mse_linear:.4f}")
print(f"R²: {r2_linear:.4f}")

print("\n非线性回归模型:")
print(f"优化后的参数: α = {params[0]:.4f}, β1 = {params[1]:.4f}, β2 = {params[2]:.4f}")
print(f"均方误差 (MSE): {mse_nonlinear:.4f}")
print(f"R²: {r2_nonlinear:.4f}")

print("\n多项式回归模型 (2 次):")
print(f"均方误差 (MSE): {mse_poly:.4f}")
print(f"R²: {r2_poly:.4f}")

print("\n模型比较:")
print(f"线性回归模型 - MSE: {mse_linear:.4f}, R²: {r2_linear:.4f}")
print(f"非线性回归模型 - MSE: {mse_nonlinear:.4f}, R²: {r2_nonlinear:.4f}")
print(f"多项式回归模型 (2 次) - MSE: {mse_poly:.4f}, R²: {r2_poly:.4f}")