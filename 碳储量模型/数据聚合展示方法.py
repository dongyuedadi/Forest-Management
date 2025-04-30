import pandas as pd
import numpy as np

file_path = r'C:\Users\hys5637428\Desktop\模型拟合\黑龙江地方2010_2015年一类样地数据.xlsx'
data = pd.read_excel(file_path)
df = data.copy()
#
df_groupby = df.groupby(['年代1', '区域码'])['bas1'].sum()
print('grounby:'df_groupby)
#
df_agg=df.agg({'SCI1':'sum'})
print('\n agg:',df_agg)
#
# 注意：这里的 filter 是 GroupBy 对象的方法，不是 DataFrame 的方法
grouped = df.groupby(['年代1', '区域码'])
df_filter = grouped.filter(lambda x: x['面积'].sum() < 0)
print('\n filter:',df_filter)
#
df_filter = df[(df['面积'] < 0.06)|(df['面积'] > 0.06)]
print(df_filter)
#
pivot_data=pd.pivot_table(df,index=['年代1','区域码','坡位'],values=['bas1'],columns=['坡度'],aggfunc=np.sum,fill_value=0)
print(pivot_data)