import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#MAT（Mean Annual Temperature，年均温）
#MAP(Mean Annual Precipitation，年均降水量）
#Annual average sunshine duration（年均日照时数)
#Average annual evaporation（年均蒸发量)
#LA（Leaf Area，叶面积）
#SLA（Specific Leaf Area，比叶面积）
#（Leaf Dry Matter Content，叶片干物质含量）
#BGBP（Below-Ground Biomass Proportion，地下生物量比例）
def robust_factor_analysis(file_path):
    try:
        # 1. 数据加载与预处理
        df = pd.read_excel(file_path)

        # 选择数值型变量
        variables = ['Longitude', 'Latitude', 'Elevation', 'Species Richness', 'Forest Age',
            'Average DBH', 'Forest Density',
            'Soil.N', 'Soil.P', 'Soil.PH', 'MAT', 'MAP',
            'Annual average sunshine duration', 'Average annual evaporation',
            'LA', 'SLA', 'LDMC', 'LN', 'LP', 'BGBP'
        ]
        data = df[variables].dropna()
        print(f"有效样本量: {len(data)}")

        # 标准化数据
        scaler = StandardScaler()
        data_std = scaler.fit_transform(data)

        # 2. KMO检验
        kmo_all, kmo_model = calculate_kmo(data_std)
        print(f"\nKMO检验值: {kmo_model:.3f}")
        if kmo_model < 0.6:
            print("警告：KMO值低于0.6，因子分析结果可能不可靠")
        else:
            print("KMO检验通过，适合进行因子分析")

        # 3. 确定因子数量
        fa = FactorAnalyzer(rotation=None, impute="drop")
        fa.fit(data_std)

        # 计算特征值和方差贡献
        ev, v = fa.get_eigenvalues()
        cumulative_variance = np.cumsum(fa.get_factor_variance()[1])

        # 绘制碎石图
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(range(1, len(ev) + 1), ev, 'bo-')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.title('碎石图')
        plt.xlabel('因子数量')
        plt.ylabel('特征值')

        plt.subplot(1, 2, 2)
        plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, 'rs-')
        plt.axhline(y=0.85, color='g', linestyle='--')
        plt.title('累计方差解释率')
        plt.xlabel('因子数量')
        plt.ylabel('累计方差')
        plt.tight_layout()
        plt.show()

        # 更健壮的因子数量确定方法
        if len(np.where(cumulative_variance >= 0.85)[0]) > 0:
            n_factors = np.where(cumulative_variance >= 0.85)[0][0] + 1
            print(f"\n根据85%方差标准，提取{n_factors}个因子")
        else:
            # 使用Kaiser标准（特征值>1）
            n_factors = sum(ev > 1)
            if n_factors == 0:
                n_factors = 3  # 保底选择3个因子
                print("\n警告：无法达到85%方差且无特征值>1的因子，强制使用3个因子")
            else:
                print(f"\n警告：无法达到85%方差，改用特征值>1标准，提取{n_factors}个因子")
            print(f"当前最大累计方差: {max(cumulative_variance):.1%}")

        # 4. 因子旋转分析
        def perform_rotation(rotation_method):
            fa = FactorAnalyzer(n_factors=n_factors, rotation=rotation_method)
            fa.fit(data_std)

            # 结果整理
            loadings = pd.DataFrame(
                fa.loadings_,
                index=variables,
                columns=[f'因子{i + 1}' for i in range(n_factors)]
            )

            variance = pd.DataFrame(
                fa.get_factor_variance(),
                index=['特征根', '方差解释率', '累计方差'],
                columns=[f'因子{i + 1}' for i in range(n_factors)]
            )

            return loadings, variance

        print("\n=== 正交旋转(varimax)结果 ===")
        orth_loadings, orth_variance = perform_rotation('varimax')
        print("\n因子载荷矩阵:")
        print(orth_loadings.round(2))
        print("\n方差解释:")
        print(orth_variance.round(3))

        print("\n=== 斜交旋转(promax)结果 ===")
        oblq_loadings, oblq_variance = perform_rotation('promax')
        print("\n因子载荷矩阵:")
        print(oblq_loadings.round(2))
        print("\n方差解释:")
        print(oblq_variance.round(3))

    except FileNotFoundError:
        print("错误：文件未找到，请检查路径是否正确")
    except KeyError as e:
        print(f"错误：数据中缺少必要的列 - {str(e)}")
    except Exception as e:
        print(f"分析过程中出错: {str(e)}")


# 执行分析
file_path = r"C:\Users\hys5637428\Desktop\文献数据库\Belowground biomass of natural and planted forests in China.xlsx"
robust_factor_analysis(file_path)