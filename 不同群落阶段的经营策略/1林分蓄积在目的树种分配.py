def classify_sps_class(sps):
    if sps in ['红松', '水曲柳', '胡桃楸', '黄菠萝', '紫椴', '冷杉']:
        return '目的树种'
    else:
        return '非目的树种'

species_mapping1={'软阔混交林':'RK',
                  '软硬阔混交林':'RYK',
                  '硬阔混交林':'YK',
                  '原始性次生林':'YSC'}
import os
import pandas as pd
from plotnine import *
# 设置路径和读取数据
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
data_path = os.path.join(out_path, '各径阶林分蓄积.xlsx')
data = pd.read_excel(data_path)
# 应用分类函数并汇总数据
df = data.copy()
# 注意：这里假设 '树种' 列中的每个元素都是单个字符串，不是列表或 Series。
# 如果 '树种' 列包含的是列表或 Series，那么需要调整 classify_sps_class 函数来处理这种情况。
df['分类'] = df['树种'].apply(classify_sps_class)
df['分类蓄积'] = df.groupby(['Plot', '分类'])['径阶蓄积'].transform('sum')
df.drop_duplicates(subset=['Plot','分类'], inplace=True)
df['Plot']=df['Plot'].map(species_mapping1)
ordered_sites=['目的树种','非目的树种']
df['分类'] = pd.Categorical(df['分类'], categories=ordered_sites, ordered=True)
df= df.sort_values(by='分类')
# 设置图形主题和元素
theme_settings = theme(axis_line=element_line(color='black'),
                        text=element_text(family=['SimSun'], color='black', size=17),
                        title=element_text(family=['SimSun'], color='black', size=17),
                        axis_text_x=element_text(family='SimSun', color='black', size=17, angle=0, hjust=0.5),
                        legend_text=element_text(size=17, family='SimSun', color='black'),
                        panel_grid_major=element_blank(),
                        panel_grid_minor=element_blank(),
                        panel_background=element_rect(fill='white'),
                        figure_size=(12, 10))

# 定义绘图对象
fg = (ggplot(df, aes(x='Plot', y='分类蓄积', fill='分类'))
       + geom_bar(stat='identity', color='k', position='fill')
       + scale_fill_manual(values=['w', 'gray'], labels=['目的树种\nTarget species','非目的树种\nNon-target species'])
       + theme_settings
       + xlab(" 林分类型\nStand type") + ylab("           目的树种蓄积分配系数\nStock distribution coefficient of target species")
      )
# 显示图形
fg.show()
