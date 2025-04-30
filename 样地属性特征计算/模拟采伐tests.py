import os
import pandas as pd

file_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out2'
file = os.path.join(file_path, '空间结构.xlsx')
data = pd.read_excel(file)
out_df = data[data['树种'].isin(['红松', '胡桃楸', '黄菠萝', '春榆', '柞树', '白桦', '水曲柳', '紫椴'])]
bianhao=out_df.loc[(out_df['混交度']<0.75)&(out_df['样地']==1)&(out_df['角尺度']>0.517)&(out_df['大小比']>0)]
baihua=out_df.loc[(out_df['大小比']==0)&(out_df['树种']=='白桦')&(out_df['角尺度']>0.5)&(out_df['样地']==1)]
print(bianhao['编号'])
print(baihua['编号'])
print(bianhao['材积'].sum())
print(baihua['材积'].sum())
print(bianhao.shape)
print(baihua.shape)

