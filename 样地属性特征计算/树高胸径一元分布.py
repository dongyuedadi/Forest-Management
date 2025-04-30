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

#正态分布拟合
from scipy.optimize import curve_fit

def func(x,a,u,sig):
    return a*np.exp(-(x-u)**2/(2*sig**2))/(sig*math.sqrt(2*math.pi))
#拟合自定义函数
def get_curve_fit_param(x,y,opt_fun,p0):
    poptg,pcov=curve_fit(opt_fun,x,y,p0=p0,maxfev=60000)
    err=np.sqrt(np.sum((y-opt_fun(x,*poptg))**2)/len(x))
    print(err)
    print(poptg)
    print(pcov)
    return poptg

#Weibull分布拟合
def Weib(x,a,scale,shape):
    return 44*(shape/scale)*((x-a)/scale)**(shape-1)*np.exp(-((x-a)/scale)**shape)

#完整胸径、树高拟合过程
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False

bin_range=int(max(df['胸径'])+2)
x=np.array(df['胸径'])
fig=plt.figure(figsize=(10,6))
ax=plt.subplot(2, 2, 1)
fig.add_subplot(ax)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
n,bins,c=ax.hist(df['胸径'],bins=range(0,bin_range,2),edgecolor='black')
y=n
x=bins[:-1]
ztfb=get_curve_fit_param(x,y,func,p0=[5,35,6])
ztfbpre=func(x,*ztfb)
#ax.plot(x,y,'r*',ls='-')
ax.plot(x,ztfbpre,ls='-',color='orange')
#Wbfb=get_curve_fit_param(x,y,Weib,p0=[20,20,5])
#Wbfbpre=func(x,*Wbfb)
#plt.plot(x,y,'r*')
#ax.plot(x,Wbfbpre,'b+',ls='-',color='red')
plt.xticks(range(0,60,2))
plt.xlabel('径阶分布(cm)')
plt.ylabel('频数')
plt.yticks([5,10,15,20,25])

#
ax1=plt.subplot(2, 2, 2)
fig.add_subplot(ax1)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
n1,bins1,c1=ax.hist(df['树高'],bins=range(0,30,2),edgecolor='black')
y1=n1
x1=bins1[:-1]
ztfb1=get_curve_fit_param(x1,y1,func,p0=[11,23,1])
ztfbpre1=func(x1,*ztfb1)
#ax.plot(x,y,'r*',ls='-')
ax1.plot(x1,ztfbpre1,ls='-',color='orange')
#Wbfb1=get_curve_fit_param(x1,y1,Weib1,p0=[10,20,5])
#Wbfbpre1=func(x1,*Wbfb1)
#plt.plot(x,y,'r*')
#ax1.plot(x1,Wbfbpre1,'b+',ls='-',color='red')
plt.xticks(range(24,51,2))
plt.xlabel('树高分布(m)')
plt.ylabel('频数')
plt.yticks([5,10,15,20,25])

#
ax2=plt.subplot(2, 2, 3)
fig.add_subplot(ax2)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
n2,bins2,c2=ax2.hist(df['胸径'],bins=range(0,60,2),edgecolor='black')
y2=n2/np.sum(n2)
x2=bins2[:-1]
ztfb2=get_curve_fit_param(x2,y2,func,p0=[5,35,6])
ztfbpre2=func(x2,*ztfb2)
#ax.plot(x,y,'r*',ls='-')
ax2.plot(x2,ztfbpre2,ls='-',color='orange')
#Wbfb2=get_curve_fit_param(x2,y2,Weib,p0=[15,20,5])
#Wbfbpre2=func(x2,*Wbfb2)
#plt.plot(x,y,'r*')
#ax2.plot(x2,Wbfbpre2,'b+',ls='-',color='red')
plt.xticks(range(24,51,2))
plt.xlabel('径阶分布(cm)')
plt.ylabel('频率')
plt.yticks([5,10,15,20,25])

#
ax3=plt.subplot(2, 2, 4)
fig.add_subplot(ax3)
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
n3,bins3,c3=ax3.hist(df['树高'],bins=range(0,30,2),edgecolor='black')
y3=n3/np.sum(n3)
x3=bins3[:-1]
ztfb3=get_curve_fit_param(x3,y3,func,p0=[5,35,6])
ztfbpre3=func(x3,*ztfb3)
#ax.plot(x,y,'r*',ls='-')
ax3.plot(x3,ztfbpre3,ls='-',color='orange')
#Wbfb3=get_curve_fit_param(x3,y3,Weib3,p0=[10,20,5])
#Wbfbpre3=func(x3,*Wbfb3)
#plt.plot(x,y,'r*')
#ax3.plot(x3,Wbfbpre3,'b+',ls='-',color='red')
plt.xticks(range(24,51,2))
plt.xlabel('树高分布(cm)')
plt.ylabel('频率')
plt.yticks([5,10,15,20,25])

plt.savefig(r'C:\Users\hys5637428\Desktop\帽儿山蘑菇调查\out\频数频率分布图')
plt.show()


