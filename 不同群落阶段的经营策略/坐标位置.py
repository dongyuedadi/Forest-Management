import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

file_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\path'
out_path=r'C:\Users\hys5637428\Desktop\不同阶段经营模式\out'
name_list=os.listdir(file_path)
for names in name_list:
    data=os.path.join(file_path,names)
    df=pd.read_excel(data,sheet_name='每木检尺及测高记录表')
    x_list = df[df['X轴'] > 100]
    y_list = df[df['Y轴'] > 100]
    if len(x_list) != 0 or len(y_list) != 0:
        print('错误,样地{}有异常值'.format(names))
        print(x_list, y_list)
    df['geometry']=list(zip(df['X轴'],df['Y轴']))
    df['geometry']=df['geometry'].apply(Point)
    gpd_df = gpd.GeoDataFrame(df, geometry='geometry')
    gpd_df.plot(color='green')
    plt.title('样地{}样木分布图'.format(names))
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.grid(True)
    plt.savefig(r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\样木分布图.png',dpi=500)
    plt.show()
