import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

# 全局配置
CONFIG = {
    "GRID_SIZE": 50,  # 样地尺寸（米）
    "GRID_STEP": 1,  # 网格间隔（米）
    "MIN_HEIGHT": 0.5,  # 红松幼苗高度（米）
    "RS_THRESHOLD": 0.6,  # RS筛选阈值
    "MAX_POINTS": 750,  # 最大补植株数
    "OUTPUT_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\补植计算结果",
    "SAPLING_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\2022年帽儿山21块地原始数据-采伐设计-材积表-蓄积-采伐木选择\2022年帽儿山-21块地原始数据",
    "TREE_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\2022年帽儿山21块地原始数据-采伐设计-材积表-蓄积-采伐木选择\蓄积+样地设计",
    "PLOT_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\样木分布图"  # 新增：分布图保存路径
}


# 工具函数
def validate_numeric(df, columns):
    """强制转换指定列为数值类型"""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def generate_grid():
    """生成样地网格坐标"""
    return [(x, y) for x in np.arange(0.5, CONFIG["GRID_SIZE"], CONFIG["GRID_STEP"])
            for y in np.arange(0.5, CONFIG["GRID_SIZE"], CONFIG["GRID_STEP"])]


# 数据加载模块
def load_sapling_data(plot_id):
    """加载幼树数据（自动补全缺失列）"""
    path = os.path.join(CONFIG["SAPLING_DIR"], f"{plot_id}号地.xlsx")
    df = pd.read_excel(path, sheet_name='抚育更新')
    # 列名标准化和单位转换
    column_mapping = {
        '坐标点X': 'X', '坐标点Y': 'Y', '树高（cm）': '树高(cm)'
    }
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    if '树高(cm)' in df.columns:
        df['树高'] = pd.to_numeric(df['树高(cm)'], errors='coerce') * 0.01
    df = df.dropna(subset=['X', 'Y', '树种', '树高'])
    return df[['X', 'Y', '树种', '树高']].copy()


def load_tree_data(plot_id):
    """加载乔木数据（严格校验数据类型）"""
    path = os.path.join(CONFIG["TREE_DIR"], f"{plot_id}号地.xlsx")
    df = pd.read_excel(path)
    # 列名修正和数据清洗
    df = df.rename(columns={',南': '南'})
    if '采伐木' in df.columns:
        df = df[df['采伐木'] != '是']
    # 强制转换数值类型
    numeric_cols = ['X', 'Y', '胸径', '树高', '东', '南', '西', '北']
    df = validate_numeric(df, numeric_cols)
    df = df.dropna(subset=['东', '南', '西', '北'])
    return df[['X', 'Y', '树种', '胸径', '树高', '东', '南', '西', '北']].copy()


# 计算模块
def calculate_crowding(tree_df):
    """第一阶段：仅用乔木数据计算密集度"""
    grid = generate_grid()
    crowding_dict = {}
    for x, y in grid:
        # 计算最近邻
        points = tree_df[['X', 'Y']].astype(float).values
        distances = np.sqrt((points[:, 0] - x)  ** 2 + (points[:, 1] - y)  ** 2)
        nearest = np.argsort(distances)[:4]
        # 密集度计算
        crown_avg = tree_df.iloc[nearest][['东', '南', '西', '北']].mean(axis=1).values
        dist_values = distances[nearest]
        crowd_score = sum(c * 2 > d for c, d in zip(crown_avg[1:], dist_values[1:])) / 4
        crowding_dict[(x, y)] = crowd_score

    return crowding_dict


def calculate_indicators(combined_df, crowding_dict):
    """第二阶段：计算混交度和成层性"""
    results = []
    for (x, y), crowd in crowding_dict.items():
        points = combined_df[['X', 'Y']].astype(float).values
        distances = np.sqrt((points[:, 0] - x)  ** 2 + (points[:, 1] - y)  ** 2)
        nearest = np.argsort(distances)[:4]
        neighbors = combined_df.iloc[nearest]
        # 混交度计算
        species = neighbors['树种'].tolist()
        mix_value = sum(1 for s in species[1:] if s != species[0]) / 4
        # 成层性计算
        heights = neighbors['树高'].values
        layer_score = sum(abs(h - CONFIG["MIN_HEIGHT"]) >= 5 for h in heights[1:]) / 4
        # RS指数计算
        rs = np.sqrt((layer_score + 0.1) * (crowd + 0.1))
        results.append({
            'X': x, 'Y': y,
            '密集度': crowd,
            '混交度': mix_value,
            '成层性': layer_score,
            'RS': rs
        })
    return pd.DataFrame(results)


def plot_tree_distribution(plot_id, tree_df, sapling_df,final_df):
    """绘制样木分布图"""
    os.makedirs(CONFIG["PLOT_DIR"], exist_ok=True)
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    # 绘制样地边界
    ax.add_patch(Rectangle((0, 0), CONFIG["GRID_SIZE"], CONFIG["GRID_SIZE"],
                           fill=False, edgecolor='black', linewidth=1))
    # 绘制乔木冠幅投影（矩形表示）
    for _, row in tree_df.iterrows():
        x, y = row['X'], row['Y']
        east, south, west, north = row['东'], row['南'], row['西'], row['北']
        width = east + west
        height = north + south
        # 创建椭圆补丁
        ax.add_patch(Ellipse((x, y), width, height,  # 中心坐标(x,y)，宽度，高度
                             fill=True, alpha=0.3, facecolor='green', edgecolor='darkgreen'))
        plt.plot(x, y, 'o', color='darkgreen', markersize=3)  # 乔木中心点

    # 绘制更新数据（样木分布点）
    if not sapling_df.empty:
        plt.scatter(sapling_df['X'], sapling_df['Y'],
                    color='red', s=10, label='更新样木', alpha=0.7)
    # 绘制补植数据（样木分布点）
    if not final_df.empty:
        plt.scatter(final_df['X'], final_df['Y'],
                    color='#FFD700', s=10, label='补植', alpha=0.7)
    # 设置图形属性
    plt.xlim(0, CONFIG["GRID_SIZE"])
    plt.ylim(0, CONFIG["GRID_SIZE"])
    plt.xlabel('X坐标 (米)')
    plt.ylabel('Y坐标 (米)')
    plt.title(f'{plot_id}号地分布图')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    # 保存图形
    plot_path = os.path.join(CONFIG["PLOT_DIR"], f"{plot_id}号地分布图.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"样木分布图已保存至: {plot_path}")


# 主处理流程
def process_plot(plot_id):
    """处理单个样地"""
    print(f"正在处理样地 {plot_id}号...")
    # 第一阶段：乔木数据计算密集度
    tree_df = load_tree_data(plot_id)
    crowding_dict = calculate_crowding(tree_df) if not tree_df.empty else {}

    # 第二阶段：合并数据计算其他指标
    sapling_df = load_sapling_data(plot_id)
    # 选择需要的列后再合并
    combined_df = pd.concat(
        [tree_df[['X', 'Y', '树种', '树高']],
         sapling_df[['X', 'Y', '树种', '树高']]],
        ignore_index=True
    )

    # 执行计算
    results = calculate_indicators(combined_df, crowding_dict)
    filtered = results[results['RS'] < CONFIG["RS_THRESHOLD"]]
    sorted_df = filtered.sort_values(by='RS', ascending=True)
    final_df = sorted_df
    # 绘制样木分布图
    plot_tree_distribution(plot_id, tree_df, sapling_df,final_df)
    # 保存结果
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], f"{plot_id}号地补植点.xlsx")
    final_df.to_excel(output_path, index=False)

    # 计算统计量
    count = len(final_df)
    avg_rs = round(final_df['RS'].mean(), 2) if count > 0 else 0.0
    # 乔木株树和总株数
    tree_num = len(tree_df)
    total_num = len(combined_df)
    return count, avg_rs, tree_num, total_num


def main():
    """主程序"""
    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    os.makedirs(CONFIG["PLOT_DIR"], exist_ok=True)

    # 处理所有样地
    summary = []
    for plot_id in range(21):
        count, avg_rs, tree_num, total_num = process_plot(plot_id)
        summary.append({
            "样地编号": f"{plot_id}号地",
            "补植株数": count,
            "平均RS": avg_rs,
            "乔木株树": tree_num,
            "总株数": total_num
        })

    # 生成汇总报告
    summary_df = pd.DataFrame(summary)

    # 添加总计行
    total_row = {
        "样地编号": "总计",
        "补植株数": summary_df["补植株数"].sum(),
        "平均RS": round(summary_df["平均RS"].mean(), 2)
    }
    summary_df = pd.concat([summary_df, pd.DataFrame([total_row])], ignore_index=True)

    # 保存结果
    summary_path = os.path.join(CONFIG["OUTPUT_DIR"], "样地补植汇总.xlsx")
    summary_df.to_excel(summary_path, index=False)
    print(f"处理完成，汇总结果保存至: {summary_path}")


if __name__ == "__main__":
    main()