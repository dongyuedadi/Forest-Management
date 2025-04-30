import pandas as pd
import os

# 读取数据
file_path = r"C:\Users\hys5637428\Desktop\模型拟合"
data_file = os.path.join(file_path, '黑龙江地方2010_2015年一类样地数据.xlsx')
index_file = os.path.join(file_path, '使用数据.xls')

# 加载Excel文件到DataFrame
data = pd.read_excel(data_file)
data_index = pd.read_excel(index_file)

# 定义变量和阈值（这些可以从外部文件或配置中读取）
variables = [
    '土壤厚度', '腐殖质厚度', '落叶厚度', '灌木覆盖度', '灌木平均高', '草本覆盖度', '草本平均高',
    '植被总覆盖', '优势树种%1', '年龄1', '优势dg1', '平均直径1', '平均树高1', 'SCI1', '株数1',
    'bas1', 'SDI1', 'm活1', 'm枯倒1', 'W干1', 'W枝1', 'W叶1', 'W根1', 'w地上1', 'w全树1','C全树1'
]

target_thresholds = {
    '土壤厚度': 54.5, '腐殖质厚度': 15.0, '落叶厚度': 5.0, '灌木覆盖度': 35.0, '灌木平均高': 1.47,
    '草本覆盖度': 70.0, '草本平均高': 0.4, '植被总覆盖': 90.0, '优势树种%1': 92.93, '年龄1': 99.9,
    '优势dg1': 25.69, '平均直径1': 22.293, '平均树高1': 12.09, 'SCI1': 11.098, '株数1': 2718.3,
    'bas1': 23.2448, 'SDI1': 1411.09, 'm活1': 124.76, 'm枯倒1': 20.8, 'W干1': 101.53327,
    'W枝1': 41.534077, 'W叶1': 4.4809494, 'W根1': 33.904444, 'w地上1': 146.74941, 'w全树1': 180.51575,'C全树1':186.2544}


def calculate_multifunctionality_index(data, data_index, stage):
    # 筛选数据
    index_list = data_index[data_index['判别式2分组'] == stage]['样地号'].unique()
    filtered_data = data[data['样地号'].isin(index_list)]
    # 计算得分
    scores = filtered_data[variables].apply(lambda col: col / target_thresholds[col.name]).clip(0, 1)
    multifunctionality_score = scores.sum(axis=1) / len(variables)
    # 输出多功能性指数的平均值
    multifunctionality_index = multifunctionality_score.mean()
    print(f'生态系统服务多功能性指数{stage}阶段: {multifunctionality_index}')

# 调用函数计算多功能性指数
for stage in [1, 2, 3]:
    calculate_multifunctionality_index(data, data_index, stage)