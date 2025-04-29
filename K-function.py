import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from scipy.stats import poisson, norm


# 1. Ripley's K-function 和 L(t) 变换
def ripley_k_function(points, t_max, area):
    n = len(points)
    lambda_hat = n / area  # 点密度估计
    dist_matrix = distance_matrix(points, points)

    def K(t):
        count = np.sum(dist_matrix <= t) - n  # 减去自身
        return count / (lambda_hat * n)

    def L(t):
        return np.sqrt(K(t) / np.pi)

    t_values = np.linspace(0, t_max, 100)
    L_values = [L(t) for t in t_values]

    return t_values, L_values


# 2. 蒙特卡洛模拟生成置信区间
def monte_carlo_simulation(points, t_max, area, n_simulations=99):
    n = len(points)
    t_values, L_observed = ripley_k_function(points, t_max, area)
    L_simulated = []

    for _ in range(n_simulations):
        random_points = np.random.uniform(0, np.sqrt(area), (n, 2))
        _, L_random = ripley_k_function(random_points, t_max, area)
        L_simulated.append(L_random)

    L_simulated = np.array(L_simulated)
    lower_bound = np.percentile(L_simulated, 2.5, axis=0)
    upper_bound = np.percentile(L_simulated, 97.5, axis=0)

    return t_values, L_observed, lower_bound, upper_bound


# 3. 双变量 K-function 分析
def bivariate_k_function(points1, points2, t_max, area):
    n1 = len(points1)
    n2 = len(points2)
    lambda1 = n1 / area
    lambda2 = n2 / area
    dist_matrix = distance_matrix(points1, points2)

    def K12(t):
        count = np.sum(dist_matrix <= t)
        return count / (lambda1 * lambda2 * n1 * n2)

    def L12(t):
        return np.sqrt(K12(t) / np.pi)

    t_values = np.linspace(0, t_max, 100)
    L12_values = [L12(t) for t in t_values]

    return t_values, L12_values


# 4. Neyman-Scott 点过程模型
def neyman_scott_k_function(h, sigma_sq, rho):
    return np.pi * h ** 2 + (1 / rho) * (1 - np.exp(-h ** 2 / (4 * sigma_sq)))


# 5. 生成随机数据并可视化
def main():
    # 参数设置
    area = 100  # 研究区域面积
    t_max = 5  # 最大距离
    n_points = 100  # 点的数量

    # 生成随机数据
    np.random.seed(42)
    points = np.random.uniform(0, np.sqrt(area), (n_points, 2))
    points1 = np.random.uniform(0, np.sqrt(area), (n_points // 2, 2))  # 第一类点
    points2 = np.random.uniform(0, np.sqrt(area), (n_points // 2, 2))  # 第二类点

    # Ripley's K-function 分析
    t_values, L_observed, lower_bound, upper_bound = monte_carlo_simulation(points, t_max, area)

    # 双变量 K-function 分析
    t_values_bivariate, L12_values = bivariate_k_function(points1, points2, t_max, area)

    # Neyman-Scott 点过程模型
    h_values = np.linspace(0, t_max, 100)
    K_values = [neyman_scott_k_function(h, sigma_sq=1, rho=0.1) for h in h_values]

    # 可视化结果
    plt.figure(figsize=(15, 5))

    # Ripley's K-function 结果
    plt.subplot(1, 3, 1)
    plt.plot(t_values, L_observed, label="Observed L(t)")
    plt.fill_between(t_values, lower_bound, upper_bound, color="gray", alpha=0.5, label="95% Confidence Envelope")
    plt.xlabel("Distance (t)")
    plt.ylabel("L(t)")
    plt.title("Ripley's K-function Analysis")
    plt.legend()

    # 双变量 K-function 结果
    plt.subplot(1, 3, 2)
    plt.plot(t_values_bivariate, L12_values, label="L12(t)", color="orange")
    plt.xlabel("Distance (t)")
    plt.ylabel("L12(t)")
    plt.title("Bivariate K-function Analysis")
    plt.legend()

    # Neyman-Scott 点过程模型
    plt.subplot(1, 3, 3)
    plt.plot(h_values, K_values, label="Neyman-Scott K(h)", color="green")
    plt.xlabel("Distance (h)")
    plt.ylabel("K(h)")
    plt.title("Neyman-Scott Point Process Model")
    plt.legend()

    plt.tight_layout()
    plt.show()


# 运行主函数
if __name__ == "__main__":
    main()