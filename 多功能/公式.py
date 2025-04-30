import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置使用 LaTeX 渲染数学公式
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

def save_formula_image(formula, filename, dpi=300):
    fig = plt.figure(figsize=(3, 2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.text(0.5, 0.5, formula, fontsize=20, ha='center', va='center')
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.5)
    plt.close()

# 定义皮尔逊相关系数公式
pearson_formula = r'$\rho_{X,Y}=\frac{\mathrm{cov}(X,Y)}{\sigma_X\sigma_Y}$'
output_file = r"C:\Users\hys5637428\Desktop\不同阶段经营模式\3.15课题汇报\公式.jpg"
save_formula_image(pearson_formula, output_file)
# 保存公式图像
print(pearson_formula)