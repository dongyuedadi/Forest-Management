import pandas as pd
import numpy as np
import os

# 挑选距离参照树最近的四株相邻木
def get_distance(data, inX):
    tree_points = data[['X轴', 'Y轴']].values
    tree = tree_points[inX]
    diffMat = np.tile(tree, (len(tree_points), 1)) - tree_points
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = np.sqrt(sqDistances)
    sortedDistIndicies = distances.argsort()
    return [sortedDistIndicies[:5], distances[sortedDistIndicies[:5]]]

# 定义大小比
def comparison_DBH(dbhs):
    ref_dia = dbhs[0]
    k_values = [1 if d >= ref_dia else 0 for d in dbhs[1:]]
    M = np.sum(k_values) / 4
    return M

file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list = os.listdir(file_path)

# 空间结构参数计算
U_list = []
plot_list = []
BH_list = []
Sps_list = []

for names in name_list:
    data = pd.read_excel(os.path.join(file_path, names), sheet_name='每木检尺及测高记录表')
    data = data[~data['状态'].isin(['枯立木', '倒木'])]
    data.loc[:, ['X轴', 'Y轴']] = data[['X轴', 'Y轴']].ffill()
    diameter = data['胸径'].values
    sps = data['树种'].values

    for i in range(len(data)):
        ids = get_distance(data, i)
        U = comparison_DBH(diameter[ids[0][1:]])  # 注意这里只取相邻四株的胸径
        U_list.append(U)
        BH_list.append(i + 1)  # 编号从1开始
        plot_list.append(names.rsplit('.', 1)[0])
        Sps_list.append(sps[ids[0][0]])

out_df = pd.DataFrame({
    '大小比': U_list,
    '树种': Sps_list,
    '编号': BH_list,
    'plot': plot_list
})

# 计算各个样地大小比为0的株树比例
df_zero = out_df.groupby('plot')['大小比'].apply(lambda x: (x == 0).mean()).reset_index(name='大小比概率')

# 导入林分胸高断面积计算林分潜在最大胸高断面积
dataBA = pd.read_excel(os.path.join(out_path, '林分BA.xlsx'))

# 计算各个样地目的树种总的大小比均值
out_df=out_df[out_df['树种'].isin(['红松','水曲柳','胡桃楸','黄菠萝','紫椴','冷杉'])]
out_df['树种大小比'] = out_df.groupby(['plot'])['大小比'].transform('mean')
Species_U = out_df.drop_duplicates(subset=['plot'])

# 计算各树种相对显著度（这里假设'树种优势度'列已存在于dataBA中）
dataBA=dataBA[dataBA['树种'].isin(['红松','水曲柳','胡桃楸','黄菠萝','紫椴','冷杉'])]
Species_dominance=dataBA.groupby(['plot'])['树种优势度'].transform('mean')
Species_dominance = dataBA.drop_duplicates(subset=['plot'])
print(Species_dominance)
#输出目的树种胸高断面积
dataBA['林分目的树种胸高断面积']=dataBA.groupby('plot')['胸高断面积'].transform('sum')
dataBA=dataBA.drop_duplicates(subset=['plot'])
dataBA.to_excel(os.path.join(out_path,'林分目的树种BA.xlsx'),index=False)
# 计算目的树种优势度
Dsp_DF = []
for plots in Species_dominance['plot'].unique():
    dom_values = Species_dominance[Species_dominance['plot'] == plots]['树种优势度'].values[0]
    U_values = Species_U[Species_U['plot'] == plots]['树种大小比'].values
    Dsp = np.sqrt(dom_values * (1 - U_values.mean()))
    print(plots, Dsp)

