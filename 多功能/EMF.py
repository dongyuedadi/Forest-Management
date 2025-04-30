import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, f_oneway
import warnings

# 全局配置
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings("ignore")


# ====================
# 数据预处理
# ====================
def load_and_preprocess():
    """数据加载与标准化处理"""
    df = pd.read_excel(r"C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\数据(9)_with_soil_properties.xlsx")

    # 数据清洗
    df = df.dropna(subset=['阶段']).replace([np.inf, -np.inf], np.nan)

    # 标准化处理
    metrics = ["涵养水源功能(元/年/公顷)","保育土壤功能(元/公顷)","固碳释氧功能（元/公顷）","木材生产功能（元/公顷）"]
    for col in metrics:
        df[f'{col}标准化值']  = (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-6)
        print(f'{col}: {df[col].min()}, {df[col].max()}, {df[col].mean()}')

    # 计算生态系统多功能性(EMF)
    df['EMF'] = df[[f'{col}标准化值' for col in metrics]].mean(axis=1)

    return df


# ====================
# 可视化模块
# ====================
def plot_combined_violin():
    """组合式小提琴图（5个子图）"""
    df = load_and_preprocess()
    metrics = ["涵养水源功能(元/年/公顷)标准化值","保育土壤功能(元/公顷)标准化值","固碳释氧功能（元/公顷）标准化值","木材生产功能（元/公顷）标准化值",'EMF']
    titles = ['碳汇功能', '土壤保育功能', '珍贵木材生产功能', '水源涵养功能', '生态系统多功能性']

    fig, axes = plt.subplots(5, 1, figsize=(12, 18), dpi=100)
    plt.subplots_adjust(hspace=0.35)

    for ax, col, title in zip(axes, metrics, titles):
        # 数据过滤
        data = df[['阶段', col]].dropna()

        # 绘制小提琴图
        sns.violinplot(x='阶段', y=col, data=data, ax=ax,
                       cut=0, inner="quartile", linewidth=1.5,
                       palette="Set2")

        # 添加统计标注
        groups = data.groupby('阶段')
        if len(groups) > 1:
            anova_data = [groups.get_group(s)[col] for s in groups.groups]
            f_stat, p_val = f_oneway(*anova_data)
            p_text = f"ANOVA p={p_val:.3f}" if p_val >= 0.001 else "ANOVA p<0.001"
            ax.text(0.05, 0.95, p_text, transform=ax.transAxes,
                    fontsize=10, color='darkred', weight='bold',
                    bbox=dict(facecolor='white', alpha=0.8))

        ax.set_title(f"{title}分布", fontsize=12, pad=12)
        ax.set_xlabel('' if ax != axes[-1] else '发展阶段')
        ax.set_ylabel('标准化值' if title != '生态系统多功能性' else 'EMF')
    plt.show()


def plot_multithreshold_trend():
    """多阈值趋势分析（单图）"""
    df = load_and_preprocess()
    metrics = ["涵养水源功能(元/年/公顷)标准化值","保育土壤功能(元/公顷)标准化值","固碳释氧功能（元/公顷）标准化值","木材生产功能（元/公顷）标准化值"]

    thresholds = np.linspace(0, 1, 11)
    results = []

    for t in thresholds:
        # 计算多功能性指标
        normalized = (df[metrics] - df[metrics].min()) / (df[metrics].max() - df[metrics].min() + 1e-6)
        df['MF'] = (normalized >= t).mean(axis=1)

        # 按阶段分组，计算均值和标准误差
        grouped = df.groupby('阶段')['MF'].agg(['mean', 'sem'])
        grouped['threshold'] = t
        results.append(grouped.reset_index())

    # 合并结果
    trend_df = pd.concat(results)

    # 绘制趋势图
    plt.figure(figsize=(10, 6), dpi=120)
    sns.lineplot(data=trend_df, x='threshold', y='mean', hue='阶段',
                 style='阶段', markers=True, markersize=8,
                 palette="tab10", linewidth=2.5)

    plt.xticks(np.linspace(0, 1, 6), [f"{x:.0%}" for x in np.linspace(0, 1, 6)])
    plt.xlabel('功能达标阈值', fontsize=12)
    plt.ylabel('多功能性指数', fontsize=12)
    plt.title('多功能性随阈值变化趋势分析', fontsize=14, pad=15)
    plt.legend(title='发展阶段', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.show()

# ====================
# 统计分析模块
# ====================
def export_statistics():
    """输出统计结果到Excel"""
    df = load_and_preprocess()

    # 各阶段描述性统计
    desc_stats = df.groupby('阶段').agg({
        '涵养水源功能(元/年/公顷)': ['mean', 'std'],
        '保育土壤功能(元/公顷)': ['mean', 'std'],
        '固碳释氧功能（元/公顷）': ['mean', 'std'],
        '木材生产功能（元/公顷）': ['mean', 'std'],
        'EMF': ['mean', 'std']
    })

    # 年龄相关性分析
    corr_results = []
    for col in ["涵养水源功能(元/年/公顷)标准化值","保育土壤功能(元/公顷)标准化值","固碳释氧功能（元/公顷）标准化值","木材生产功能（元/公顷）标准化值",'EMF']:
        clean_df = df[['年龄', col]].dropna()
        if len(clean_df) > 10:
            r, p = pearsonr(clean_df['年龄'], clean_df[col])
            corr_results.append({
                '指标': col,
                '相关系数': r,
                'p值': p,
                '样本量': len(clean_df)
            })

    # 保存结果
    with pd.ExcelWriter(r'C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\统计分析结果.xlsx') as writer:
        desc_stats.to_excel(writer, sheet_name='描述性统计')
        pd.DataFrame(corr_results).to_excel(writer, sheet_name='年龄相关性', index=False)

    print("统计分析结果已保存至 统计分析结果.xlsx")


# ====================
# 主程序
# ====================
if __name__ == "__main__":
    print("正在进行数据分析...")
    df = load_and_preprocess()

    print("\n生成组合式小提琴图...")
    plot_combined_violin()

    print("\n生成多阈值趋势图...")
    plot_multithreshold_trend()

    print("\n执行统计分析...")
    export_statistics()

    print("\n分析完成！结果文件已保存至当前目录")