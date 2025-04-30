# -*- coding: utf-8 -*-
from plotnine import *
import os
import pandas as pd

# 分类函数
def classify_diameter_class(diameter):
    if diameter <= 12:
        return '小径木'
    elif 12 < diameter <= 24:
        return '中径木'
    else:
        return '大径木'

# 设置路径和读取数据
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
data_path = os.path.join(out_path, '各径阶林分株树.xlsx')
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
species_mapping1 = {'软阔混交林':'RK', '软硬阔混交林':'RYK', '硬阔混交林':'YK'}

# 数据处理流程
df = data.copy()
df['分类'] = df['径阶'].apply(classify_diameter_class)
df['树种分类株树'] = df.groupby(['Plot','树种', '分类'])['径阶株树'].transform('sum')
df.drop_duplicates(subset=['Plot','树种','分类'], inplace=True)

# 名称标准化
df['树种'] = df['树种'].map(species_mapping)
df['Plot'] = df['Plot'].map(species_mapping1)

# 分类排序
ordered_sites = ['大径木','中径木','小径木']
df['分类'] = pd.Categorical(df['分类'], categories=ordered_sites, ordered=True)
df = df.sort_values(by='分类')

# 拆分数据集
df_target = df[df['树种'].isin(['HS', 'SQL', 'HTQ', 'HBL', 'ZD', 'LS'])]
df_second = df[df['树种'].isin(['CY', 'SM', 'BH', 'SY', 'DQY', 'KD'])]

# 图形主题配置
theme_settings = theme(
    axis_line=element_line(color='black'),
    text=element_text(family=['SimSun'], color='black', size=17),
    title=element_text(family=['SimSun'], color='black', size=17),
    axis_text_x=element_text(
        family='SimSun',
        color='black',
        size=17,
        angle=0,
        hjust=0.5,
        margin={'t':10}  # 增加X轴标签上边距
    ),
    axis_text_y=element_text(
        family='SimSun',
        color='black',
        size=17,
        margin={'r':10}  # 增加Y轴标签右边距
    ),
    legend_text=element_text(size=17, family='SimSun', color='black'),
    panel_grid_major=element_blank(),
    panel_grid_minor=element_blank(),
    panel_background=element_rect(fill='white'),
    figure_size=(16, 8),  # 优化图形比例
    strip_background=element_rect(fill='#F0F0F0'),  # 分面标题背景
    strip_text=element_text(size=18)  # 分面标题字号
)

# 目的树种绘图
target_plot = (
    ggplot(df_target, aes(x='树种', y='树种分类株树', fill='分类'))
    + geom_bar(stat='identity', color='k', position='fill', width=0.85)
    + scale_fill_manual(
        values=['w', 'gray', 'black'],
        labels=['LD', 'MD', 'SD'],
        name='径阶分类'
    )
    + theme_settings
    + xlab("   目的树种\nTarget species")
    + ylab("       株数分配系数\nDistribution coefficient/%")
    + facet_wrap('~Plot', nrow=1)  # 强制单行排列
    + theme(
        legend_position='top',  # 图例置顶
        legend_title=element_blank(),
        legend_box_margin=10,
        subplots_adjust={'wspace':0.25}  # 分面间距
    )
)
target_plot.show()

# 非目的树种绘图
non_target_plot = (
    ggplot(df_second, aes(x='树种', y='树种分类株树', fill='分类'))
    + geom_bar(stat='identity', color='k', position='fill', width=0.85)
    + scale_fill_manual(
        values=['w', 'gray', 'black'],
        labels=['LD', 'MD', 'SD'],
        name='径阶分类'
    )
    + theme_settings
    + xlab("    非目的树种\nNon-target species")
    + ylab("       株数分配系数\nDistribution coefficient/%")
    + facet_wrap('~Plot', nrow=1)
    + theme(
        legend_position='top',
        legend_title=element_blank(),
        subplots_adjust={'wspace':0.25}
    )
)
non_target_plot.show()