#群落数量动态指数
def calculate_product(lst):
    product = math.prod(lst)
    # 检查列表中是否存在负数
    has_negative = any(num < 0 for num in lst)
    # 如果存在负数且乘积为正，则取反
    if has_negative and product > 0:
        product = -product
    return product

import math
import matplotlib.pyplot as plt
import pandas as pd
import os
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

file_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\静态生命表'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\标准化静态生命表'
name_list=os.listdir(file_path)
sheet_list=[['水曲柳','胡桃楸','色木槭','红松','春榆'],
            ['紫椴','春榆','色木槭','水曲柳','糠椴'],
            ['水曲柳','糠椴','山杨','胡桃楸','紫椴'],
             ['山杨','紫椴','糠椴','水曲柳','白桦']]
#种群数量变化动态指数字典
Vpi_dict={'plot':[],'树种':[],'Vpi':[]}
#群落数量动态变化
Vc_list=[]
Vc_plot=[]
Vc=[]
sht=0
for I in name_list:
    print(sht)
    data_path = os.path.join(file_path, I)
    sheet_name = sheet_list[sht]
    my_path = os.path.join(out_path, f'{I}')
    #标准化径阶，填充不存在径阶值为0
    with pd.ExcelWriter(my_path,
                        engine='xlsxwriter') as writer:
        for j in sheet_name:
            data = pd.read_excel(data_path, sheet_name=j)
            df = data.copy()
            df['径阶'] = pd.to_numeric(df['径阶'], errors='coerce').astype(int)
            df['株树'] = pd.to_numeric(df['株树'], errors='coerce').astype(int)
            my_dict = {i: 0 for i in range(2, max(df['径阶']), 2)}
            excel_dict = df.set_index('径阶').to_dict()['株树']
            for key in excel_dict.keys():
                my_dict[key] = excel_dict[key]
                # 将字典转换成列表，每个元素是一个包含键和值的元组
            data_list = [(k, v) for k, v in my_dict.items()]
            # 将列表转换成DataFrame，列名分别为'Key'和'Value'
            my_pf = pd.DataFrame(data_list, columns=['径阶', '株树'])
            sheet_name = f'{j}'
            my_pf.to_excel(writer, sheet_name=sheet_name, index=False)

            # 计算种群数量变化动态指数
            # 径阶和对应的株树数量
            diameter_classes = list(my_pf['径阶'])  # 径阶列表
            tree_counts = list(my_pf['株树'])  # 对应的株树数量
            # 计算相邻两径阶间的个体数量变化动态 V_n
            V_n = []
            for i in range(len(tree_counts) - 1):
                S_n = tree_counts[i]
                S_n_plus_1 = tree_counts[i + 1]
                if max(S_n, S_n_plus_1) == 0:
                    V_n.append(0)
                else:
                    V_n.append((S_n - S_n_plus_1) / max(S_n, S_n_plus_1))
            # 计算株树不为0的径阶个数 k
            k = sum(1 for count in tree_counts if count != 0)
            # 找到株树S中最小非零数 min_non_zero_Sn
            min_non_zero_Sn = min(count for count in tree_counts if count > 0)
            #计算种群动态变化指数 V_pi
            sum_Sn = sum(tree_counts)  # 所有 Sn 的总和（包括0）
            # 计算 sum(Sn*Vn)，但只考虑那些有对应 V_n 值的 Sn（在这个例子中，这会自动排除与0相邻的项）
            sum_Sn_Vn = sum(S_n * V_n_i for S_n, V_n_i in zip(tree_counts[:-1], V_n))
            # 计算 V_pi
            V_pi = (1 / (
                        k * min_non_zero_Sn * sum_Sn)) * sum_Sn_Vn if k != 0 and min_non_zero_Sn != 0 and sum_Sn != 0 else 0
            basename = I.rsplit('.', 1)[0]
            Vpi_dict['plot'].append(basename)
            Vpi_dict['树种'].append(j)
            Vpi_dict['Vpi'].append(V_pi)
            Vc.append(V_pi)
            # 打印结果
            print(f"{ basename, j},V_pi:", V_pi)
    Vc_list.append(calculate_product(Vc))
    Vc_plot.append(basename)
    #更新索引
    sht+=1
Vpi_pf = pd.DataFrame(Vpi_dict)
Vpi_pf.to_excel(os.path.join(out_path,'种群动态变化指数 V_pi.xlsx'),index=False)
Vc_pf = pd.DataFrame()
Vc_pf['plot'] = Vc_plot
Vc_pf['群落数量动态指数']=Vc_list
Vpi_pf.to_excel(os.path.join(out_path,'群落数量动态指数Vc.xlsx'),index=False)
print(Vc_pf)