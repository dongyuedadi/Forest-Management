import pandas as pd
import numpy as np
from scipy import stats
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, PowerTransformer
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import boxcox
from sklearn.metrics import accuracy_score
# 1. 数据加载与预处理
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_excel(r"C:\Users\hys5637428\Desktop\土壤性质结果.xlsx")
df['SOM_trans'], _ = boxcox(df['SOM_mean'])
df['TK_trans'], _ = boxcox(df['TK_mean'])
df['TN_trans'], _ = boxcox(df['TN_mean'])
df['TP_trans'], _ = boxcox(df['TP_mean'])
df['BD_trans'], _ = boxcox(df['BD_mean'])
variables = ['SOM_trans', 'TK_trans', 'TN_trans', 'TP_trans', 'BD_trans']
X = df[variables]
y = df['区域']

# 2. 数据转换（应对非正态性）
pt = PowerTransformer(method='yeo-johnson')  # Yeo-Johnson转换
X_trans = pd.DataFrame(pt.fit_transform(X), columns=variables)

# 3. 正态性检验（Shapiro-Wilk）
def check_normality(X, y, alpha=0.05):
    variables = X.columns.tolist()  # 确保获取所有变量名
    regions = y.unique()
    # 初始化结果字典：变量为键，值为区域检验结果的嵌套字典
    results = {var: {} for var in variables}

    for var in variables:
        for region in regions:
            region_data = X[y == region][var].dropna()  # 提取当前区域当前变量数据
            # 样本量检查（Shapiro-Wilk要求样本量3≤n≤5000）
            if len(region_data) < 3:
                results[var][region] = {'p_value': None, 'is_normal': None, 'error': '样本量不足'}
                continue
            # 执行Shapiro-Wilk检验
            try:
                stat, p_value = stats.shapiro(region_data)
                is_normal = p_value > alpha
                results[var][region] = {'p_value': round(p_value, 4), 'is_normal': is_normal}
            except Exception as e:
                results[var][region] = {'p_value': None, 'is_normal': None, 'error': str(e)}

    # 转换为DataFrame输出
    df_list = []
    for var in variables:
        for region in regions:
            res = results[var].get(region, {})
            df_list.append({
                '变量': var,
                '区域': region,
                'p值': res.get('p_value', 'N/A'),
                '是否正态': '是' if res.get('is_normal') else '否' if 'is_normal' in res else 'N/A',
                '备注': res.get('error', '')
            })
    return pd.DataFrame(df_list)


# 调用
normality_df = check_normality(X, y)
print(normality_df)


# 4. 方差齐性检验（Levene）
def check_homogeneity(X, y, alpha=0.05):
    groups = [X[y == region][var].values for region in y.unique() for var in variables]
    _, p = stats.levene(*groups)
    return p > alpha


homo = check_homogeneity(X_trans, y)
print(f"方差齐性检验结果: {'通过' if homo else '未通过'}")


# 5. 距离判别（修正后的马氏距离）
def distance_discriminant(X_train, y_train, X_test):
    centroids = X_train.groupby(y_train).mean()
    cov_matrices = {cls: X_train[y_train == cls].cov() for cls in centroids.index}  # 各类独立协方差
    inv_covs = {cls: np.linalg.inv(cov_matrices[cls]) for cls in centroids.index}

    y_pred = []
    for _, row in X_test.iterrows():
        distances = {}
        for cls in centroids.index:
            delta = row - centroids.loc[cls]
            distance = np.sqrt(delta @ inv_covs[cls] @ delta.T)
            distances[cls] = distance
        y_pred.append(min(distances, key=distances.get))
    return np.array(y_pred)


# 6. 贝叶斯判别（协方差非齐性优化）
class BayesianDiscriminant:
    def __init__(self, prior='balanced'):
        self.priors = None
        self.means = {}
        self.covs = {}
        self.classes = None
        self.prior_method = prior

    def fit(self, X, y):
        self.classes = y.unique()
        n_samples = len(X)

        # 计算先验概率
        if self.prior_method == 'balanced':
            self.priors = {cls: 1 / len(self.classes) for cls in self.classes}
        else:
            class_counts = y.value_counts(normalize=True).to_dict()
            self.priors = class_counts

        # 计算各类独立协方差矩阵
        for cls in self.classes:
            X_cls = X[y == cls]
            self.means[cls] = X_cls.mean(axis=0).values
            self.covs[cls] = X_cls.cov()

    def predict_proba(self, X):
        posteriors = []
        for idx, row in X.iterrows():
            prob_dict = {}
            total = 0
            for cls in self.classes:
                try:
                    likelihood = stats.multivariate_normal.pdf(row, mean=self.means[cls], cov=self.covs[cls])
                except:
                    likelihood = 1e-6  # 处理奇异矩阵
                prior = self.priors[cls]
                prob_dict[cls] = prior * likelihood
                total += prob_dict[cls]
            posteriors.append({k: v / total for k, v in prob_dict.items()})
        return posteriors

    def predict(self, X):
        posteriors = self.predict_proba(X)
        return np.array([max(p, key=p.get) for p in posteriors])


# 7. Fisher判别/QDA自动选择
def adaptive_discriminant(X_train, y_train, X_test):
    if homo:
        model = LinearDiscriminantAnalysis()
    else:
        model = QuadraticDiscriminantAnalysis()  # 方差不齐时使用QDA
    model.fit(X_train, y_train)
    return model.predict(X_test)


# 8. 模型训练与评估
X_train, X_test, y_train, y_test = train_test_split(X_trans, y, test_size=0.3, random_state=42)

# 距离判别结果
y_pred_dist = distance_discriminant(X_train, y_train, X_test)
print("\n距离判别分类报告:")
print(classification_report(y_test, y_pred_dist, zero_division=0))

# 贝叶斯判别结果（调整先验概率）
bayes_model = BayesianDiscriminant(prior='balanced')
bayes_model.fit(X_train, y_train)
y_pred_bayes = bayes_model.predict(X_test)
print("\n贝叶斯判别分类报告:")
print(classification_report(y_test, y_pred_bayes, zero_division=0))

# 自适应判别结果
y_pred_adapt = adaptive_discriminant(X_train, y_train, X_test)
print("\n自适应判别分类报告:")
print(classification_report(y_test, y_pred_adapt, zero_division=0))

# 9. 混淆矩阵可视化（修正变量错误）
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
titles = ['距离判别', '贝叶斯判别', '自适应判别']
predictions = [y_pred_dist, y_pred_bayes, y_pred_adapt]

for i, (yp, title) in enumerate(zip(predictions, titles)):
    cm = confusion_matrix(y_test, yp)
    sns.heatmap(cm, annot=True, fmt='d', ax=axes[i],
                xticklabels=np.unique(y_test),
                yticklabels=np.unique(y_test),
                cmap='Blues')
    axes[i].set_xlabel('预测标签')
    axes[i].set_ylabel('真实标签')
    axes[i].set_title(title)
plt.tight_layout()
plt.show()

# 在模型训练与评估部分后添加以下代码（接原代码末尾）

# 10. 回判评估（训练集分类效果）
print("\n========== 回判评估（训练集） ==========")

# 距离判别回判
y_train_pred_dist = distance_discriminant(X_train, y_train, X_train)
print("\n距离判别训练集分类报告:")
print(classification_report(y_train, y_train_pred_dist, zero_division=0))

# 贝叶斯判别回判
y_train_pred_bayes = bayes_model.predict(X_train)
print("\n贝叶斯判别训练集分类报告:")
print(classification_report(y_train, y_train_pred_bayes, zero_division=0))

# 自适应判别回判
y_train_pred_adapt = adaptive_discriminant(X_train, y_train, X_train)
print("\n自适应判别训练集分类报告:")
print(classification_report(y_train, y_train_pred_adapt, zero_division=0))

# 对比训练集与测试集准确率
print(f"\n距离判别 训练集/测试集准确率: {accuracy_score(y_train, y_train_pred_dist):.2f}/{accuracy_score(y_test, y_pred_dist):.2f}")
print(f"贝叶斯判别 训练集/测试集准确率: {accuracy_score(y_train, y_train_pred_bayes):.2f}/{accuracy_score(y_test, y_pred_bayes):.2f}")
print(f"自适应判别 训练集/测试集准确率: {accuracy_score(y_train, y_train_pred_adapt):.2f}/{accuracy_score(y_test, y_pred_adapt):.2f}")

# 可视化回判混淆矩阵
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
titles = ['距离判别', '贝叶斯判别', '自适应判别']
train_predictions = [y_train_pred_dist, y_train_pred_bayes, y_train_pred_adapt]

for i, (yp, title) in enumerate(zip(train_predictions, titles)):
    cm = confusion_matrix(y_train, yp)
    sns.heatmap(cm, annot=True, fmt='d', ax=axes[i],
                xticklabels=np.unique(y_train),
                yticklabels=np.unique(y_train),
                cmap='Reds')
    axes[i].set_xlabel('预测标签')
    axes[i].set_ylabel('真实标签')
    axes[i].set_title(f'{title} (训练集)')
plt.tight_layout()
plt.show()