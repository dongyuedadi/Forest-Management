import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import  r2_score
from scipy.stats import t
#忽略numpy的特定类型警告
np.seterr(all='ignore')
# 加载数据
file_path = r'C:\Users\hys5637428\Desktop\模型拟合\使用数据.xls'
out_path_pic = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\pictures'
out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
data = pd.read_excel(file_path)
df = data.copy()
df,df_test=train_test_split(df,test_size=0.2,random_state=42)
# 过滤掉SDI为0的行
mask = df['SDI'] != 0
df = df.loc[mask]
# 提取变量
SDI = df['SDI'].values
DBH = df['平均直径'].values
N = df['株数'].values
X =np.log(DBH)
y = np.log(N)  # 使用对数变换后的N作为响应变量
# 添加常数项以拟合截距
X_with_const = sm.add_constant(X)
# 定义要拟合的分位数
quantiles = [0.90, 0.95, 0.9625]
# 存储每个分位数的回归结果
results = {}
 # 对每个分位数进行回归
for quantile in quantiles:
    model = QuantReg(y, X_with_const)
    result = model.fit(q=quantile)
    # 存储结果
    results[quantile] = result
    # 最大密度线图
    α, β = result.params
    α_log=np.exp(α)
    # 创建参数名和值的字典
    params_dict = {
        '参数名': ['α', 'β'],
        '值': [α, β]
    }
    # 转换为DataFrame
    df_params = pd.DataFrame(params_dict)
    df_params.to_excel(os.path.join(out_path, f'分位数{quantile}回归参数值.xlsx'), index=False)
    X1 = range(5, 100, 1)
    predictions = α + β * np.log(X1)
    plt.scatter(np.log(DBH), y)
    plt.plot(np.log(X1), predictions)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel('ln(N)', fontsize=14)
    plt.xlabel('ln(D)', fontsize=14)
    # plt.title(f'最大密度线', fontsize=20)
    filename = f'Quantile {quantile} regression_curve.png'
    plt.savefig(os.path.join(out_path_pic, filename))
    plt.show()
    plt.clf()
    # 输出回归系数和摘要
    print(f"Quantile {quantile} regression coefficients:")
    print(result.params)
    print(result.summary())

SDI_values=α_log*15**β
print(SDI_values)



