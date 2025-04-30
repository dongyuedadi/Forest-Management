import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r'C:\Users\hys5637428\Desktop\模型拟合\黑龙江地方2010_2015年一类样地数据.xlsx'
data = pd.read_excel(file_path)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False
df = data.copy()
Slope_Aspect= df['坡向'].values
Slope_Position= df['坡位'].values
DBH1=df['bas1'].values
fig=plt.figure(figsize=(10,6))
ax=plt.subplot(1, 2, 1)
fig.add_subplot(ax)
sns.boxplot(y='bas1',x='坡位',hue='坡向',data=df)
ax1=plt.subplot(1, 2, 2)
fig.add_subplot(ax1)
ax1.boxplot(DBH1,showfliers=True)
ax1.set_xticks([1])
ax1.set_xticklabels(['bas1'])
plt.show()

#异常值检测
#计算下四分位数和上四分位数
Q1=df['bas1'].quantile(q=0.25)
Q3=df['bas1'].quantile(q=0.75)
#基于1.5倍四分位差计算上下须对应的值
low_whisker=Q1-1.5*(Q3-Q1)
high_whisker=Q3+1.5*(Q3-Q1)
print('Q1:{}\n'.format(Q1))
print('Q3:{}\n'.format(Q3))
#寻找异常点
outliers = df['bas1'][(df['bas1'] > high_whisker) | (df['bas1'] < low_whisker)]
print('异常值\n{}、\n下四分位数\n{}\n上四分位数\n{}'.format(outliers,low_whisker,high_whisker))
index_list=outliers.index
#df['bas1'].drop(index_list,inplace=True)#删除异常值
#df['bas1'].fillna(value=np.mean(df['bas1']),inplace=True)#空值填充
df.drop(index=index_list,axis=0,inplace=True)#删除异常值所在行
Q1=df['bas1'].quantile(q=0.25)
Q3=df['bas1'].quantile(q=0.75)
#基于1.5倍四分位差计算上下须对应的值
low_whisker=Q1-1.5*(Q3-Q1)
high_whisker=Q3+1.5*(Q3-Q1)
print('剔除异常点后')
print('Q1:{}\n'.format(Q1))
print('Q3:{}\n'.format(Q3))
#寻找异常点
outliers = df['bas1'][(df['bas1'] > high_whisker) | (df['bas1'] < low_whisker)]
print('异常值\n{}、\n下四分位数\n{}\n上四分位数\n{}'.format(outliers,low_whisker,high_whisker))
print(np.sum(df.isnull(),axis=0))
