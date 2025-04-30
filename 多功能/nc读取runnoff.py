import xarray as xr
import pandas as pd

# ==================== 配置参数 ====================
nc_path = r"C:\Users\hys5637428\Desktop\CanESM5\historical\surrunoff_VIC_historical_2000_monthly.nc"  # NetCDF 文件路径
output_excel = r"C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\runoff结果.xlsx"  # 输出结果文件路径
excel_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\转换结果.xlsx'
    # ========== 准备坐标数据 ==========
df_zb = pd.read_excel(excel_path)
coordinates = list(zip(df_zb['纬度_WGS84'],df_zb['经度_WGS84']))  # 确保顺序为(经度, 纬度)
# ==================== 打开 NetCDF 文件 ====================
# 使用 xarray 打开 NetCDF 文件
try:
    ds = xr.open_dataset(nc_path)
    print("NetCDF 文件已成功打开！")
except Exception as e:
    print(f"无法打开 NetCDF 文件: {str(e)}")
    exit(1)


# ==================== 定义提取函数 ====================
def extract_runoff(dataset, lon, lat, var_name='runoff'):
    """
    从 NetCDF 数据集中提取指定经纬度的 runoff 数据
    参数：
    dataset: xarray Dataset 对象
    lon: 经度值
    lat: 纬度值
    var_name: 要提取的变量名称
    """
    try:
        # 选择最近邻点
        point_data = dataset[var_name].sel(
            lon=lon,
            lat=lat,
            method='nearest'
        )
        return point_data
    except Exception as e:
        print(f"提取失败: {str(e)}")
        return None


# ==================== 提取数据 ====================
# 存储提取结果
results = []

# 遍历坐标列表，提取数据
for lon, lat in coordinates:
    # 提取 runoff 数据
    runoff_data = extract_runoff(ds, lon, lat)

    # 如果提取成功，添加到结果列表
    if runoff_data is not None:
        # 将数据转换为列表形式
        runoff_values = runoff_data.values.tolist()
        results.append({
            '经度': lon,
            '纬度': lat,
            'runoff': runoff_values
        })
        print(f"在经度 {lon}、纬度 {lat} 处提取到 {len(runoff_values)} 个 runoff 数据点。")
    else:
        print(f"在经度 {lon}、纬度 {lat} 处未能提取到数据。")

# ==================== 保存结果 ====================
# 将结果转换为 DataFrame
df = pd.DataFrame(results)

# 定义新列名
months = [f'month_{i}' for i in range(1, 13)]
# 将列表拆分成单独的列
df[months] = df['runoff'].apply(pd.Series)

# 保存到 Excel 文件
df.to_excel(output_excel, index=False)

# ==================== 关闭 NetCDF 文件 ====================
ds.close()
