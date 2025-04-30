import os
import rasterio
import numpy as np
import pandas as pd
from rasterio.transform import rowcol


def extract_precipitation(tif_path, coordinates):
    """从WGS84坐标的TIFF文件中提取降水值"""
    results = []
    try:
        with rasterio.open(tif_path) as dataset:
            data = dataset.read(1)
            transform = dataset.transform

            for lon, lat in coordinates:
                try:
                    # 验证经纬度有效性（注意：这里参数顺序为经度、纬度）
                    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                        raise ValueError(f"经纬度 ({lon}, {lat}) 超出WGS84有效范围")

                    # 计算行列号
                    row, col = rowcol(transform, lon, lat)
                    row = int(round(row))
                    col = int(round(col))

                    # 检查行列号边界
                    if row < 0 or row >= dataset.height or col < 0 or col >= dataset.width:
                        raise IndexError(f"行列号 ({row}, {col}) 超出栅格范围")

                    # 提取数据并处理NoData
                    value = data[row, col]
                    if value == dataset.nodata or np.isnan(value):
                        results.append(np.nan)  # 统一用NaN表示无效值
                    else:
                        results.append(float(value))

                except Exception as e:
                    print(f"坐标 ({lon}, {lat}) 错误: {str(e)}")
                    results.append(np.nan)

    except Exception as e:
        print(f"处理文件 {tif_path} 时发生错误: {str(e)}")
        results = [np.nan] * len(coordinates)  # 保持数据对齐

    return results


if __name__ == "__main__":
    # ========== 配置参数 ==========
    tif_folder = r"C:\Users\hys5637428\Desktop\文献数据库\全球降水tif\wc2.1_30s_prec"
    excel_path = r'C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\转换结果.xlsx'
    output_excel =r'C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\降雨.xlsx'

    # ========== 准备坐标数据 ==========
    df_zb = pd.read_excel(excel_path)
    coordinates = list(zip(df_zb['纬度_WGS84'],df_zb['经度_WGS84']))  # 确保顺序为(经度, 纬度)

    # ========== 初始化结果DataFrame ==========
    result_df = pd.DataFrame({
        '经度': df_zb['经度_WGS84'],
        '纬度': df_zb['纬度_WGS84']
    })

    # ========== 遍历处理所有TIFF文件 ==========
    tif_files = sorted(
        [f for f in os.listdir(tif_folder) if f.endswith('.tif') and '_prec_' in f],
        key=lambda x: int(x.split('_')[-1].split('.')[0])
    )

    for filename in tif_files:
        tif_path = os.path.join(tif_folder, filename)
        month = filename.split('_')[-1].split('.')[0]  # 提取月份编号

        print(f"正在处理 {filename}...")
        precipitation = extract_precipitation(tif_path, coordinates)

        result_df[f'month_{month}'] = precipitation

    # ========== 保存结果 ==========
    result_df.to_excel(output_excel, index=False)
    print(f"数据处理完成，结果已保存至：{output_excel}")