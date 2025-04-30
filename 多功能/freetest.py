import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 字体设置（确保中文显示）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

# 示例数据（中英双语标签）
data = {
    "植被类型 (Vegetation type)": ["乔木 (Tree)", "乔木 (Tree)", "乔木 (Tree)",
                              "灌木 (Shrub)", "灌木 (Shrub)", "灌木 (Shrub)",
                              "草本 (Herb)", "草本 (Herb)", "草本 (Herb)"],
    "群落1 (Community 1)": ["软阔混交林 (Soft-broad)", "软硬阔混交林 (Soft-hard)", "软阔混交林 (Soft-broad)",
                         "软阔混交林 (Soft-broad)", "软硬阔混交林 (Soft-hard)", "软阔混交林 (Soft-broad)",
                         "软阔混交林 (Soft-broad)", "软硬阔混交林 (Soft-hard)", "软阔混交林 (Soft-broad)"],
    "群落2 (Community 2)": ["软硬阔混交林 (Soft-hard)", "硬阔混交林 (Hard-broad)", "硬阔混交林 (Hard-broad)",
                         "软硬阔混交林 (Soft-hard)", "硬阔混交林 (Hard-broad)", "硬阔混交林 (Hard-broad)",
                         "软硬阔混交林 (Soft-hard)", "硬阔混交林 (Hard-broad)", "硬阔混交林 (Hard-broad)"],
    "Jaccard指数 (Jaccard index)": [0.6522, 0.5909, 0.5909, 0.5333, 0.4375, 0.6, 0.4103, 0.369, 0.3562],
    "β多样性 (β-diversity)": [0.3478, 0.4091, 0.4091, 0.4667, 0.5625, 0.4, 0.5897, 0.631, 0.6438]
}
df = pd.DataFrame(data)

# Jaccard指数热图
plt.figure(figsize=(14, 7))
heatmap_data = df.pivot(index="植被类型 (Vegetation type)",
                        columns=["群落1 (Community 1)", "群落2 (Community 2)"],
                        values="Jaccard指数 (Jaccard index)")
sns.heatmap(
    heatmap_data,
    annot=True,
    cmap="binary",
    vmin=0.3,
    vmax=0.7,
    annot_kws={"fontsize":9},
    linewidths=0.5,
    cbar_kws={'label': 'Jaccard指数值 (Jaccard index value)'}
)
plt.title("Jaccard相似性指数分析\nJaccard Similarity Index Analysis", fontsize=14, pad=20)
plt.xticks(rotation=0, ha='center', fontsize=9)
plt.yticks(fontsize=9)
plt.xlabel("群落组合 (Community combinations)", fontsize=11)
plt.ylabel("植被类型 (Vegetation type)", fontsize=11)
plt.tight_layout()
plt.show()