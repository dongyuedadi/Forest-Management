import pandas as pd
output_excel1 = r"C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\evp结果.xlsx"
output_excel2 = r"C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\runoff结果.xlsx"
output_excel3=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\降雨.xlsx'
df1=pd.read_excel(output_excel1)
df2=pd.read_excel(output_excel2)
df3=pd.read_excel(output_excel3)
dfcolumns=[ 'month_1', 'month_2', 'month_3', 'month_4',
       'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10',
       'month_11', 'month_12']
df4=df3[dfcolumns]-df2[dfcolumns]-df1[dfcolumns]
df4['mean_value'] = df4[dfcolumns].mean(axis=1)
print(df4)
output_excel = r"C:\Users\hys5637428\Desktop\不同阶段经营模式\课题汇报\结果\水源涵养.xlsx"  # 输出结果文件路径
df4.to_excel(output_excel, index=False)