import os
import pandas as pd
def analyze_excel_files(directory_path):

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"目录不存在: {directory_path}")

    # 获取目录中所有的Excel文件
    excel_files = [f for f in os.listdir(directory_path)
                   if f.endswith(('.xlsx', '.xls'))]

    if not excel_files:
        print(f"目录中没有找到Excel文件: {directory_path}")
        return {}

    # 存储所有文件的分析结果
    analysis_results = {}

    for file in excel_files:
        file_path = os.path.join(directory_path, file)
        try:
            # 读取Excel文件的所有sheet
            xls = pd.ExcelFile(file_path)
            sheet_results = {}

            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheet_analysis = analyze_dataframe(df)
                sheet_results[sheet_name] = sheet_analysis

            analysis_results[file] = sheet_results
        except Exception as e:
            print(f"处理文件 {file} 时出错: {str(e)}")
            analysis_results[file] = {"error": str(e)}

    return analysis_results


def analyze_dataframe(df):

    analysis = {
        "row_count": len(df),
        "columns": {}
    }

    for column in df.columns:
        col_data = df[column]
        dtype = str(col_data.dtype)
        missing_values = col_data.isna().sum()

        col_info = {
            "data_type": dtype,
            "missing_values": int(missing_values),
            "unique_values": int(col_data.nunique())
        }

        # 如果是数值型数据，添加统计信息
        if pd.api.types.is_numeric_dtype(col_data):
            col_info.update({
                "max": float(col_data.max()) if not col_data.empty else None,
                "min": float(col_data.min()) if not col_data.empty else None,
                "mean": float(col_data.mean()) if not col_data.empty else None,
                "is_numeric": True
            })
        else:
            col_info["is_numeric"] = False

        analysis["columns"][column] = col_info

    return analysis


def print_analysis_results(results):
    """
    打印分析结果

    参数:
        results (dict): analyze_excel_files函数返回的分析结果
    """
    for file_name, sheets in results.items():
        print(f"\n文件: {file_name}")
        print("=" * 50)

        if "error" in sheets:
            print(f"错误: {sheets['error']}")
            continue

        for sheet_name, analysis in sheets.items():
            print(f"\n工作表: {sheet_name}")
            print("-" * 40)
            print(f"总行数: {analysis['row_count']}")
            print("\n列分析:")

            for col_name, col_info in analysis['columns'].items():
                print(f"\n列名: {col_name}")
                print(f"  数据类型: {col_info['data_type']}")
                print(f"  缺失值数量: {col_info['missing_values']}")
                print(f"  唯一值数量: {col_info['unique_values']}")

                if col_info['is_numeric']:
                    print(f"  最大值: {col_info['max']}")
                    print(f"  最小值: {col_info['min']}")
                    print(f"  平均值: {col_info['mean']}")


def save_results_to_excel(results, output_file):
    data = []
    for file_name, sheets in results.items():
        if "error" in sheets:
            data.append({
                "文件名": file_name,
                "工作表": "N/A",
                "列名": "N/A",
                "数据类型": "N/A",
                "缺失值数量": "N/A",
                "唯一值数量": "N/A",
                "最大值": "N/A",
                "最小值": "N/A",
                "平均值": "N/A",
                "总行数": "N/A",
                "错误信息": sheets['error']
            })
            continue

        for sheet_name, analysis in sheets.items():
            for col_name, col_info in analysis['columns'].items():
                row = {
                    "文件名": file_name,
                    "工作表": sheet_name,
                    "列名": col_name,
                    "数据类型": col_info['data_type'],
                    "缺失值数量": col_info['missing_values'],
                    "唯一值数量": col_info['unique_values'],
                    "总行数": analysis['row_count']
                }

                if col_info['is_numeric']:
                    row.update({
                        "最大值": col_info['max'],
                        "最小值": col_info['min'],
                        "平均值": col_info['mean']
                    })
                else:
                    row.update({
                        "最大值": "N/A",
                        "最小值": "N/A",
                        "平均值": "N/A"
                    })

                data.append(row)

    # 创建DataFrame并保存
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"分析结果已保存到: {output_file}")


if __name__ == "__main__":
    # 用户输入目录路径
    directory_path =r"C:\Users\hys5637428\Desktop\毕业论文\2022年帽儿山21块地原始数据-采伐设计-材积表-蓄积-采伐木选择\2022年帽儿山-21块地原始数据"
    # 分析文件
    results = analyze_excel_files(directory_path)
    # 打印结果
    print_analysis_results(results)
    output_file = r"C:\Users\hys5637428\Desktop\毕业论文\分析结果.xlsx"  # 添加文件名
    save_results_to_excel(results, output_file)
