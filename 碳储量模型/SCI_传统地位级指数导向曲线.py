import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.model_selection import train_test_split
import os

file_path = r'C:\Users\hys5637428\Desktop\模型拟合\使用数据.xls'
data = pd.read_excel(file_path)
df = data.copy()
#确保分母不为0
mask = df['SCI'] != 0
df = df.loc[mask]
#划分SCI
listBins = list(range(0, 29, 4))
listLabels = list(range(2,30 , 4))
df['SCI_int'] = None
df['SCI_int'] = pd.cut(df['SCI'], bins=listBins, labels=listLabels, include_lowest=True)
df_train,df_test=train_test_split(df,test_size=0.2,random_state=42)
df=df_train.copy()
years = df['年龄'].values
H=df['平均树高'].values
SCI=df['SCI_int'].values
# 确保 X 是一个二维 NumPy 数组
X = np.column_stack((years,H))
y=list(SCI)


# 自定义损失函数
def SCI_Logistic(params, X, y):
    a,b,c = params
    A0=50
    predictions = X[:,1]*(((1+c*np.exp(-b*X[:,0]))/a)/((1+c*np.exp(-b*A0))/a))
    return mean_squared_error(y, predictions)
def SCI_Mitscherlich(params, X, y):
    a,b= params
    A0=50
    predictions = X[:,1]*((a*(1-np.exp(-b*A0)))/(a*(1-np.exp(-b*X[:,0]))))
    return mean_squared_error(y, predictions)
def SCI_Chapman_Richards(params, X, y):
    a,b,c = params
    A0=50
    predictions = X[:, 1] * ((a*(1-np.exp(-b*A0))**c)/(a*(1-np.exp(-b*X[:,0]))**c))
    return mean_squared_error(y, predictions)
def SCI_Schumacher(params, X, y):
    a,b = params
    A0=50
    predictions =X[:, 1] * ((a*(np.exp(-b / A0))) / ((a*np.exp(-b / X[:, 0]))))
    return mean_squared_error(y, predictions)
def SCI_Korf(params, X, y):
    a,b,c = params
    A0 = 50
    predictions = X[:,1]*((a*np.exp(-b*(A0**(-c))))/(a*np.exp(-b*(X[:,0]**(-c)))))
    return mean_squared_error(y, predictions)
#参数值输出函数
def PARAMS(list,values,sheetname):
    # 创建参数名和值的字典
    params_dict = {
        '参数名': list,
        '值': values
    }
    # 转换为DataFrame
    df_params = pd.DataFrame(params_dict)
    out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
    out_path_pic = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
    df_params.to_excel(os.path.join(out_path, f'{sheetname}参数值.xlsx'), index=False)
# 优化和评估函数
def optimize_and_evaluate(function, initial_guess, X, y):
    result = minimize(function, initial_guess, args=(X, y))
    params = result.x
    if function == SCI_Mitscherlich:
        a, b = params
        best_predictions = X[:, 1] * ((a * (1 - np.exp(-b * 50))) / (a * (1 - np.exp(-b * X[:, 0]))))
        sheetname='SCI_Mitscherlich'
        list=['a','b']
        values=[a,b]
        PARAMS(list, values, sheetname)
    elif function == SCI_Logistic:
        a, b, c = params
        best_predictions = X[:, 1] * ((a / (1 + c * np.exp(-b * 50))) / (a / (1 + c * np.exp(-b * X[:, 0]))))
        sheetname = 'SCI_Logistic'
        list=['a','b','c']
        values = [a, b,c]
        PARAMS(list, values, sheetname)
    elif function == SCI_Chapman_Richards:
        a, b, c = params
        best_predictions = X[:, 1] * ((a * (1 - np.exp(-b * 50)) ** c) / (a * (1 - np.exp(-b * X[:, 0])) ** c))
        sheetname = 'SCI_Chapman_Richards'
        list = ['a', 'b', 'c']
        values = [a, b,c]
        PARAMS(list, values, sheetname)
    elif function == SCI_Schumacher:
        a, b = params
        best_predictions = X[:, 1] * ((a * (np.exp(-b / 50))) / (a * (np.exp(-b / X[:, 0]))))
        sheetname = 'SCI_Schumacher'
        list = ['a', 'b']
        values = [a, b]
        PARAMS(list, values, sheetname)
    elif function == SCI_Korf:
        a, b, c = params
        best_predictions = X[:, 1] * ((a * np.exp(-b * (50 ** (-c)))) / (a * np.exp(-b * (X[:, 0] ** (-c)))))
        sheetname = 'SCI_Korf'
        list = ['a', 'b', 'c']
        values = [a, b,c]
        PARAMS(list, values, sheetname)
    RGE_EvaluatingModelPerformance(y, best_predictions,len(params), sheetname)
    print(f'方程{function}params:{params}')
# 评估模型性能
def RGE_EvaluatingModelPerformance(y, best_predictions,p,sheetname):
    RSS = np.sum((best_predictions - y) ** 2)
    MSE = RSS/(len(y)-p)
    Sxy=np.sqrt(MSE)
    R2 = r2_score(y, best_predictions)
    #R2=1-SSE(残差平方和，模型预测值与实际观测值之间的差异)/SST(总平方和，Total Sum of Squares，实际观测值与其均值之间的差异)
    n=len(best_predictions)
    RSS_LIST=[]
    MSE_LIST=[]
    Sxy_LIST=[]
    R2_LIST=[]
    RSS_LIST.append(RSS)
    MSE_LIST.append(MSE)
    Sxy_LIST.append(Sxy)
    R2_LIST.append(R2)
    out_df = pd.DataFrame()
    out_df['剩余残差平方和'] =RSS_LIST
    out_df['剩余均方差'] = MSE_LIST
    out_df['剩余标准差'] = Sxy_LIST
    out_df['相关指数'] = R2_LIST
    print(f'剩余残差平方和: {RSS}')
    print(f'剩余均方差: {MSE}')
    print(f'剩余标准差: {Sxy}')
    print(f'相关指数: {R2}')
    out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
    out_df.to_excel(os.path.join(out_path, f'{sheetname}EvaluatingModelPerformance.xlsx'), index=False)
# 优化每个模型
function_list = [SCI_Logistic, SCI_Mitscherlich, SCI_Chapman_Richards, SCI_Schumacher, SCI_Korf]
initial_guess_list = [[13.4, 0.055, 3.7], [14.07, 0.029], [14.79, 0.023, 0.85], [15.15,17.08], [24.94, 6.07, 0.50]]
df1=df_test.copy()
years1 = df1['年龄'].values
H1=df1['平均树高'].values
SCI1=df1['SCI_int'].values
# 确保 X 是一个二维 NumPy 数组
X1 = np.column_stack((years1,H1))
y1=list(SCI1)
for func, guess in zip(function_list, initial_guess_list):
    print(f"\n优化 {func.__name__}")
    optimize_and_evaluate(func, guess, X1, y1)



