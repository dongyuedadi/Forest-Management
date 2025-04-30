from matplotlib import pyplot as plt
from scipy.optimize import minimize,least_squares
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from scipy.stats import t

file_path = r'C:\Users\hys5637428\Desktop\模型拟合\使用数据.xls'
data = pd.read_excel(file_path)
df = data.copy()
# 确保分母不为0
mask = df['SCI'] != 0
df = df.loc[mask]
# 划分SCI
listBins = list(range(0, 29, 4))
listLabels = list(range(2, 30, 4))
df['SCI_int'] = None
df['SCI_int'] = pd.cut(df['SCI'], bins=listBins, labels=listLabels, include_lowest=True)
# 创建哑变量
df_dummies = pd.get_dummies(df, columns=['判别式2分组'])
bool_columns = df_dummies.select_dtypes(include=[bool])
df_dummies[bool_columns.columns] = bool_columns.astype(int)
df = df_dummies
# 创建测试子集
df, df_test = train_test_split(df, test_size=0.2, random_state=42)
# 哑变量s
s1 = df['判别式2分组_1'].values
s2 = df['判别式2分组_2'].values
s3 = df['判别式2分组_3'].values
years = df['年龄'].values
SDI = df['SDI']
SCI = df['SCI_int'].values
TH = df['平均树高'].values
CAR = df['碳储量'].values
Y_BAS = df['BAS'].values
X = np.column_stack((SCI, SDI, years, TH, s1, s2, s3, Y_BAS))
y = list(CAR)
X1 = np.column_stack((years, TH, s1, s2, s3))
y1 = list(SCI)


# a，b分别为对应第i个分区的参数，s1～s3为构造的哑变量。公式中参数c变化不大，因此没有构造哑变量
# 地位级指数模型参数预估
def SCI_Chapman_Richards(params, X1, y1):
    a1, a2, a3, b1, b2, b3, c = params
    s1, s2, s3 = X1[:, 2], X1[:, 3], X1[:, 4]
    a = a1 * s1 + a2 * s2 + a3 * s3
    b = b1 * s1 + b2 * s2 + b3 * s3
    A0 = 50
    predictions = X1[:, 1] * ((a * (1 - np.exp(-b * A0)) ** c) / (a * (1 - np.exp(-b * X1[:, 0])) ** c))
    return mean_squared_error(y1, predictions)


initial_guess = [14.79, 14.79, 14.79, 0.023, 0.023, 0.023, 0.85]
function = SCI_Chapman_Richards
bounds = [(0, None), (0, None), (0, None),(0, None),(0, None),(0, None),(0, None)]  # 对应 a, b, c 的边界
result = minimize(function, initial_guess, args=(X1, y1), bounds=bounds)
sciparams = result.x
scia1, scia2, scia3, scib1, scib2, scib3, scic = sciparams
# print(f'\nSCI-Evaluating Model Performance{scia1,scia2,scia3,scib1,scib2,scib3,scic}')
SDI_out=1535.1857966309715
# 胸高断面积碳储量联立方程组参数预估
def BAS_FUC(params, X, y):
    a0_1, a0_2, a0_3, a1, k0_1, k0_2, k0_3, k1, c = params
    # 在方程组中断面积预估模型中对参数a0和k0构造哑变量，最终方程组形式如下：
    a0 = a0_1 * X[:, 4] + a0_2 * X[:, 5] + a0_3 * X[:, 6]
    k0 = k0_1 * X[:, 4] + k0_2 * X[:, 5] + k0_3 * X[:, 6]
    best_predictions = a0 * (X[:, 0] ** a1) * (1 - np.exp((-k0) * ((X[:, 1] / 10000) ** k1) * X[:, 2])) ** c
    if np.isnan(best_predictions).any():
        print("Warning: Predictions contain NaN values!")
        # 可以选择返回一个特定的值或进行其他处理
        return np.nan  # 或者返回一个大的惩罚值，比如 1e10
    return best_predictions
def VOL_FUC(params, X, y):
    d0, d1 = params
    best_predictions = X[:, 7] * X[:, 3] * (d0 / (X[:, 3] + d1))
    return best_predictions

params1 = [19, 19, 19, 0.17, 4.6, 4.6, 4.6, 3.2, 0.3]
params2 = [9, 7]
initial_guess = np.concatenate((np.array(params1), np.array(params2)))

def residuals(params, X, y1, y2):
    y_pred_1 = BAS_FUC(params[:9], X, y1)
    y_pred_2 = VOL_FUC(params[9:], X, y2)
    return np.concatenate((y1 - y_pred_1, y2 - y_pred_2))
# 设置参数边界
bounds_lower = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bounds_upper = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
bounds = (bounds_lower, bounds_upper)
# 在优化过程中应用边界
result = least_squares(residuals, initial_guess, bounds=bounds, args=(X, Y_BAS, y))
#result = least_squares(residuals, initial_guess, args=(X, Y_BAS, y))
print("Optimized parameters:", result.x)
best_params = result.x
a0_1, a0_2, a0_3, a1, k0_1, k0_2, k0_3, k1, c = best_params[:9]
d0, d1 = best_params[9:]
# 创建参数名和值的字典
params_dict = {
    '参数名': ['a0_1', 'a0_2', 'a0_3', 'a1', 'k0_1', 'k0_2', 'k0_3', 'k1', 'c', 'd0', 'd1'],
    '值': [a0_1, a0_2, a0_3, a1, k0_1, k0_2, k0_3, k1, c, d0, d1]
}
# 转换为DataFrame
df_params = pd.DataFrame(params_dict)
out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
out_path_pic = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\pictures'
df_params.to_excel(os.path.join(out_path, '碳储量参数值.xlsx'), index=False)
# 速查表矩阵设置
dummies_list = [1, 2, 3]
a0_list = [a0_1 * 1, a0_2 * 1, a0_3 * 1]
k0_list = [k0_1 * 1, k0_2 * 1, k0_3 * 1]
scia_list = [scia1 * 1, scia2 * 2, scia3 * 3]
scib_list = [scib1 * 1, scib2 * 2, scib3 * 3]
Age = range(5, 101, 5)
SCI_list = range(8, 21, 2)

# 碳储量矩阵
with pd.ExcelWriter(r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\小兴安岭珍贵硬阔叶林碳储量速查表.xlsx',
                    engine='xlsxwriter') as writer:
    for s in dummies_list:
        a0 = a0_list[s - 1]
        k0 = k0_list[s - 1]
        scia = scia_list[s - 1]
        scib = scib_list[s - 1]
        CAR_matrix = np.zeros((len(Age), len(SCI_list)))
        for idx_age, val_age in enumerate(Age):
            for idx_i, val_i in enumerate(SCI_list):
                Height = val_i * (1 / (
                ((scia * (1 - np.exp(-scib * 50)) ** scic) / (scia * (1 - np.exp(-scib * val_age)) ** scic))))
                BAS = a0 * (val_i ** a1) * (1 - np.exp((-k0) * ((SDI_out / 10000) ** k1) * val_age)) ** c
                CAR_matrix[idx_age, idx_i] = BAS * Height * (d0 / (Height + d1))
        # print(f'\n哑变量{s}:小兴安岭珍贵硬阔叶林蓄积量速查表\n{BAS_matrix}')
        df_CAR_matrix = pd.DataFrame(CAR_matrix, index=Age, columns=SCI_list)
        sheet_name = f'哑变量{s}'
        df_CAR_matrix.to_excel(writer, sheet_name=sheet_name, index=True)
        for i in SCI_list:
            Height = i * (
                        1 / (((scia * (1 - np.exp(-scib * 50)) ** scic) / (scia * (1 - np.exp(-scib * Age)) ** scic))))
            BAS = a0 * (i ** a1) * (1 - np.exp((-k0) * ((SDI_out / 10000) ** k1) * Age)) ** c
            Volumes = BAS * 15 * (d0 / (15 + d1))
            plt.plot(Age, Volumes, label=f'SCI={i}')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylabel('碳储量/$t$', fontsize=14)
        plt.xlabel('年龄/years', fontsize=14)
        plt.legend(fontsize=10)
        # plt.title(f'碳储量:哑变量{s}——Chapman_Richards', fontsize=20)
        filename = f'碳储量哑变量_{s}_curve.png'
        plt.savefig(os.path.join(out_path_pic, filename))
        plt.show()
        plt.clf()


def EvaluatingModelPerformance(y, best_predictions, p, sheetname):
    ME = np.mean(y - best_predictions)
    MAE = np.mean(abs(y - best_predictions))
    MPE = np.mean((y - best_predictions) / y)
    MAPE = np.mean(abs((y - best_predictions) / y))
    R2 = r2_score(y, best_predictions)
    # R2=1-SSE(残差平方和，模型预测值与实际观测值之间的差异)/SST(总平方和，Total Sum of Squares，实际观测值与其均值之间的差异)
    n = len(best_predictions)
    t_critical_value = t.ppf(0.975, n - p - 1)
    Sy = np.sqrt(np.sum((y - best_predictions) ** 2) / (n * (n - p - 1)))
    ACCURACY = 1 - (t_critical_value * Sy) / np.mean(best_predictions)
    ME_LIST = []
    MAE_LIST = []
    MPE_LIST = []
    MAPE_LIST = []
    R2_LIST = []
    ACCURACY_LIST = []
    ME_LIST.append(ME)
    MAE_LIST.append(MAE)
    MPE_LIST.append(MPE)
    MAPE_LIST.append(MAPE)
    R2_LIST.append(R2)
    ACCURACY_LIST.append(ACCURACY)
    out_df = pd.DataFrame()
    out_df['平均偏差'] = ME_LIST
    out_df['均绝对偏差'] = MAE_LIST
    out_df['均相对偏差'] = MPE_LIST
    out_df['均相对绝对值偏差'] = MAPE_LIST
    out_df['相关指数'] = R2_LIST
    out_df['预测精度'] = ACCURACY_LIST
    print(f'Mean Error: {ME}')
    print(f'Mean Absolute Error: {MAE}')
    print(f'Mean Percentage Error: {MPE}%')
    print(f'Mean Absolute Percentage Error: {MAPE}%')
    print(f'R^2 Score: {R2}')
    print(f'Prediction Accuracy: {ACCURACY:.5f}')
    out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
    out_df.to_excel(os.path.join(out_path, f'{sheetname}EvaluatingModelPerformance.xlsx'), index=False)


s1 = df_test['判别式2分组_1'].values
s2 = df_test['判别式2分组_2'].values
s3 = df_test['判别式2分组_3'].values
years = df_test['年龄'].values
SDI = df_test['SDI']
SCI = df_test['SCI_int'].values
TH = df_test['平均树高'].values
Y_BAS = df_test['BAS'].values
Volumes = df_test['碳储量'].values
X = np.column_stack((SCI, SDI, years, TH, s1, s2, s3))
y = list(Volumes)
# 碳储量
a0 = a0_1 * X[:, 4] + a0_2 * X[:, 5] + a0_3 * X[:, 6]
k0 = k0_1 * X[:, 4] + k0_2 * X[:, 5] + k0_3 * X[:, 6]
BAS = a0 * (X[:, 0] ** a1) * (1 - np.exp((-k0) * ((X[:, 1] / 10000) ** k1) * X[:, 2])) ** c
best_predictions = BAS * X[:, 3] * (d0 / (X[:, 3] + d1))
print(f'\nBAS-VOL-Evaluating Model Performance{a0_1, a0_2, a0_3, a1, k0_1, k0_2, k0_3, k1, c, d0, d1}')
EvaluatingModelPerformance(y, best_predictions, len(best_params), sheetname='碳储量')
