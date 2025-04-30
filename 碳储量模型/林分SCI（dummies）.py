import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
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
# 创建哑变量
df_dummies = pd.get_dummies(df, columns=['判别式2分组'])
bool_columns = df_dummies.select_dtypes(include=[bool])#选择布尔类型的列
df_dummies[bool_columns.columns] = bool_columns.astype(int)#将布尔列转换为整型列
df= df_dummies
years = df['年龄'].values
H=df['平均树高'].values
SCI=df['SCI_int'].values
#哑变量s
s1=df['判别式2分组_1'].values
s2 = df['判别式2分组_2'].values
s3=df['判别式2分组_3'].values
# 确保 X 是一个二维 NumPy 数组
X = np.column_stack((years,H,s1,s2,s3))
y=list(SCI)
#a，b分别为对应第i个分区的参数，s1～s3为构造的哑变量。公式中参数c变化不大，因此没有构造哑变量
def SCI_Chapman_Richards(params, X, y):
    a1,a2,a3,b1,b2,b3,c= params
    s1, s2, s3 = X[:,2], X[:,3], X[:,4]
    a=a1*s1+a2*s2+a3*s3
    b=b1*s1+b2*s2+b3*s3
    A0=50
    predictions = X[:, 1] * ((a*(1-np.exp(-b*A0))**c)/(a*(1-np.exp(-b*X[:,0]))**c))
    return mean_squared_error(y, predictions)
initial_guess=[17,17,17, 0.023, 0.023,0.023,0.7]
function = SCI_Chapman_Richards
bounds = [(0, None), (0, None), (0, None),(0, None),(0, None),(0, None),(0, None)]  # 对应 a, b, c 的边界
result = minimize(function, initial_guess, args=(X, y), bounds=bounds)
#result = minimize(function, initial_guess, args=(X, y))
params = result.x
a1,a2,a3,b1,b2,b3,c= params
# 创建参数名和值的字典
params_dict = {
    '参数名': ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c'],
    '值': [a1,a2,a3,b1,b2,b3,c]
}
# 转换为DataFrame
df_params = pd.DataFrame(params_dict)
out_path = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out'
out_path_pic = r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\pictures'
df_params.to_excel(os.path.join(out_path, 'SCI参数值.xlsx'), index=False)

s1, s2, s3 = X[:, 2], X[:, 3], X[:, 4]
a = a1 * s1 + a2 * s2 + a3 * s3
b = b1 * s1 + b2 * s2 + b3 * s3
best_predictions = X[:, 1] * ((a * (1 - np.exp(-b * 50)) ** c) / (a * (1 - np.exp(-b * X[:, 0])) ** c))
a1=[a1 * 1 ,a2 * 1 , a3 * 1]
b1=[ b1 * 1 , b2 * 1 ,b3 * 1]

SCI_list=df['SCI_int'].unique()
dummies_list=[1,2,3]
Age=range(5,101,5)
SCI_list=range(8,21,2)
# 创建一个 ExcelWriter 对象，指定输出文件路径
with pd.ExcelWriter(r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\小兴安岭珍贵硬阔叶林树高速查表.xlsx',
                    engine='xlsxwriter') as writer:
    for s in dummies_list:
        a=a1[s-1]
        b=b1[s-1]
        Height_matrix = np.zeros((len(Age), len(SCI_list)))
        for idx_age, val_age in enumerate(Age):
            for idx_i, val_i in enumerate(SCI_list):
                Height_matrix[idx_age, idx_i] = val_i * (
                        1 / ((a * (1 - np.exp(-b * 50)) ** c) / (a * (1 - np.exp(-b * val_age)) ** c))
                )
        df_Height_matrix = pd.DataFrame(Height_matrix, index=Age, columns=SCI_list)
        sheet_name=f'哑变量{s}'
        df_Height_matrix.to_excel(writer, sheet_name=sheet_name, index=True)
        for i in SCI_list:
            Height=i*(1/(  ((a * (1 - np.exp(-b * 50)) ** c) / (a * (1 - np.exp(-b * Age)) ** c))))
            plt.plot(Age, Height, label=f'SCI={i}')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylabel('树高/m',fontsize=14)
        plt.xlabel('年龄/years',fontsize=14)
        plt.legend(fontsize=10)
        #plt.title(f'地位级指数曲线:哑变量{s}——Chapman_Richards', fontsize=20)
        filename = f'SCI哑变量_{s}_curve.png'
        plt.savefig(os.path.join(out_path_pic, filename))
        plt.show()
        plt.clf()