import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

file_path = r'C:\Users\hys5637428\Desktop\模型拟合\黑龙江地方2010_2015年一类样地数据.xlsx'
data = pd.read_excel(file_path)
df = data.copy()
SCI = df['SCI1'].values
SDI = df['SDI1'].values
t = df['年龄1'].values
BAS = df['bas1'].values

# 确保 X 是一个二维 NumPy 数组
X = np.column_stack((SCI, SDI, t))
y = BAS
# 自定义损失函数
def loss_function(params, X, y):
    a, ao, b1, bo, c = params
    predictions = a * X[:, 0] ** ao * (1 - np.exp(-b1 * (X[:, 1] / 10000) ** bo)) * X[:, 2] ** c
    return mean_squared_error(y, predictions)

# 初始参数猜测
initial_guess = [1, 1, 1, 1, 1]
# 优化
result = minimize(loss_function, initial_guess, args=(X, y))
# 最佳拟合参数
best_params = result.x
#.x后面的x并不是指某个特定的数学变量或参数名，而是一个属性名，用于访问优化结果中的参数值
#这个命名约定在scipy.optimize模块中是标准的，用于区分其他可能包含在OptimizeResult对象中的信息，
# 比如.fun（最终的目标函数值）、.success（是否成功找到最小值）、.message（关于优化过程的额外信息）等
# 解构最佳拟合参数
a, ao, b1, bo, c = best_params
# 预测（使用最佳拟合参数）
best_predictions = a * X[:, 0] ** ao * (1 - np.exp(-b1 * (X[:, 1] / 10000) ** bo)) * X[:, 2] ** c
# 评估模型性能
mse = mean_squared_error(y, best_predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y, best_predictions)#Coefficient of Determination
#R2=1-SSE(残差平方和，模型预测值与实际观测值之间的差异)/SST(总平方和，Total Sum of Squares，
# 实际观测值与其均值之间的差异)
mape = np.mean(np.abs((y - best_predictions) / y)) * 100
#abs是绝对值函数（Absolute Value Function）
accuracy = 1 - mape / 100

print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')
print(f'R^2 Score: {r2}')
print(f'Mean Absolute Percentage Error: {mape}%')
print(f'Prediction Accuracy: {accuracy:.2f}')