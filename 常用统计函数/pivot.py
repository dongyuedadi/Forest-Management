import os
import pandas as pd
import numpy as np
file_path=r"C:\\Users\\hys5637428\\Desktop\\帽儿山蘑菇调查\\path"
file=os.path.join(file_path,'9.15-9.20蘑菇调查.xlsx')
data=pd.read_excel(file,sheet_name='检尺')
print(data.head())

pivot_data=pd.pivot_table(data,index='树种',values=['树高'],columns='样地',fill_value='无')
print(pivot_data.head())