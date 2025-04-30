import os
import pandas as pd
import math
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False
def Pinus_koraiensis(D):#红松材积
    H= 1.3 + 30.09177 * np.exp(-16.3698 / D)
    Dw= -0.08197754 + 1.00135 * D
    v=6.3527721e-05 * Dw ** 1.9435455 * H ** 0.89689361
    return v
def Picea(D):#云杉
    H = 1.3 + 32.21942 * np.exp(-17.06452 / D)
    Dw = -0.03871096 + 0.9971613 * D
    v=6.1859978e-05 * Dw ** 1.85577513 * H ** 1.0070547
    return v

def Abies(D):#冷杉
    H=1.3+30.63747*np.exp(-14.82347/D)
    Dw=-0.08269092+0.998732*D
    v=6.1859978e-05*Dw**1.85577513*H**1.0070547
    return v
def Larix(D):#落叶松
    v = 0.0006576508 * D** 2.018535
    return v
def Fraxinus(D):#水曲柳
    H=1.3+24.84302*np.exp(-10.26841/D)
    Dw=-0.1340759+0.9904621*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Juglans (D):#胡桃楸
    H = 1.3 + 24.84302 * np.exp(-10.26841 / D)
    Dw = -0.1340759 + 0.9904621 * D
    v = 4.1960698e-05 * Dw ** 1.9094595 * H ** 1.0413892
    return v
def Phellodendron(D):#黄菠萝
    H = 1.3 + 24.84302 * np.exp(-10.26841 / D)
    Dw = -0.1340759 + 0.9904621 * D
    v = 4.1960698e-05 * Dw ** 1.9094595 * H ** 1.0413892
    return v
def Tilia (D):#紫椴
    H=1.3+23.83062*np.exp(-11.08188/D)
    Dw=-0.3178201+0.993646*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Acer (D):#色木槭
    H = 1.3 + 19.66254 * np.exp(-8.601885 / D)
    Dw = -0.1948627 + 0.9913445 * D
    v = 4.1960698e-05 * Dw ** 1.9094595 * H ** 1.0413892
    return v
def Ulmus (D):#榆树
    H=1.3+24.17011*np.exp(-12.04452/D)
    Dw=-0.09734+0.9870044*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Quercus (D):#蒙古栎
    H=1.3+17.75595*np.exp(-7.737241/D)
    Dw=0.2083972+0.9771802*D
    v=6.1125534e-05*Dw**1.8810091*H**0.94462565
    return v
def Betula_costata (D):#枫桦
    H=1.3+24.01214*np.exp(-8.630002/D)
    Dw=-0.1172836+0.9899376*D
    v=4.1960698e-05*Dw**1.9094595*H**1.0413892
    return v
def Betula_davurica (D):#黑桦
    H=1.3+20.4484*np.exp(-8.399443/D)
    Dw=0.02539258+0.9797975*D
    v=5.2786451e-05*Dw**1.7947313*H**1.0712623
    return v
def Betula_platyphylla (D):#白桦
    H=1.3+26.4656*np.exp(-8.740813/D)
    Dw=-0.1689837+1.006111*D
    v=5.1935163e-05*Dw**1.8586884*H**1.0038941
    return v
def Populus_davidiana (D):#山杨
    H=1.3+27.60532*np.exp(-9.567569/D)
    Dw=-0.2641493+1.009529*D
    v=5.3474319e-05*Dw**1.8778994*H**0.99982785
    return v
def Populus(D):#大青杨
    H=1.3+26.51351*np.exp(-10.29054/D)
    Dw=-0.02728948+0.990946*D
    v=5.3474319e-05*Dw**1.8778994*H**0.99982785
    return v
def broadleaf(D):#杂木材积？？？
    Dw=-0.41226+0.97241*D
    H=25.791498-378.521967/(Dw+17)
    v=0.00004331*Dw**1.73738556*H**1.22688346
    return v
# 树木距离计算函数
def distance(row1, row2):
    return math.sqrt((row1['x'] - row2['x']) ** 2 + (row1['y'] - row2['y']) ** 2)
def heigh(row1, row2):
    return math.sqrt((row1['heigh'] - row2['heigh']) ** 2 )
def broadleaf(D):#杂木材积？？？
    Dw=-0.41226+0.97241*D
    H=25.791498-378.521967/(Dw+17)
    v=0.00004331*Dw**1.73738556*H**1.22688346
    return v
 # 计算材积
def volum(D,tree_name):
    if tree_name == '红松':
        v = Pinus_koraiensis(D)
    elif tree_name == '水曲柳':
        v = Fraxinus(D)
    elif tree_name == '红皮云杉' or tree_name == '鱼鳞云杉':
        v = Picea(D)
    elif tree_name == '冷杉' or tree_name == '辽东冷杉':
        v = Abies(D)
    elif tree_name == '大青杨':
        v = Populus(D)
    elif tree_name == '落叶松':
        v = Larix(D)
    elif tree_name == '胡桃楸':
        v = Juglans(D)
    elif tree_name == '黄菠萝':
        v = Phellodendron(D)
    elif tree_name == '色木':
        v = Acer(D)
    elif tree_name == '春榆' or tree_name == '裂叶榆':
        v = Ulmus(D)
    elif tree_name == '枫桦':
        v = Betula_costata(D)
    elif tree_name == '柞树':
        v = Quercus(D)
    elif tree_name == '黑桦':
        v = Betula_davurica(D)
    elif tree_name == '紫椴':
        v = Tilia(D)
    elif tree_name == '白桦':
        v = Betula_platyphylla(D)
    elif tree_name == '山杨':
        v = Populus_davidiana(D)
    else:
        v = broadleaf(D)
    return v
def canopy_crow_create(ds,selected_trees_df,disruptions_trees_df,basename):
    # 目标树和干扰树坐标图
    # 创建目标树的 GeoDataFrame
    gpd_selected_trees = gpd.GeoDataFrame(
        selected_trees_df,
        geometry=gpd.points_from_xy(selected_trees_df['x'], selected_trees_df['y'])
    )

    # 创建干扰树的 GeoDataFrame
    gpd_disruptions_trees = gpd.GeoDataFrame(
        disruptions_trees_df,
        geometry=gpd.points_from_xy(disruptions_trees_df['x'], disruptions_trees_df['y'])
    )

    # 使用 plt.figure() 创建一个新的图形
    fig, ax = plt.subplots()
    # 绘制目标树，颜色为绿色
    # 提取点的坐标
    x, y = gpd_selected_trees.geometry.x, gpd_selected_trees.geometry.y
    # 使用 scatter 绘制点，设置形状为三角形，边缘颜色为红色，填充颜色为白色
    ax.scatter(x, y, marker='*', color='white', edgecolor='green', label='目标树', s=20)  # s 控制点的大小
    # 绘制干扰树，颜色为红色
    # 提取点的坐标
    x, y = gpd_disruptions_trees.geometry.x, gpd_disruptions_trees.geometry.y
    # 使用 scatter 绘制点，设置形状为三角形，边缘颜色为红色，填充颜色为白色
    ax.scatter(x, y, marker='^', color='white', edgecolor='red', label='干扰树', s=10)  # s 控制点的大小
    # 设置标题和坐标轴标签
    plt.title('样地{}样木分布图'.format(basename))
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.grid(True)
    plt.legend()  # 显示图例

    for df in [selected_trees_df,disruptions_trees_df]:
        for index, row in df.iterrows():  # 使用 iterrows() 来迭代行和索引
            theta = np.arange(0, 2 * np.pi, np.pi / 90)
            a = row['东']
            b = row['西']
            c = row['南']
            d = row['北']
            # 计算树冠投影的椭圆
            crown_radius_x = (a + b) / 2 if pd.notna(a) and pd.notna(b) else 0
            crown_radius_y = (c + d) / 2 if pd.notna(c) and pd.notna(d) else 0
            t = theta
            crown_x = crown_radius_x * np.cos(t) + row['x']
            crown_y = crown_radius_y * np.sin(t) + row['y']
            plt.plot(crown_x, crown_y,color='black')



file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\燕安大径材培育规划\抚育小班'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\目标树和干扰树分布图'
name_list=os.listdir(file_path)

a=0
out_df={'plot':[],'目标树平均胸径':[],'干扰树平均胸径':[],'干扰树株树':[],'干扰树蓄积':[]}
for i in name_list:
    basename = i.rsplit('.', 1)[0]  # 注意：i 需要在这段代码之前被定义
    a+=1
    data=os.path.join(file_path,i)
    data=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    #数据清洗
    data=data.copy()
    data = data[~data['状态'].isin(['枯立木', '倒木'])]
    data['树高'].dropna(inplace=True)
    # 数据格式：DataFrame，列名为 'x', 'y', 'diameter', 'species'
    trees_df=pd.DataFrame()
    trees_df['species'] = data['树种']
    trees_df['x']=data['X']
    trees_df['y']=data['Y']
    trees_df['东']=data['东']
    trees_df['南'] = data['南']
    trees_df['西'] = data['西']
    trees_df['北'] = data['北']
    trees_df['diameter']=data['胸径']
    trees_df['heigh']=data['树高']
    trees_df['species']=data['树种']
    trees_df['冠幅平均值']=(data['东']+data['西']+data['南']+data['北'])/4
    average_diameter=trees_df['diameter'].mean()
    #计算材积
    trees_df['volum'] = trees_df.apply(lambda row: volum(row['diameter'], row['species']), axis=1)
    # 指定树种
    preferred_species = {'红松', '水曲柳', '胡桃楸', '黄菠萝', '紫椴', '云杉', '冷杉'}

    # 过滤并排序DataFrame中的树木
    filtered_sorted_trees = trees_df[trees_df['species'].isin(preferred_species)].sort_values(by='diameter',
                                                                                              ascending=False)
    filtered_sorted_trees=filtered_sorted_trees[filtered_sorted_trees['diameter']>=average_diameter]
    selected_trees = []
    # 尝试选择最多100棵树，满足距离条件
    for index, tree in filtered_sorted_trees.iterrows():
        if all(distance(tree, selected_tree) > 12 for selected_tree in selected_trees):
            selected_trees.append(tree)
        if len(selected_trees) >= 15:
            break

    # 如果选择的树木不足100株，则从剩余树木中选择
    if len(selected_trees) < 15:
        remaining_sorted_trees = trees_df[~trees_df.index.isin([t.name for t in selected_trees])].sort_values(
            by='diameter', ascending=False)
        remaining_sorted_trees = remaining_sorted_trees[remaining_sorted_trees['diameter'] >= average_diameter]
        for index, tree in remaining_sorted_trees.iterrows():
            if all(distance(tree, selected_tree) > 12 for selected_tree in selected_trees):
                selected_trees.append(tree)
            if len(selected_trees) >= 15:
                break

    # 将选定的树木转换回DataFrame
    selected_trees_df = pd.DataFrame(selected_trees)

    #干扰树选择
    filtered_disruptions_trees = trees_df[~trees_df['species'].isin(preferred_species)].sort_values(by='diameter',
                                                                                                    ascending=False)
    disruptions_trees=[]
    for index, tree in filtered_disruptions_trees.iterrows():
        for index,selected_tree in selected_trees_df.iterrows():
            crown=selected_tree['冠幅平均值']+tree['冠幅平均值']
            if (heigh(tree, selected_tree) < 5)&(distance(tree, selected_tree) <= 1.2*crown):
                disruptions_trees.append(tree)

    # 将干扰树转换回DataFrame
    disruptions_trees_df = pd.DataFrame(disruptions_trees)

    #绘图
    #树冠图
    data=data[data.index.isin(selected_trees_df.index)|data.index.isin(disruptions_trees_df.index)]
    canopy_crow_create(data,selected_trees_df,disruptions_trees_df,basename)
    plt.savefig(os.path.join(out_path, basename + '.png'))
    plt.show()
    plt.clf()

    #目标树平均胸径
    selectedaverage_diameter = selected_trees_df['diameter'].mean()
    disruptions_trees_diameter=disruptions_trees_df['diameter'].mean()
    disruptions_denisity=len(disruptions_trees_df['x'])
    disruptions_trees_vol=disruptions_trees_df['volum'].sum()
    out_df['plot'].append(basename)
    out_df['目标树平均胸径'].append(selectedaverage_diameter)
    out_df['干扰树平均胸径'].append(disruptions_trees_diameter)
    out_df['干扰树株树'].append(disruptions_denisity)
    out_df['干扰树蓄积'].append(disruptions_trees_vol)
    #print(basename,selected_trees_df)


out_df=pd.DataFrame(out_df)
out_df.to_excel(os.path.join(out_path,'模拟采伐.xlsx'),index=False)


