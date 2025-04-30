import os
import pandas as pd
import numpy as np
file_path=r"C:\\Users\\hys5637428\\Desktop\\帽儿山蘑菇调查\\path"
file=os.path.join(file_path,'9.15-9.20蘑菇调查.xlsx')
data=pd.read_excel(file,sheet_name='检尺')
print(data.head())
grouped=data.groupby(['样地','树种'])['胸径']
print(grouped.size())
for name, group in grouped:
    print(name)
    print(group)
print(grouped.sum())


print(grouped.agg([('合计','sum')]))

grouped1=data.groupby(['样地','树种'])
filter1=grouped1.filter(lambda x:x['胸径'].mean()>5)
print(filter1)
