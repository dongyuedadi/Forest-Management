import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 文件路径
file_path = r'C:\Users\hys5637428\Desktop\模型拟合\使用数据(1).xls'
out_path = r'C:\Users\hys5637428\Desktop\模型拟合'

# 读取数据
data = pd.read_excel(file_path)
df = data.copy()

# 选择自变量和因变量
X = df['年龄']  # 自变量
y = df['株数']        # 因变量

# 添加常数项（截距）
X = sm.add_constant(X)

# 拟合线性回归模型
model = sm.OLS(y, X)  # 普通最小二乘法
results = model.fit()  # 拟合模型

# 输出回归结果
print(results.summary())

# 绘制散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['年龄'], y=df['株数'], label='数据点')

# 绘制回归线
plt.plot(df['年龄'], results.fittedvalues, color='red', label='回归线')

# 添加标题和标签
plt.title('线性回归分析: 年龄 vs 株数')
plt.xlabel('年龄')
plt.ylabel('株数')
plt.legend()

# 显示图形
plt.show()