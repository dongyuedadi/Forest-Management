import os
import pandas as pd
from itertools import combinations

def jaccard_index(set1, set2):
    """计算两个集合的Jaccard相似系数"""
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0


# 文件路径设置
file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'

# 初始化数据结构
forest_types = ['软阔混交林', '软硬阔混交林', '硬阔混交林']
species_data = {
    '乔木': {ft: set() for ft in forest_types},
    '灌木': {ft: set() for ft in forest_types},
    '草本': {ft: set() for ft in forest_types}
}

# 读取并处理所有森林类型数据
for file in os.listdir(file_path):
    if not file.endswith('.xlsx'):
        continue

    # 提取森林类型标识
    ft = next((x for x in forest_types if x in file), None)
    if not ft:
        continue

    # 读取数据
    full_path = os.path.join(file_path, file)
    try:
        tree_df = pd.read_excel(full_path, sheet_name='每木检尺及测高记录表').dropna(subset=['树种'])
        shrub_df = pd.read_excel(full_path, sheet_name='植被（灌木）调查表').dropna(subset=['种名'])
        herb_df = pd.read_excel(full_path, sheet_name='植被（草本）调查表').dropna(subset=['种名'])
    except Exception as e:
        print(f"读取文件{file}出错: {str(e)}")
        continue

    # 收集物种数据（不考虑分带）
    species_data['乔木'][ft].update(tree_df['树种'].unique())
    species_data['灌木'][ft].update(shrub_df['种名'].unique())
    species_data['草本'][ft].update(herb_df['种名'].unique())

# 计算β多样性矩阵
results = []
for veg_type in ['乔木', '灌木', '草本']:
    # 生成所有两两组合
    for ft1, ft2 in combinations(forest_types, 2):
        ji = jaccard_index(species_data[veg_type][ft1], species_data[veg_type][ft2])
        results.append({
            '植被类型': veg_type,
            '群落1': ft1,
            '群落2': ft2,
            'Jaccard指数': round(ji, 4),
            'β多样性': round(1 - ji, 4)  # β多样性=1-Jaccard相似度
        })

# 创建结果DataFrame
result_df = pd.DataFrame(results).sort_values(['植被类型', '群落1'])

# 保存结果
output_path = os.path.join(out_path, '群落间β多样性分析.xlsx')
result_df.to_excel(output_path, index=False)

print("分析完成，结果已保存至:", output_path)
print("\n结果预览:")
print(result_df)
