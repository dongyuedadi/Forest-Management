import os
import pandas as pd
import numpy as np
file_path=r"C:\\Users\\hys5637428\\Desktop\\帽儿山蘑菇调查\\path"
file=os.path.join(file_path,'9.15-9.20蘑菇调查.xlsx')
data=pd.read_excel(file,sheet_name='检尺')
data.count()#非空值数量
data.columns
data.index

data.head()
data.tail()

data['胸径'].sum()
data['树高'].mean()
print(data['胸径'].median())
print(data['胸径'].std(),data['胸径'].var())#无偏估计，分母为n-1
print(data['胸径'].max(),data['胸径'].min())
print(data['胸径'].head().prod())
print(data['胸径'].cumsum())
print(data['胸径'].pct_change())#(当前值 - 前一值) / 前一值

data['胸高断面积']=data['胸径'].apply(lambda x:x**2/4*np.pi)
print(data['胸高断面积'].tail())
print(data.size)

