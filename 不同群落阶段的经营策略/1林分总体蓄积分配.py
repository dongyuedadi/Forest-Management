
# 分类函数
def classify_diameter_class(diameter):
    if diameter <= 12:
        return '小径木'
    elif 12 < diameter <= 24:
        return '中径木'
    else:
        return '大径木'

import os
import pandas as pd
# 导入库
from plotnine import *
# 设置路径和读取数据
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
data_path = os.path.join(out_path, '各径阶林分蓄积.xlsx')
data = pd.read_excel(data_path)
species_mapping1={'软阔混交林':'RK',
                  '软硬阔混交林':'RYK',
                  '硬阔混交林':'YK',
                  '原始性次生林':'YSC'}
# 应用分类函数并汇总数据
df = data.copy()
df['分类'] = df['径阶'].apply(classify_diameter_class)
df['分类蓄积'] = df.groupby(['Plot', '分类'])['径阶蓄积'].transform('sum')
df.drop_duplicates(subset=['Plot','分类'], inplace=True)
df['Plot']=df['Plot'].map(species_mapping1)
ordered_sites=['大径木','中径木','小径木']
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
       + scale_fill_manual(values=['w', 'gray', 'black'], labels=['LD', 'MD', 'SD'])
       + theme_settings
       + xlab(" 林分类型\nStand type") + ylab("                    大中小径阶蓄积分配系数\nAccumulation distribution coefficient of small and medium order")
      )
# 显示图形
fg.show()
