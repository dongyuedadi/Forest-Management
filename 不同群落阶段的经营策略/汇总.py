import pandas as pd
import os

# 定义文件路径和工作表名称
file_path =  r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
file_path1 =  r'C:\Users\hys5637428\Desktop\不同阶段经营模式\标准化静态生命表'
name_list = ['各树种树高胸径标准差.xlsx', '竞争指数树种均值.xlsx', '密集度和成层性树种均值.xlsx',
             '空间结构指数树种均值.xlsx','树种大中小径木蓄积.xlsx','林分大中小径木株树.xlsx']

df0= pd.read_excel(os.path.join(file_path, name_list[0]))
df1= pd.read_excel(os.path.join(file_path, name_list[1]))
df2= pd.read_excel(os.path.join(file_path, name_list[2]))
df3= pd.read_excel(os.path.join(file_path, name_list[3]))
df4= pd.read_excel(os.path.join(file_path1, '种群动态变化指数 V_pi.xlsx'))
df5= pd.read_excel(os.path.join(file_path, name_list[4]))
df6= pd.read_excel(os.path.join(file_path, name_list[5]))
# 逐步合并DataFrame
# 首先合并df0和df1
merged_df = pd.merge(df0, df1, on=['Plot', '树种'], how='inner')
# 然后合并上一步的结果和df2
merged_df = pd.merge(merged_df, df2, on=['Plot', '树种'], how='inner')
# 最后合并上一步的结果和df3
merged_df = pd.merge(merged_df, df3, on=['Plot', '树种'], how='inner')
merged_df = pd.merge(merged_df, df4, on=['Plot', '树种'], how='inner')
merged_df = pd.merge(merged_df, df5, on=['Plot', '树种'], how='inner')
merged_df = pd.merge(merged_df, df6, on=['Plot', '树种'], how='inner')
# 打印合并后的DataFrame
print(merged_df)
merged_df.to_excel(os.path.join(file_path,'林分结构特征和汇总.xlsx'),index=False)


