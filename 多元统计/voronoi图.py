import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# 生成一些随机点作为样方
np.random.seed(0)  # 设置随机种子以便结果可重复
points = np.random.rand(15, 2)  # 生成15个二维随机点

# 创建Voronoi图
vor = Voronoi(points)

# 绘制Voronoi图
fig, ax = plt.subplots()
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_alpha=0.4, line_width=2, point_size=2)

# 绘制原始点
ax.plot(points[:, 0], points[:, 1], 'o')

# 设置图形标题和坐标轴标签
ax.set_title('Voronoi Diagram')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')

# 显示图形
plt.show()