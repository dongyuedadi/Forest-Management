# -*- coding: utf-8 -*-
from pyproj import Transformer
import warnings

warnings.filterwarnings("ignore")


def try_transformation(epsg_code, x, y, description):
    """尝试坐标转换并打印结果"""
    try:
        transformer = Transformer.from_crs(f"EPSG:{epsg_code}", "EPSG:4326")
        lon, lat = transformer.transform(x, y)
        print(f"[{description}] 经度: {lon:.6f}°, 纬度: {lat:.6f}°")
    except Exception as e:
        print(f"转换失败 [{description}]: {str(e)}")


def main():
    # 原始坐标（用户提供）
    original_x = 846206
    original_y = 5182677

    # 可能为X/Y顺序颠倒的情况
    swapped_x = original_y
    swapped_y = original_x

    # 尝试所有可能的坐标系转换
    transformations = [
        # 高斯-克吕格 3°带（东北顺序）
        (4544, original_x, original_y, "CGCS2000 3°带44带 (X=东距, Y=北距)"),
        (4544, swapped_x, swapped_y, "CGCS2000 3°带44带 (X=北距, Y=东距 ← 可能顺序错误)"),

        # 高斯-克吕格 6°带（东北顺序）
        (4508, original_x, original_y, "CGCS2000 6°带22带 (X=东距, Y=北距)"),

        # 北京54坐标系
        (2444, original_x, original_y, "北京54 3°带44带 (X=东距, Y=北距)"),

        # 西安80坐标系
        (2344, original_x, original_y, "西安80 3°带44带 (X=东距, Y=北距)"),

        # UTM 52N（WGS84）
        (32652, original_x, original_y, "UTM 52N (WGS84, X=东距, Y=北距)"),
        (32652, swapped_x, swapped_y, "UTM 52N (X=北距, Y=东距 ← 可能顺序错误)"),
    ]

    # 执行所有转换尝试
    for epsg, x, y, desc in transformations:
        try_transformation(epsg, x, y, desc)

    # 提示用户验证
    print("\n请通过以下步骤验证结果：")
    print("1. 将输出的经纬度输入 Google 地图（例如：133.456, 46.789）")
    print("2. 检查是否位于黑龙江省虎林市东方红林场附近（约46.7°N, 133.3°E）")
    print("3. 若所有结果均偏离，可能是坐标系未覆盖或需要自定义参数")


if __name__ == "__main__":
    main()