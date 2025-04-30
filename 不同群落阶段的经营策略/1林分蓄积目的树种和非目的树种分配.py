import os
import pandas as pd

# 设置路径和读取数据
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
data_path = os.path.join(out_path, '各径阶林分蓄积.xlsx')
data = pd.read_excel(data_path)

# 分类函数
def classify_diameter_class(diameter):
    if diameter <= 12:
        return '小径木'
    elif 12 < diameter <= 24:
        return '中径木'
    else:
        return '大径木'

# 应用分类函数并汇总数据
df = data.copy()
df['分类'] = df['径阶'].apply(classify_diameter_class)
df['树种分类蓄积'] = df.groupby(['plot','树种', '分类'])['径阶蓄积'].transform('sum')
df['树种总蓄积'] = df.groupby(['plot','树种'])['径阶蓄积'].transform('sum')
df.drop_duplicates(subset=['plot','树种','分类'], inplace=True)

df_second=df[~df['树种'].isin(['红松','水曲柳','胡桃楸','黄菠萝','紫椴','冷杉'])]
df=df[df['树种'].isin(['红松','水曲柳','胡桃楸','黄菠萝','紫椴','冷杉'])]

#目的树种蓄积样地分配
df_all=df.copy()
df_all.drop_duplicates(subset=['plot','树种'], inplace=True)
#排序
ordered_sites=['红松', '水曲柳', '胡桃楸','黄菠萝','紫椴','冷杉']
df_all['树种'] = pd.Categorical(df_all['树种'], categories=ordered_sites, ordered=True)
df_all= df_all.sort_values(by='树种')
df_all = df_all.sort_values(by='树种总蓄积', ascending=False).reset_index(drop=True)

from plotnine import *
fg = (ggplot(df_all, aes(x='plot', y='树种总蓄积', fill='树种')) + geom_bar(stat='identity', color='k',position='fill')
            + scale_fill_manual(values=['w','gray','black','lightgrey','Tan','FloralWhite'],
                           labels=['红松', '水曲柳', '胡桃楸','黄菠萝','紫椴','冷杉'])
          + theme(axis_line=element_line(color='black')
                  , text=element_text(family=['Times New Roman'], color='black', size=17)
                  , title=element_text(family=['SimSun'], color='black', size=17)
                  ,axis_text_x=element_text(family='SimSun', color='blue', size=12, angle=0, hjust=1) # 设置 x 轴坐标文字格式
                  ,  legend_text=element_text(size=12, family='SimSun', color='black'),
                  panel_grid_major=element_blank(),  # 去除主要网格线
                  panel_grid_minor=element_blank()# 去除次要网格线
                  , panel_background=element_rect(fill='white')
                  , figure_size=(12, 10))
          + xlab("树种") + ylab("蓄积分配系数")
          )
fg.show()

#目的树种蓄积分类分配
ordered_sites=['大径木','中径木','小径木']
df['分类'] = pd.Categorical(df['分类'], categories=ordered_sites, ordered=True)
df= df.sort_values(by='分类')
for name in df['plot'].unique():
    df_group = df[df['plot']==name]
    from plotnine import *
    fg = (ggplot(df_group, aes(x='分类', y='树种分类蓄积', fill='树种')) + geom_bar(stat='identity', color='k',position='fill')
          + theme(axis_line=element_line(color='black')
                  , text=element_text(family=['Times New Roman'], color='black', size=17)
                  , title=element_text(family=['SimSun'], color='black', size=17)
                  , axis_text_x=element_text(family='SimSun', color='blue', size=12, angle=0, hjust=1)  # 设置 x 轴坐标文字格式
                  , legend_text=element_text(size=12, family='SimSun', color='black')
                  , panel_grid_major=element_blank(),  # 去除主要网格线
                  panel_grid_minor=element_blank()# 去除次要网格线
                  , panel_background=element_rect(fill='white')
                  , figure_size=(12, 10))
          + xlab(f"{name}树种") + ylab("蓄积分配系数")
          )
    #fg.show()


#非目的树种
ordered_sites=['大径木','中径木','小径木']
df_second['分类'] = pd.Categorical(df_second['分类'], categories=ordered_sites, ordered=True)
df_second= df_second.sort_values(by='分类')

for name in df_second['plot'].unique():
    df_second_group = df_second[df_second['plot']==name]
    from plotnine import *
    fg = (ggplot(df_second_group, aes(x='分类', y='树种分类蓄积', fill='树种')) + geom_bar(stat='identity', color='k',position='fill')
          + theme(axis_line=element_line(color='black')
                  , text=element_text(family=['Times New Roman'], color='black', size=17)
                  , title=element_text(family=['SimSun'], color='black', size=17)
                  , axis_text_x=element_text(family='SimSun', color='blue', size=12, angle=0, hjust=1)  # 设置 x 轴坐标文字格式
                  , legend_text=element_text(size=12, family='SimSun', color='black')
                  , panel_grid_major=element_blank(),  # 去除主要网格线
                  panel_grid_minor=element_blank()# 去除次要网格线
                  , panel_background=element_rect(fill='white')
                  , figure_size=(12, 10))
          + xlab(f"{name}树种") + ylab("蓄积分配系数")
          )
    #fg.show()

