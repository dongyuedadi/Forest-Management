import os
import pandas as pd
import numpy as np

file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list = os.listdir(file_path)

# 定义高度区间和标签
bins = [30, 50, 100, float('inf')]
labels = ['30-50', '50-100', '大于100']
def process_file(file_name, bins, labels):
    # 读取Excel文件
    data_path = os.path.join(file_path, file_name)
    basename = file_name.rsplit('.', 1)[0]
    data = pd.read_excel(data_path, sheet_name='30cm以上幼苗幼树高调查记录')
    # 删除'树高'列中包含缺失值的行
    data = data.dropna(subset=['树高'])
    # 创建一个空的DataFrame来存储结果
    results = []
    # 计算总数量
    counts1, _ = np.histogram(data['树高'], bins=bins)
    total_count = sum(counts1)
    # 按树种分组
    for species in data['树种'].unique():
        species_data = data[data['树种'] == species]
        # 计算每个区间的数量
        counts, _ = np.histogram(species_data['树高'], bins=bins)
        # 循环处理每个区间
        for idx, label in enumerate(labels):
            proportion = counts[idx] / total_count
            results.append({
                'plot': basename,
                '树种': species,
                '树高区间': label,
                '株树比例': proportion,
                '总株树': total_count
            })

    return results

# 处理每个文件并收集结果
all_results = []
for i in name_list:
    if i.endswith('.xlsx') or i.endswith('.xls'):  # 确保只处理Excel文件
        all_results.extend(process_file(i, bins, labels))

# 将结果转换为DataFrame
out_df = pd.DataFrame(all_results)
out_df['树高区间比例']=out_df.groupby(['plot','树高区间'])['株树比例'].transform('sum')
out_df['树种比例']=out_df.groupby(['plot','树种'])['株树比例'].transform('sum')
# 打印或保存输出DataFrame
print(out_df)
out_df.to_excel(os.path.join(out_path, '30cm以上更新树种高度区间分布.xlsx'), index=False)
out_df['树种株树']=out_df['树种比例']*out_df['总株树']
out_df1=out_df.drop_duplicates(subset=['plot','树种'])
out_df1.to_excel(os.path.join(out_path, '30cm以上更新树种株树.xlsx'), index=False)