import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

def canopy_crow_create(ds, outpath):
    coods = ds.loc[:, ['X轴', 'Y轴']].values
    plt.scatter(coods[:, 0], coods[:, 1])

    for index, row in ds.iterrows():  # 使用 iterrows() 来迭代行和索引
        print(row)
        try:
            theta = np.arange(0, 2 * np.pi, np.pi / 90)
            a = row['东']
            b = row['西']
            c = row['南']
            d = row['北']
            # 这里假设 a, b 是树冠在 x 方向上的宽度，c, d 是 y 方向上的宽度
            # 但是这样的计算可能不准确，因为通常树冠不是规则的椭圆或圆形
            # 计算树冠投影的椭圆
            crown_radius_x = (a + b) / 2 if pd.notna(a) and pd.notna(b) else 0
            crown_radius_y = (c + d) / 2 if pd.notna(c) and pd.notna(d) else 0

            t = theta
            crown_x = crown_radius_x * np.cos(t) + row['X轴']
            crown_y = crown_radius_y * np.sin(t) + row['Y轴']

            plt.plot(crown_x, crown_y)
        except Exception as e:
            print(f"Error processing index {index}: {e}")

    plt.xlabel('E(x)')
    plt.ylabel('E(y)')
    plt.title('树冠投影图')
    plt.savefig(os.path.join(outpath, '树冠投影图.png'), dpi=300)
    plt.show()


file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'

# 确保输出目录存在
os.makedirs(out_path, exist_ok=True)

name_list = os.listdir(file_path)
for i in name_list:
    if i.endswith('.xlsx') or i.endswith('.xls'):  # 只处理 Excel 文件
        data_path = os.path.join(file_path, i)
        data = pd.read_excel(data_path, sheet_name='每木检尺及测高记录表')
        # 数据清洗
        data = data[~data['状态'].isin(['枯立木', '倒木'])]
        if data['X轴'].isnull().all():
            print(f"文件 {i} 中 'X轴' 列全是空的或 NaN 值")
            continue  # 跳过当前文件
        # 填充缺失值
        data[['东', '南', '西', '北']].fillna(0, inplace=True)
        # 创建树冠投影图
        canopy_crow_create(data, out_path)