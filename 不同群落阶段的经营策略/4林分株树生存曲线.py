def even_slip(params, x, y):
    a,b= params
    predictions = a*np.exp(-b*x)
    return mean_squared_error(y, predictions)

def optimize_even_slip(function, initial_guess, x, y,bounds):
    result = minimize(function, initial_guess, args=(x, y),bounds=bounds)
    params = result.x
    return params
def RGE_EvaluatingModelPerformance(y, best_predictions,p):
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
    #print(f'剩余残差平方和: {RSS}')
    #print(f'剩余均方差: {MSE}')
    #print(f'剩余标准差: {Sxy}')
    print(f'相关指数: {R2}\n')
    return R2

import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import pandas as pd
import os
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\静态生命表'

name_list=os.listdir(file_path)
sheet_list=[['水曲柳','胡桃楸','色木','红松','春榆','裂叶榆','黄菠萝','紫椴'],
            ['紫椴','黄菠萝','大青杨','胡桃楸','冷杉','春榆','色木','水曲柳','糠椴'],
            ['水曲柳','糠椴','山杨','胡桃楸','黄菠萝','红松','紫椴','色木','春榆'],
             ['胡桃楸','冷杉','红松','山杨','黄菠萝','紫椴','糠椴','水曲柳','春榆','色木','白桦']]
k=0
for i in name_list:
    if i=='原始性次生林.xlsx':
        print(i)
        data_path = os.path.join(file_path, i)
        sheet_name = sheet_list[k]
        for j in sheet_name:
            data = pd.read_excel(data_path, sheet_name=j)
            df = data.copy()
            y = df['株树'].values
            x = df['径阶'].values
            initial_guess = [1, 1]
            bounds = [(0, None), (0, None)]
            a, b = optimize_even_slip(even_slip, initial_guess, x, y, bounds)
            print(f'{i, j}', a, b)
            best_predictions = a * np.exp(-b * x)
            R=RGE_EvaluatingModelPerformance(y, best_predictions, 2)
            x1 = range(2, max(x) + 2, 2)
            y1 = a * np.exp(-b * x1)
            plt.plot(x1, y1)
            plt.title(f'{i}:{j}\n{R}')
            plt.show()
            plt.clf()
        else:
            continue
    k+=1
