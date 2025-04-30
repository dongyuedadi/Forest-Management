import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

# 全局配置
CONFIG = {
    "GRID_SIZE": 50,  # 样地尺寸（米）
    "GRID_STEP": 1,  # 网格间隔（米）
    "MAX_POINTS": 750,  # 最大补植株数
    "OUTPUT_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\补植计算结果",
    "SAPLING_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\2022年帽儿山21块地原始数据-采伐设计-材积表-蓄积-采伐木选择\2022年帽儿山-21块地原始数据",
    "TREE_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\2022年帽儿山21块地原始数据-采伐设计-材积表-蓄积-采伐木选择\蓄积+样地设计",
    "PLOT_DIR": r"C:\Users\hys5637428\Desktop\毕业论文\样木分布图"
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
    """加载幼树数据（含胸径）"""
    path = os.path.join(CONFIG["SAPLING_DIR"], f"{plot_id}号地.xlsx")
    df = pd.read_excel(path, sheet_name='抚育更新')

    # 列名标准化和单位转换
    column_mapping = {
        '坐标点X': 'X', '坐标点Y': 'Y',
        '地径（mm）': '地径(mm)'
    }
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})

    # 转换单位
    if '地径(mm)' in df.columns:
        df['地径'] = pd.to_numeric(df['地径(mm)'], errors='coerce') * 0.1
    # 清理数据
    required_cols = ['X', 'Y', '树种','地径']
    df = df.dropna(subset=required_cols)
    return df[required_cols].copy()


def load_tree_data(plot_id):
    """加载乔木数据"""
    path = os.path.join(CONFIG["TREE_DIR"], f"{plot_id}号地.xlsx")
    df = pd.read_excel(path)

    # 列名修正
    df = df.rename(columns={',南': '南'})
    if '采伐木' in df.columns:
        df = df[df['采伐木'] != '是']

    # 强制转换数值类型
    numeric_cols = ['X', 'Y', '胸径', '树高', '东', '南', '西', '北']
    df = validate_numeric(df, numeric_cols)
    df = df.dropna(subset=['东', '南', '西', '北'])
    return df[['X', 'Y', '树种', '胸径', '树高', '东', '南', '西', '北']].copy()
# 核心计算逻辑
def calculate_replant_points(tree_df, sapling_df):
    """计算可补植点"""
    grid = generate_grid()
    valid_points = []

    for x, y in grid:
        # 排除树冠投影范围
        in_crown = False
        for _, tree in tree_df.iterrows():
            tx, ty = tree['X'], tree['Y']
            width = tree['东'] + tree['西']
            height = tree['北'] + tree['南']

            # 椭圆方程判断
            a = width / 2
            b = height / 2
            if ((x - tx) ** 2) / (a ** 2) + ((y - ty) ** 2) / (b ** 2) <= 1:
                in_crown = True
                break
        if in_crown:
            continue
        # 排除更新样木周围
        #near_sapling = False
        #for _, sapling in sapling_df.iterrows():
            #sx, sy = sapling['X'], sapling['Y']
            #radius = sapling['地径'] * 20 *0.01 # 计算保护半径（米）
            #if np.sqrt((x - sx) ** 2 + (y - sy) ** 2) <= radius:
                #near_sapling = True
                #break
        #if near_sapling:
            #continue

        valid_points.append({'X': x, 'Y': y})

    return pd.DataFrame(valid_points)
# 可视化模块
def plot_distribution(plot_id, tree_df, sapling_df, replant_df):
    """绘制分布图"""
    os.makedirs(CONFIG["PLOT_DIR"], exist_ok=True)
    plt.figure(figsize=(12, 10))
    ax = plt.gca()
    # 绘制样地边界
    ax.add_patch(Rectangle((0, 0), CONFIG["GRID_SIZE"], CONFIG["GRID_SIZE"],
                           fill=False, edgecolor='black', linewidth=1.5))
    # 绘制乔木冠幅
    for _, tree in tree_df.iterrows():
        tx, ty = tree['X'], tree['Y']
        width = tree['东'] + tree['西']
        height = tree['北'] + tree['南']
        ax.add_patch(Ellipse((tx, ty), width, height,
                             fill=True, alpha=0.8, facecolor='green',
                             edgecolor='darkgreen', linewidth=0.5))
        ax.plot(tx, ty, 'o', color='darkgreen', markersize=4)
    # 绘制更新样木
    if not sapling_df.empty:
        ax.scatter(sapling_df['X'], sapling_df['Y'],
                   color='red', s=20, label='更新样木',
                   alpha=0.8, edgecolors='k', linewidths=0.5)
    # 绘制补植点
    if not replant_df.empty:
        ax.scatter(replant_df['X'], replant_df['Y'],
                   color='gold', s=20, label='补植点',
                   alpha=0.8, edgecolors='k', linewidths=0.5)
    # 设置图形属性
    ax.set(xlim=(0, CONFIG["GRID_SIZE"]), ylim=(0, CONFIG["GRID_SIZE"]),
           xlabel='X坐标 (米)', ylabel='Y坐标 (米)',
           title=f'{plot_id}号地林木分布图')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper right')
    # 保存图形
    plot_path = os.path.join(CONFIG["PLOT_DIR"], f"{plot_id}号地分布图.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"分布图已保存至: {plot_path}")
# 主处理流程
def process_plot(plot_id):
    """处理单个样地"""
    print(f"正在处理样地 {plot_id}号...")
    # 加载数据
    try:
        tree_df = load_tree_data(plot_id)
        sapling_df = load_sapling_data(plot_id)
    except FileNotFoundError:
        print(f"警告：{plot_id}号地数据文件缺失")
        return 0, 0, 0
    # 计算补植点
    replant_df = calculate_replant_points(tree_df, sapling_df)
    #final_df = replant_df.head(CONFIG["MAX_POINTS"])
    final_df = replant_df
    # 保存结果
    output_path = os.path.join(CONFIG["OUTPUT_DIR"], f"{plot_id}号地补植点.xlsx")
    final_df.to_excel(output_path, index=False)
    # 绘制分布图
    #plot_distribution(plot_id, tree_df, sapling_df, final_df)
    # 统计信息
    count = len(final_df)
    tree_count = len(tree_df)
    total_count = tree_count + len(sapling_df)
    return count, tree_count, total_count


def main():
    """主程序"""
    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    os.makedirs(CONFIG["PLOT_DIR"], exist_ok=True)

    # 处理所有样地
    summary = []
    for plot_id in range(21):
        count, tree_count, total = process_plot(plot_id)
        summary.append({
            "样地编号": f"{plot_id}号地",
            "补植株数": count,
            "乔木株数": tree_count,
            "总株数": total
        })

    # 生成汇总报告
    summary_df = pd.DataFrame(summary)

    # 添加总计行
    total_row = {
        "样地编号": "总计",
        "补植株数": summary_df["补植株数"].sum(),
        "乔木株数": summary_df["乔木株数"].sum(),
        "总株数": summary_df["总株数"].sum()
    }
    summary_df = pd.concat([summary_df, pd.DataFrame([total_row])], ignore_index=True)

    # 保存汇总结果
    summary_path = os.path.join(CONFIG["OUTPUT_DIR"], "样地补植汇总.xlsx")
    summary_df.to_excel(summary_path, index=False)
    print(f"处理完成，汇总结果保存至: {summary_path}")


if __name__ == "__main__":
    main()