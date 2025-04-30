from sklearn.model_selection import train_test_split
import pandas as pd


#加载数据集
file_path = r'C:\Users\hys5637428\Desktop\模型拟合\黑龙江地方2010_2015年一类样地数据.xlsx'
data = pd.read_excel(file_path)
df = data.copy()
#划分训练集和测试集
df_train,df_test=train_test_split(df,test_size=0.2,random_state=42)
#在编程和机器学习中，random_state 参数经常用于控制随机数生成器的种子。设置 random_state 的目的是为了确保代码的可重复性。
# 当你设置了一个特定的 random_state 值（比如 42），随机数生成器的行为就变得可预测了，这意味着每次运行代码时，它都会生成相同的随机数序列。
#random_state=42 是一种约定俗成的做法，它结合了文化意义和实用性

#测试训练集和测试集是否有重复
df_train_list=list(df_train['样地号'])
df_test_list=list(df_test['样地号'])
duplicate_list=list(set(df_train_list) & set(df_test_list))
contact_list=list(set(df_train_list) |set(df_test_list))
print(duplicate_list)
print(contact_list)