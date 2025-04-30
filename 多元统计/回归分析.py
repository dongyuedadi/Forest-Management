import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan, linear_rainbow
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.model_selection import train_test_split
from itertools import combinations
from tqdm import tqdm
from statsmodels.graphics.regressionplots import plot_ccpr
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# 设置可视化主题
sns.set_theme(style="whitegrid", palette="muted", font="SimHei")
plt.rcParams.update({
    'axes.unicode_minus': False,
    'figure.figsize': (14, 9),
    'figure.dpi': 100,
    'savefig.bbox': 'tight'
})


# 1. 增强数据预处理
def load_clean_data(path, transform_type=None):
    """数据加载与清洗，支持多种变换"""
    df = pd.read_excel(path)
    required_cols = ['BGBP', 'Elevation', 'Species Richness',
                     'Forest Age', 'Average DBH', 'Forest Density',
                     'Soil.N', 'Soil.P', 'Soil.PH', 'MAT', 'MAP']

    df = df[required_cols].dropna().replace([np.inf, -np.inf], np.nan).dropna()
    # 异常值检测
    def robust_tukey_filter(s):
        q1 = s.quantile(0.15)
        q3 = s.quantile(0.85)
        iqr = q3 - q1
        return s.between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)

    mask = df.apply(robust_tukey_filter).all(axis=1)
    return df[mask].reset_index(drop=True)


# 2. 可视化模块
class ModelVisualizer:
    """封装可视化方法的类"""

    @staticmethod
    def plot_diagnostics(model, X, y, model_name):
        """综合诊断可视化"""
        fig = plt.figure(figsize=(18, 15))
        gs = fig.add_gridspec(3, 4)

        # 残差分布图
        ax1 = fig.add_subplot(gs[0, :2])
        sns.histplot(model.resid, kde=True, ax=ax1, color='steelblue')
        ax1.set_title(f'{model_name} - 残差分布', fontsize=12)
        ax1.axvline(0, color='darkred', linestyle='--')

        # Q-Q图
        ax2 = fig.add_subplot(gs[0, 2:])
        stats.probplot(model.resid, plot=ax2)
        ax2.get_lines()[0].set_markerfacecolor('steelblue')
        ax2.get_lines()[0].set_markersize(4.0)
        ax2.set_title('正态Q-Q图', fontsize=12)

        # 残差-拟合值图
        ax3 = fig.add_subplot(gs[1, :2])
        sns.scatterplot(x=model.fittedvalues, y=model.resid, ax=ax3,
                        alpha=0.6, color='steelblue')
        ax3.axhline(0, color='darkred', linestyle='--')
        ax3.set_title('残差 vs 拟合值', fontsize=12)

        # 杠杆值-Cook距离图
        ax4 = fig.add_subplot(gs[1, 2:])
        influence = model.get_influence()
        leverage = influence.hat_matrix_diag
        cooks_d = influence.cooks_distance[0]
        sns.scatterplot(x=leverage, y=cooks_d, ax=ax4,
                        size=np.abs(model.resid), hue=np.abs(model.resid),
                        palette='flare', legend=False)
        ax4.axhline(4 / len(X), color='darkred', linestyle='--')
        ax4.set_title('杠杆值 vs Cook距离', fontsize=12)

        # VIF热力图
        ax5 = fig.add_subplot(gs[2, 0])
        vif = pd.DataFrame({
            "Variable": X.columns,
            "VIF": [variance_inflation_factor(sm.add_constant(X).values, i + 1)
                    for i in range(X.shape[1])]
        })
        sns.barplot(y='Variable', x='VIF', data=vif.sort_values('VIF'),
                    ax=ax5, palette='Blues_d')
        ax5.axvline(5, color='darkred', linestyle='--')
        ax5.set_title('方差膨胀因子(VIF)', fontsize=12)

        # 成分加残差图（前3个重要变量）
        for i, var in enumerate(X.columns[:3]):
            ax = fig.add_subplot(gs[2, i + 1])
            plot_ccpr(model, exog_idx=i + 1, ax=ax)  # 注意索引从1开始
            ax.set_title(f'成分加残差图: {var}', fontsize=10)
            ax.get_lines()[0].set_markerfacecolor('steelblue')
            ax.get_lines()[0].set_markersize(4)

        plt.tight_layout()
        return fig


# 3. 改进模型诊断流程
def enhanced_diagnostics(X, y, model_name="模型"):
    """增强版诊断流程"""
    model = sm.OLS(y, sm.add_constant(X)).fit(cov_type='HC3')

    print(f"\n=== {model_name}诊断结果 ===")
    print(f"R²: {model.rsquared:.3f} | 调整R²: {model.rsquared_adj:.3f}")
    print(f"AIC: {model.aic:.1f} | BIC: {model.bic:.1f}")

    # 统计检验
    rainbow_p = linear_rainbow(model)[1]
    bp_p = het_breuschpagan(model.resid, sm.add_constant(X))[1]
    print(f"\nRainbow检验(p={rainbow_p:.4f}) | BP检验(p={bp_p:.4f})")

    # 可视化诊断
    visualizer = ModelVisualizer()
    fig = visualizer.plot_diagnostics(model, X, y, model_name)
    plt.show()

    return model


# 4. 主流程
def main_pipeline(data_path):
    # 数据加载与预处理
    df = load_clean_data(data_path, transform_type='log')
    print(f"有效样本量: {len(df)}")
    X = df.drop('BGBP', axis=1)
    y = df['BGBP']
    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 数据标准化
    scaler = PowerTransformer()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train),
                                  columns=X.columns,
                                  index=X_train.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test),
                                 columns=X.columns,
                                 index=X_test.index)

    # 建模与诊断
    print("\n" + "=" * 40)
    print("初始模型诊断")
    print("=" * 40)
    model = enhanced_diagnostics(X_train_scaled, y_train, "初始模型")

    # 异常值处理
    influence = model.get_influence()
    cooks_d = influence.cooks_distance[0]
    threshold = 4 / len(X_train)
    outlier_mask = cooks_d > threshold

    if sum(outlier_mask) > 0:
        print(f"\n检测到异常值数量: {sum(outlier_mask)}")
        clean_X = X_train_scaled.loc[~outlier_mask]
        clean_y = y_train.loc[~outlier_mask]

        print("\n" + "=" * 40)
        print("清洗后模型诊断")
        print("=" * 40)
        clean_model = enhanced_diagnostics(clean_X, clean_y, "清洗后模型")

        # 模型比较
        X_test_const = sm.add_constant(X_test_scaled)
        metrics = pd.DataFrame({
            'Metric': ['R²', 'Adj R²', 'AIC', 'BIC'],
            '原始模型': [
                model.rsquared,
                model.rsquared_adj,
                model.aic,
                model.bic
            ],
            '清洗模型': [
                clean_model.rsquared,
                clean_model.rsquared_adj,
                clean_model.aic,
                clean_model.bic
            ]
        }).set_index('Metric')

        print("\n模型性能对比:")
        print(metrics.style.format("{:.3f}"))


if __name__ == "__main__":
    data_path = r"C:\Users\hys5637428\Desktop\文献数据库\Belowground biomass of natural and planted forests in China.xlsx"
    main_pipeline(data_path)