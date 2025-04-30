import pandas as pd
import matplotlib.pyplot as plt

# 数据准备
data = {
    "林分类型": ["软阔混交林", "软硬阔混交林", "硬阔混交林"],
    "活立木蓄积": [228.77, 188.92, 224.26],
    "胸高断面积": [29.61, 26.86, 29.47],
    "平均胸径": [17.77, 17.55, 21.71],
    "胸径标准差": [8.52, 7.10, 10.91]
}
df = pd.DataFrame(data)

# 创建画布（学术级参数）
plt.figure(figsize=(12, 6), dpi=300)
plt.rcParams.update({
    'font.size': 12,
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold'
})

# 绘制多折线图
markers = ['o', 's', 'D', '^']  # 差异化标记样式
colors = ['#2E75B6', '#ED7D31', '#70AD47', '#FFC000']  # Office主题色

for i, col in enumerate(df.columns[1:]):
    plt.plot(df["林分类型"], df[col],
             marker=markers[i],
             color=colors[i],
             linewidth=2,
             markersize=8,
             label=col)

# 图表优化（网页1）
plt.title("不同林分类型结构特征对比\nStructural Characteristics of Forest Stands", pad=20)
plt.xlabel("林分类型", labelpad=15)
plt.ylabel("标准化指标值", labelpad=15)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)

# 数值标注（网页4）
for col in df.columns[1:]:
    for idx, val in enumerate(df[col]):
        plt.annotate(f"{val:.2f}",
                    (df["林分类型"][idx], val),
                    textcoords="offset points",
                    xytext=(0, 10 if idx%2 else -15),
                    ha='center',
                    fontsize=9,
                    arrowprops=dict(arrowstyle="-", color="grey"))

plt.tight_layout()
plt.savefig("forest_stand_analysis.png", bbox_inches='tight')
plt.show()