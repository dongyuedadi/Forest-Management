# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import weibull_min

# ======================
# 全局可视化参数配置
# ======================
plt.rcParams.update({
    # 字体配置
    'font.family': 'SimSun',  # 主字体为宋体
    'font.size': 12,  # 常规字号
    'axes.unicode_minus': False,  # 解决负号显示问题

    # 分层字号系统
    'axes.titlesize': 14,  # 子图标题字号（加粗显示）
    'axes.labelsize': 13,  # 轴标签字号
    'xtick.labelsize': 11,  # X轴刻度字号
    'ytick.labelsize': 11,  # Y轴刻度字号

    # 图形元素样式
    'hist.bins': 'auto',  # 直方图默认分箱
    'grid.alpha': 0.3,  # 网格透明度
})


# ======================
# 核心绘图函数
# ======================
def plot_diameter_distribution(data, column, title, ax):
    """
    绘制带有Weibull分布的胸径分布图

    参数：
    data -- 包含数据的DataFrame
    column -- 需要分析的列名
    title -- 子图标题
    ax -- matplotlib轴对象
    """
    # 数据校验
    if data.empty or column not in data.columns:
        raise ValueError("输入数据无效或列名不存在")

    # 数据预处理
    valid_data = data[column].dropna()
    if valid_data.empty:
        print(f"警告：{title} 无有效数据")
        return

    # 直方图参数计算
    max_diameter = np.ceil(valid_data.max())
    bins = np.arange(5, max_diameter + 3, 2)  # 5cm起，2cm间隔

    # 绘制直方图
    n, bins, patches = ax.hist(
        valid_data,
        bins=bins,
        edgecolor='k',
        facecolor='#E0E0E0',
        density=False,
        alpha=0.7
    )
    # 设置主坐标轴
    ax.set_title(title, fontsize=14, fontweight='semibold', pad=12)
    ax.set_ylabel('频数\nFrequency', fontsize=12, labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.5)

    # 添加Weibull分布曲线
    ax2 = ax.twinx()
    shape, _, scale = weibull_min.fit(valid_data, floc=0)
    x = np.linspace(valid_data.min(), valid_data.max(), 200)
    pdf = weibull_min.pdf(x, shape, scale=scale)

    ax2.plot(
        x, pdf,
        color='#2F2F2F',
        linewidth=2,
        linestyle='-',
        label='Weibull拟合'
    )
    ax2.set_ylabel('概率密度\nProbability Density/%', fontsize=12, labelpad=10)

    # 添加图例
    ax.legend(loc='upper left', frameon=False)
    ax2.legend(loc='upper right', frameon=False)


# ======================
# 主程序流程
# ======================
def main():
    # 输入输出路径配置
    input_dir = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
    output_dir = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'

    # 文件名映射表
    name_mapping = {
        '软阔混交林': 'RK',
        '软硬阔混交林': 'RYK',
        '硬阔混交林': 'YK'
    }

    try:
        # 获取数据文件（最多取4个）
        files = [f for f in os.listdir(input_dir)
                 if f.endswith(('.xlsx', '.xls'))][:4]
        n_files = len(files)  # 实际文件数量

        # 初始化画布（保持2x2布局）
        fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=120)
        fig.subplots_adjust(hspace=0.35, wspace=0.3)  # 调整子图间距

        # 遍历处理文件
        for idx, (filename, ax) in enumerate(zip(files, axs.flat)):
            # 文件处理
            filepath = os.path.join(input_dir, filename)
            raw_df = pd.read_excel(filepath, sheet_name='每木检尺及测高记录表')

            # 数据清洗
            clean_df = raw_df[
                (~raw_df['状态'].isin(['枯立木', '倒木'])) &
                (raw_df['胸径'] > 0)  # 确保胸径为正值
                ].copy()

            # 获取显示名称
            basename = name_mapping.get(
                os.path.splitext(filename)[0],
                f'Unknown{idx}'
            )

            # 调用绘图函数
            plot_diameter_distribution(clean_df, '胸径', basename, ax)

            # 设置子图x轴标签
            ax.set_xlabel('径阶\nDiameter Class /cm',
                          fontsize=13,
                          labelpad=10,
                          fontweight='medium')

        # 隐藏未使用的子图
        for j in range(n_files, 4):
            axs.flat[j].axis('off')  # 彻底隐藏多余子图

        # 保存和显示
        plt.tight_layout(pad=3.0)
        plt.show()

    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        if 'files' in locals():
            print(f"当前处理文件: {filename}")


if __name__ == "__main__":
    # 执行前检查中文字体
    from matplotlib.font_manager import fontManager

    chinese_fonts = [f.name for f in fontManager.ttflist if 'SimSun' in f.name]
    if not chinese_fonts:
        print("警告：系统中未找到宋体字体，建议安装中文字体包")

    main()