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
sorted_df = dataBA.sort_values(by='胸高断面积', ascending=False)
num_rows_to_select = len(sorted_df) // 2
BA_MAX = sorted_df.iloc[:num_rows_to_select]['林分胸高断面积'].mean() * len(sorted_df) / 2

# 计算各个样地各个树种大小比均值
out_df['树种大小比'] = out_df.groupby(['plot', '树种'])['大小比'].transform('mean')
Species_U = out_df.drop_duplicates(subset=['plot', '树种'])

# 计算各树种相对显著度（这里假设'树种优势度'列已存在于dataBA中）
Species_dominance = dataBA.drop_duplicates(subset=['plot', '树种'])

# 计算目的树种优势度
Dsp_DF = []
for plots in Species_dominance['plot'].unique():
    for species in ['水曲柳', '胡桃楸', '黄菠萝', '紫椴', '红松', '云杉', '冷杉', '辽东冷杉']:
        try:
            dom_values = Species_dominance[(Species_dominance['树种'] == species) & (Species_dominance['plot'] == plots)]['树种优势度'].values[0]
            U_values = Species_U[(Species_U['树种'] == species) & (Species_U['plot'] == plots)]['树种大小比'].values
            if len(U_values) > 0:
                Dsp = np.sqrt(dom_values * (1 - U_values.mean()))
                Dsp_DF.append({'plot': plots, '树种': species, '目的树种优势度': Dsp})
        except IndexError:
            continue  # 如果找不到对应的行，则跳过

Dsp_DF = pd.DataFrame(Dsp_DF)
Dsp_DF.to_excel(os.path.join(out_path, '目的树种优势度.xlsx'), index=False)

# 计算林分长势
dataBA_dom = dataBA.drop_duplicates(subset=['plot'])
Dominance_DF = []
for i in dataBA_dom['plot'].unique():
    BA = dataBA_dom[dataBA_dom['plot'] == i]['林分胸高断面积'].values[0]
    U0 = df_zero[df_zero['plot'] == i]['大小比概率'].values[0]
    Dominance =np.sqrt(U0 * ((BA_MAX/2) / (BA_MAX - BA)))  if BA != BA_MAX else 0  # 避免除以零
    Dominance_DF.append({'plot': i, '林分优势度': Dominance})

Dominance_DF = pd.DataFrame(Dominance_DF)
Dominance_DF.to_excel(os.path.join(out_path, '林分优势度.xlsx'), index=False)
print(Dominance_DF)