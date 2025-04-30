import netCDF4 as nc
import numpy as np
import pandas as pd

# ================== 配置参数 ==================
variables = [
    {"file_path": r"C:\Users\hys5637428\Desktop\CHINA_SOIL\SOM.nc", "var_name": "SOM", "result_col": "SOM_mean"},
    {"file_path": r"C:\Users\hys5637428\Desktop\CHINA_SOIL\TK.nc", "var_name": "TK", "result_col": "TK_mean"},
    {"file_path": r"C:\Users\hys5637428\Desktop\CHINA_SOIL\TN.nc", "var_name": "TN", "result_col": "TN_mean"},
    {"file_path": r"C:\Users\hys5637428\Desktop\CHINA_SOIL\TP.nc", "var_name": "TP", "result_col": "TP_mean"},
    ## ADD BD配置项
    {"file_path": r"C:\Users\hys5637428\Desktop\CHINA_SOIL\BD.nc", "var_name": "BD", "result_col": "BD_mean"}  # 新增土壤容重
]


# ================== 主程序 ==================
def process_variable(df, file_path, var_name, result_col):
    """处理单个变量文件"""
    dataset = nc.Dataset(file_path)

    # 获取变量数据（适配不同维度顺序）[1,3](@ref)
    lon = dataset.variables['lon'][:]
    lat = dataset.variables['lat'][:]
    var_data = dataset.variables[var_name][:]

    # 新增维度检查（适用于多层数据）[2](@ref)
    dims = dataset.variables[var_name].dimensions
    print(f"{var_name}维度顺序: {dims}")

    # 初始化结果列
    results = []

    # 遍历每个坐标点
    for index, row in df.iterrows():
        target_lon = row['lon']
        target_lat = row['lat']

        # 找到最近网格点索引[3](@ref)
        lon_idx = np.abs(lon - target_lon).argmin()
        lat_idx = np.abs(lat - target_lat).argmin()

        # 新增索引范围检查（防止越界）[3](@ref)
        if lat_idx >= var_data.shape[1] or lon_idx >= var_data.shape[2]:
            raise IndexError(f"索引越界：{target_lon}°E, {target_lat}°N")

        # 提取数据（自动适配维度顺序）[1,3](@ref)
        if dims == ('depth', 'lat', 'lon'):
            values = var_data[:2, lat_idx, lon_idx]  # 前4层深度
        else:
            values = var_data[lat_idx, lon_idx, :4]  # 其他维度顺序

        # 计算均值并存储[1](@ref)
        results.append(np.nanmean(values) if np.any(values) else np.nan)
        print(f"{var_name} {target_lon}E/{target_lat}N 均值: {results[-1]:.3f}")

    # 添加结果列
    df[result_col] = results
    dataset.close()
    return df

# 输入输出文件路径
input_excel = r"C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\原始林.xlsx"
output_excel = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\原始林土壤性质结果.xlsx'
# 读取输入数据
df = pd.read_excel(input_excel)

# 批量处理所有变量
for var_info in variables:
    df = process_variable(df, ** var_info)

    # 保存结果
    df.to_excel(output_excel, index=False)
    print(f"处理完成，结果已保存到: {output_excel}")