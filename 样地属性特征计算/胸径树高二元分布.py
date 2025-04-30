import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

dir_path=r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\path'
DFs=[]
for root, dirs, files in os.walk(dir_path):#第一个为起始路径，第二个为其实路径下的文件夹，第三个是起始路径下的文件。
    for file in files:
        file_path=os.path.join(root,file)
        df=pd.read_excel(file_path,sheet_name='检尺')
        DFs.append(df)
df=pd.concat(DFs)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(dpi=500)
ax=fig.add_subplot(121,projection='3d')
df[['树高','胸径']] = df[['树高', '胸径']].fillna(0)
x=df['胸径']
y=df['树高']
hist,xedges,yedges=np.histogram2d(x,y)
xpos,ypos=np.meshgrid(xedges[:-1]+np.diff(xedges)/2,yedges[:-1]+np.diff(yedges)/2,indexing='ij')
xpos=xpos.ravel()
ypos=ypos.ravel()
zpos=0

dx=dy=1*np.ones_like(zpos)
dz=hist.ravel()
dz1=dz/np.sum(dz)
ax.bar3d(xpos,ypos,zpos,dx,dy,dz,zsort="average",edgecolor='black',linewidth=1)
ax.tick_params(labelsize=4)
fontdict={'fontsize':5}
ax.set_xlabel('D(cm)', fontdict=fontdict)
ax.set_ylabel('H(cm)', fontdict=fontdict)
ax.set_zlabel('频数', fontdict=fontdict)
plt.xticks(range(0,60,2))
plt.yticks(range(0,40,2))

ax1=fig.add_subplot(122,projection='3d')
ax1.bar3d(xpos,ypos,zpos,dx,dy,dz,zsort="average",edgecolor='black',linewidth=1)
ax1.tick_params(labelsize=4)
ax1.set_xlabel('D(cm)', fontdict=fontdict)
ax1.set_ylabel('H(cm)', fontdict=fontdict)
ax1.set_zlabel('频率', fontdict=fontdict)
plt.xticks(range(0,60,2))
plt.yticks(range(0,40,2))

ax.view_init(45,60)
ax1.view_init(45,60)
plt.savefig(r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\胸径树高频数频率分布.jpg',dpi=300)
plt.show()