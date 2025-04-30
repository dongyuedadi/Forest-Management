import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 文件路径配置
file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'

# 添加20cm数据（包含树种信息）
supplement_data = [
    {'类型': '软阔混交林', '树高': 28, '数量': 1158, '树种': '幼苗'},
    {'类型': '软硬阔混交林', '树高': 28, '数量': 149, '树种': '幼苗'},
    {'类型': '硬阔混交林', '树高': 28, '数量': 445, '树种': '幼苗'}
]

# 生成补充数据集
supp_dfs = []
for item in supplement_data:
    supp_df = pd.DataFrame({
        '类型': [item['类型']] * item['数量'],
        '树高': [item['树高']] * item['数量'],
        '树种': [item['树种']] * item['数量']  # 新增树种列
    })
    supp_dfs.append(supp_df)

# 处理包含树种的数据
def process_file_with_species(file_name):
    """读取包含树种的数据"""
    data_path = os.path.join(file_path, file_name)
    basename = file_name.rsplit('.', 1)[0]
    data = pd.read_excel(data_path, sheet_name='30cm以上幼苗幼树高调查记录')
    data_clean = data[(data['树高'] >= 15) & (data['树高'] <= 1000)].dropna(subset=['树高', '树种'])
    data_clean['类型'] = basename
    return data_clean[['类型', '树种', '树高']]


# 合并所有数据（含补充数据）
files = ['软阔混交林.xlsx', '软硬阔混交林.xlsx', '硬阔混交林.xlsx']
all_data = pd.concat([process_file_with_species(f) for f in files], ignore_index=True)
all_data = pd.concat([all_data, *supp_dfs], ignore_index=True)  # 关键修改：合并补充数据
final_df = all_data.copy()

# 绘制增强版小提琴图
plt.figure(figsize=(12, 7))
sns.violinplot(x='类型', y='树高', data=final_df,
               color='gray',
               bw_method=0.15,  # 优化带宽
               cut=0,  # 禁用范围扩展
               inner='quartile',
               edgecolor='black',
               linewidth=1,
               alpha=0.8)

# 增强可视化效果
# 标题 (Title)
plt.title('更新分布\nRegeneration distribution', fontsize=14, pad=20)
# 坐标轴标签 (Axis labels)
plt.xlabel('林分类型\nForest type', fontsize=12, labelpad=10)
plt.ylabel('树高\nHeight/cm', fontsize=12, labelpad=10)
# 基准线标注 (Reference line annotation)
plt.axhline(y=30, color='black', linestyle='--', linewidth=1.2,
            label='30cm基准高度线\n30cm reference line')
plt.legend()
plt.grid(axis='y', linestyle=':', alpha=0.8)
# 保存输出
plt.show()



# 定义树高区间参数
bins = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
labels = ['0-30', '30-60', '60-90', '90-120', '120-150',
          '150-180', '180-210', '210-240', '240-270', '270-300', '300-330']
x_ticks = [(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)]

# 为每个森林类型生成独立图表
for forest_type in all_data['类型'].unique():
    type_data = all_data[all_data['类型'] == forest_type].copy()

    # 分箱处理
    type_data['区间'] = pd.cut(type_data['树高'], bins=bins, labels=labels, right=False)
    type_data = type_data[type_data['区间'].notna()]

    # 统计频数
    counts = type_data.groupby(['树种', '区间'], observed=False) \
        .size() \
        .unstack(fill_value=0) \
        .reindex(labels, axis=1, fill_value=0)

    # 生成绘图数据
    plot_data = []
    for species in counts.index:
        for label, mid in zip(labels, x_ticks):
            plot_data.append({
                '树种': species,
                '区间中点': mid,
                '株数': counts.loc[species, label],
                '区间标签': label
            })

    plot_df = pd.DataFrame(plot_data)

    # 创建画布
    plt.figure(figsize=(15, 8))

    # 绘制散点图
    sns.scatterplot(data=plot_df, x='区间中点', y='株数', hue='树种',
                    palette='tab20', s=120, edgecolor='black',
                    linewidth=0.8, alpha=0.8)

    # 图表装饰
    plt.title(f'{forest_type} - 更新分布\n{forest_type} - Regeneration Distribution',
              fontsize=14, pad=15)
    plt.xlabel('树高区间 (cm)\nHeight Class (cm)', fontsize=12)
    plt.ylabel('株数\nStem Count', fontsize=12)
    plt.xticks(x_ticks, labels=labels, rotation=45)
    plt.ylim(0, plot_df['株数'].max() * 1.2)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # 添加数据标签
    for _, row in plot_df.iterrows():
        if row['株数'] > 0:
            plt.text(row['区间中点'], row['株数'] + 5,
                     int(row['株数']), ha='center', fontsize=8)

    # 保存输出
    #plt.show()

# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 文件路径配置
file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'

# 补充数据定义
supplement_data = [
    {'类型': '软阔混交林', '树高': 28, '数量': 1158, '树种': '幼苗'},
    {'类型': '软硬阔混交林', '树高': 28, '数量': 149, '树种': '幼苗'},
    {'类型': '硬阔混交林', '树高': 28, '数量': 445, '树种': '幼苗'}
]

# 生成补充数据集
supp_dfs = []
for item in supplement_data:
    supp_df = pd.DataFrame({
        '类型': [item['类型']] * item['数量'],
        '树高': [item['树高']] * item['数量'],
        '树种': [item['树种']] * item['数量']
    })
    supp_dfs.append(supp_df)


def process_file_with_species(file_name):
    """处理含树种数据"""
    data_path = os.path.join(file_path, file_name)
    basename = file_name.rsplit('.', 1)[0]
    data = pd.read_excel(data_path, sheet_name='30cm以上幼苗幼树高调查记录')
    data_clean = data[(data['树高'] >= 15) & (data['树高'] <= 1000)].dropna(subset=['树高', '树种'])
    data_clean['类型'] = basename
    return data_clean[['类型', '树种', '树高']]


# 合并数据集
files = ['软阔混交林.xlsx', '软硬阔混交林.xlsx', '硬阔混交林.xlsx']
all_data = pd.concat([process_file_with_species(f) for f in files], ignore_index=True)
all_data = pd.concat([all_data, *supp_dfs], ignore_index=True)

# 配置树高区间参数
bins = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
labels = ['0-30', '30-60', '60-90', '90-120', '120-150',
          '150-180', '180-210', '210-240', '240-270', '270-300', '300-330']
x_ticks = [(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)]

# 可视化主循环
for forest_type in all_data['类型'].unique():
    # 数据准备
    type_data = all_data[all_data['类型'] == forest_type].copy()
    type_data['区间'] = pd.cut(type_data['树高'], bins=bins, labels=labels, right=False)
    type_data = type_data[type_data['区间'].notna()]

    # 频数统计
    counts = type_data.groupby(['树种', '区间'], observed=False) \
        .size() \
        .unstack(fill_value=0) \
        .reindex(labels, axis=1, fill_value=0)

    # 统计检验模块（新增最大降幅筛选）
    total_counts = counts.sum(axis=0)
    max_drop = 0
    max_drop_interval = None

    for i in range(1, len(total_counts)):
        prev = total_counts.iloc[i - 1]
        current = total_counts.iloc[i]

        # 跳过无效比较
        if prev == 0 and current == 0:
            continue

        # Z检验（泊松分布假设）
        delta = current - prev
        se = np.sqrt(prev + current)
        if se == 0:
            continue
        z_score = delta / se
        p_value = stats.norm.cdf(z_score)  # 单侧检验

        # 记录最大降幅区间
        if p_value < 0.05 and delta < 0:
            drop_magnitude = prev - current  # 计算绝对下降量
            if drop_magnitude > max_drop:
                max_drop = drop_magnitude
                max_drop_interval = total_counts.index[i]

    # 生成绘图数据
    plot_data = []
    for species in counts.index:
        for label, mid in zip(labels, x_ticks):
            plot_data.append({
                '树种': species,
                '区间中点': mid,
                '株数': counts.loc[species, label],
                '区间标签': label
            })
    plot_df = pd.DataFrame(plot_data)

    # 创建画布
    plt.figure(figsize=(15, 8))

    # 绘制散点图
    sns.scatterplot(data=plot_df, x='区间中点', y='株数', hue='树种',
                    palette='tab20', s=150, edgecolor='black',
                    linewidth=0.8, alpha=0.9, zorder=2)

    # 唯一显著性标记（新增条件判断）
    if max_drop_interval:
        mid_x = x_ticks[labels.index(max_drop_interval)]

        # 添加背景色带
        plt.axvspan(mid_x - 15, mid_x + 15,
                    alpha=0.2, color='crimson', zorder=1)

        # 添加箭头标注
        plt.annotate(f'▼ 最大降幅: {int(max_drop)}株',
                     xy=(mid_x, plt.ylim()[1] * 0.93),
                     xytext=(mid_x, plt.ylim()[1] * 0.98),
                     ha='center', va='bottom',
                     color='darkred', fontsize=12,
                     arrowprops=dict(arrowstyle="->",
                                     color='darkred',
                                     lw=1.5),
                     bbox=dict(boxstyle="round,pad=0.3",
                               fc="white", ec="darkred", lw=1))

    # 图表装饰
    plt.title(f'{forest_type} - 更新分布（最大降幅标记）\n{forest_type} - Regeneration Distribution',
              fontsize=14, pad=15)
    plt.xlabel('树高区间 (cm)\nHeight Class (cm)', fontsize=12)
    plt.ylabel('株数\nStem Count', fontsize=12)
    plt.xticks(x_ticks, labels=labels, rotation=45)
    plt.ylim(0, plot_df['株数'].max() * 1.25)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # 数据标签
    for _, row in plot_df.iterrows():
        if row['株数'] > 0:
            plt.text(row['区间中点'], row['株数'] + 5,
                     int(row['株数']),
                     ha='center', fontsize=9, color='dimgrey')

    # 保存或显示
    plt.tight_layout()
    #plt.show()