
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
from plotnine import *

# 设置路径和读取数据
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
data_path = os.path.join(out_path, '各径阶林分蓄积.xlsx')
data = pd.read_excel(data_path)

# 树种名称到缩写的映射
species_mapping = {
    '春榆': 'CY',
    '色木': 'SM',
    '白桦': 'BH',
    '山杨': 'SY',
    '大青杨': 'DQY',
    '糠椴': 'KD',
    '红松': 'HS',
    '水曲柳': 'SQL',
    '胡桃楸': 'HTQ',
    '黄菠萝': 'HBL',
    '紫椴': 'ZD',
    '冷杉': 'LS'
}
species_mapping1={'软阔混交林':'RK',
                  '软硬阔混交林':'RYK',
                  '硬阔混交林':'YK',
                  '原始性次生林':'YSC'}
# 应用分类函数并汇总数据
df = data.copy()
df['分类'] = df['径阶'].apply(classify_diameter_class)
df['树种分类蓄积'] = df.groupby(['Plot', '树种', '分类'])['径阶蓄积'].transform('sum')
df.drop_duplicates(subset=['Plot', '树种', '分类'], inplace=True)

# 更新树种名称为缩写
df['树种'] = df['树种'].map(species_mapping)
df['Plot']=df['Plot'].map(species_mapping1)
# 分开目的树种和非目的树种
df_target = df[df['树种'].isin(['HS', 'SQL', 'HTQ', 'HBL', 'ZD', 'LS'])]
df_second = df[df['树种'].isin(['CY', 'SM', 'BH', 'SY', 'DQY', 'KD'])]

ordered_sites = ['大径木', '中径木', '小径木']
df_target['分类'] = pd.Categorical(df_target['分类'], categories=ordered_sites, ordered=True)
df_target = df_target.sort_values(by='分类')
df_second['分类'] = pd.Categorical(df_second['分类'], categories=ordered_sites, ordered=True)
df_second = df_second.sort_values(by='分类')

# 设置图形主题和元素
theme_settings = theme(
    axis_line=element_line(color='black'),
    text=element_text(family=['SimSun'], color='black', size=17),
    title=element_text(family=['SimSun'], color='black', size=17),
    axis_text_x=element_text(family='SimSun', color='black', size=17, angle=0, hjust=0.5),
    legend_text=element_text(size=17, family='SimSun', color='black'),
    panel_grid_major=element_blank(),
    panel_grid_minor=element_blank(),
    panel_background=element_rect(fill='white'),
    figure_size=(12, 10)
)

# 定义并显示目的树种绘图对象
fg_target = (ggplot(df_target, aes(x='树种', y='树种分类蓄积', fill='分类'))
             + geom_bar(stat='identity', color='k', position='fill')
             + scale_fill_manual(values=['w', 'gray', 'black'], labels=['LD', 'MD', 'SD'])
             + theme_settings
             + xlab("   目的树种\nTarget species") + ylab("              目的树种蓄积分配系数\nStock distribution coefficient of target species")
             + facet_wrap('~Plot')
            )
fg_target.show()

# 定义并显示非目的树种绘图对象
fg_second = (ggplot(df_second, aes(x='树种', y='树种分类蓄积', fill='分类'))
             + geom_bar(stat='identity', color='k', position='fill')
             + scale_fill_manual(values=['w', 'gray', 'black'], labels=['LD', 'MD', 'SD'])
             + theme_settings
             + xlab("    非目的树种\nNon-target species") + ylab("               非目的树种蓄积分配系数\nStock distribution coefficient of non-target species")
             + facet_wrap('~Plot')
            )
fg_second.show()