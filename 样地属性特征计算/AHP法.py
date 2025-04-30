import numpy as np

def normalize(vector):
    """将向量归一化，使其元素之和为1。"""
    norm = np.sum(vector)
    return vector / norm

def calculate_weights(matrix):
    """根据成对比较矩阵计算权重。"""
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvalue_index = np.argmax(eigenvalues)
    max_eigenvector = eigenvectors[:, max_eigenvalue_index]
    weights = normalize(max_eigenvector.real)
    n = matrix.shape[0]
    max_eigenvalue = eigenvalues[max_eigenvalue_index].real
    CI = (max_eigenvalue - n) / (n - 1)
    return weights, max_eigenvalue, CI

# 构建成对比较矩阵
criteria_matrix = np.array([
    [1,4/3,2,4,1,1,4/3,1,2,4],
    [3 / 4 ,1,3 / 2,3 , 3 / 4, 3 / 4, 1, 3 / 4, 3 / 2,3],
    [2 ,2 / 3,1,2,1 / 2,1 / 2 ,2 / 3,1 / 2,1,2],
    [1 / 4,1 / 3,1 / 2,1,1 / 4,1 / 4,1 / 3,1 / 4,1 / 2,1],
    [1,4/3,2,4,1,1,4/3,1,2,4],
    [1,4/3,2,4,1,1,4/3,1,2,4],
    [3 / 4, 1, 3 / 2, 3, 3 / 4, 3 / 4, 1, 3 / 4, 3 / 2, 3],
    [1 ,4 / 3, 2 ,4, 1, 1, 4 / 3, 1 , 2 , 4,],
    [2 ,2 / 3,1,2,1 / 2,1 / 2 ,2 / 3,1 / 2,1,2],
    [1 / 4, 1 / 3, 1 / 2, 1, 1 / 4, 1 / 4, 1 / 3, 1 / 4, 1 / 2, 1]
])

# 计算准则的权重
criteria_weights, max_eigenvalue, CI = calculate_weights(criteria_matrix)

# 一致性检验
# 对于9阶矩阵，查表或使用公式计算RI值
RI = 0.8# 示例值，请根据实际情况替换
CR = CI / RI
if CR > 0.1:
    print('\n警告！！！\n一致性检验不通过！！！')
else:
    print('\n通过一致性检验\n')

# 输出权重
print('准则权重分别为：', criteria_weights)
# 选择最佳准则
best_criterion_index = np.argmax(criteria_weights)
print("最终权重:", criteria_weights)
print(f"最佳准则: 准则 {best_criterion_index + 1}")