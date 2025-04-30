from matplotlib import pyplot as plt
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.stats import t
import os

file_path = r'C:\Users\hys5637428\Desktop\模型拟合\使用数据.xls'
out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
data = pd.read_excel(file_path)
df = data.copy()
QI_list=['株数','平均直径','年龄','SCI']
def Quantile_text(QI_LIST):
    for QI in QI_list:
        # 异常值检测
        # 计算下四分位数和上四分位数
        Q1 = df[QI].quantile(q=0.25)
        Q3 = df[QI].quantile(q=0.75)
        # 基于1.5倍四分位差计算上下须对应的值
        low_whisker = Q1 - 1.5 * (Q3 - Q1)
        high_whisker = Q3 + 1.5 * (Q3 - Q1)
        # 寻找异常点
        outliers = df[QI][(df[QI] > high_whisker) | (df[QI] < low_whisker)]
        print('异常值\n{}、\n下四分位数\n{}\n上四分位数\n{}'.format(outliers, low_whisker, high_whisker))
        index_list = outliers.index
        df.drop(index=index_list, axis=0, inplace=True)  # 删除异常值所在行
Quantile_text(QI_list)

#创建测试子集
df,df_test=train_test_split(df,test_size=0.2,random_state=42)
#df.to_excel(os.path.join(out_path, '最大密度线删选后数据.xlsx'), index=False)
#确保分母不为0
mask = df['SDI'] != 0
df = df.loc[mask]
mask = df['年龄'] != 0
df = df.loc[mask]

SDI=df['SDI'].values
DBH=df['平均直径'].values
N=df['株数'].values
X=np.log(DBH)
y=np.log(N)
SCI=df['SCI'].values
years=df['年龄'].values


def SDI_FUNCTION(params, X, y):
    α,β=params
    predictions=np.log(α)+β*X
    return mean_squared_error(y, predictions)
initial_guess=[11,-0.9417]
function = SDI_FUNCTION
result = minimize(function, initial_guess, args=(X, y))
params = result.x
α,β=params
# 创建参数名和值的字典
params_dict = {
    '参数名': ['α', 'β'],
    '值': [α,β]
}
# 转换为DataFrame
df_params = pd.DataFrame(params_dict)
out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
df_params.to_excel(os.path.join(out_path, '最大密度线参数值.xlsx'), index=False)
print(f'\nSDI-Evaluating Model Performance{α,β=}')
#最大密度线图
X1=range(5,100,1)
predictions=np.log(α)+β*np.log(X1)
plt.scatter(np.log(DBH), y)
plt.plot(np.log(X1), predictions)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('ln(N)', fontsize=14)
plt.xlabel('ln(D)', fontsize=14)
#plt.title(f'最大密度线', fontsize=20)
plt.show()
plt.clf()

    
def EvaluatingModelPerformance(y, best_predictions,p,sheetname):
    ME = np.mean(y - best_predictions)
    MAE = np.mean(abs(y - best_predictions))
    MPE=np.mean((y - best_predictions)/y)
    MAPE=np.mean(abs((y - best_predictions)/y))
    R2 = r2_score(y, best_predictions)
    #R2=1-SSE(残差平方和，模型预测值与实际观测值之间的差异)/SST(总平方和，Total Sum of Squares，实际观测值与其均值之间的差异)
    n=len(best_predictions)
    t_critical_value = t.ppf(0.975, n-p-1)
    Sy=np.sqrt(np.sum((y-best_predictions)**2)/(n*(n-p-1)))
    ACCURACY =1-(t_critical_value*Sy)/np.mean(best_predictions)
    ME_LIST=[]
    MAE_LIST=[]
    MPE_LIST = []
    MAPE_LIST = []
    R2_LIST=[]
    ACCURACY_LIST=[]
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

print(f'\nSDI-Evaluating Model Performance{α,β=}')
DBH=df_test['平均直径'].values
N=df_test['株数'].values
X3=DBH
y3=np.log(N)
best_predictions=np.log(α)+β*np.log(X3)
print('\nSDI-最大密度线Evaluating Model Performance')
EvaluatingModelPerformance(y3,best_predictions,len(params),sheetname='SDI')


