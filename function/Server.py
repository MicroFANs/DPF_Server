"""
@author:FZX
@file:Server.py
@time:2020/12/28 3:48 上午
"""
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def getcandidate():
    candidate=[8,21,2,48,101,11,30,28,18,17,15,6,3,67,7,89,29,1,98,13,64,92,66,4,1973,88,32,10,63,49,52,83,23,19,93,57,
               2285,142,40,20]
    return candidate
def getestimated():
    res=[2241,1714,1582,
         1478,
         1724,
         1393,
         1091,
         1197,
         1100,
         801,
         981,
         883,
         914,
         984,
         794,
         804,
         612,
         686,
         708,
         485,
         626,
         516,
         519,
         532,
         429,
         488,
         498,
         459,
         455,
         579,
         427,
         396,
         431,
         402,
         440,
         398,
         524,
         555,
         396,
         466]
    return res


# 欧氏距离
def distance(x1,x2):
     result=x1-x2
     return np.sqrt(np.sum(np.square(result)))

def center(data,k):
     # 分成k块初始化
     block=int(data.shape[0]/k)
     x = 0
     list=np.zeros((k,data.shape[1]))
     for i in range(k):
          list[i:]=data[x]
          x=x+block
     center_array=list
     return center_array

# laplace噪声
def laplacenoise(sensitivity,epslion,len):  #  产生单个laplace噪声
     location=0
     scale=sensitivity/epslion
     Laplacian_noise =np.random.laplace(location, scale, len)
     return Laplacian_noise # 格式为ndarray
# laplace_array
def laplacenoise_array(sensitivity,epslion,len,num):  #  产生laplace噪声数组,len是维数，num是生成的个数
     location=0
     scale=sensitivity/epslion
     list=[]
     for i in range(num):
          list .append( np.random.laplace(location, scale, len))
          Laplacian_noise=np.array(list)
     return Laplacian_noise

# kmeans iters为最大迭代次数，默认为10次迭代
def DPkmeans(data,k,iters=10,totalepslion=6,allocation=0 or 1):
     labels=[]
     sensitivity=data.shape[1]+1 # 数据维数为d，敏感度为d+1
     epslion=totalepslion
     center_array=center(data,k)
     center_array_noise=center_array #　初始点不能加噪
     print('初始点:',center_array_noise,'\n')

     clusterchanged=True
     N=0 # 记录迭代次数
     temp = np.zeros(data.shape[0])
     # 收敛条件
     minsse = 10000
     while (clusterchanged and N<iters+1):
          clusterchanged=False
          print(N)
          # 级数分配
          if allocation == 0:
               allocat = 'avg'  # 用于文件名
               epslion = totalepslion / ((N+2)*(N+1))
               print('avgepslion:', epslion)
          if allocation == 1:
               allocat = 'div2'  # 用于文件名
               epslion = epslion / 2  # 二分法分配隐私预算
               print('epslion:', epslion)
          for i in range(data.shape[0]):
               dis=[distance(data[i,:],center_array_noise[j,:]) for j in range(k)]
               index=np.argmin(dis)  #  取使dis最小时的i
               temp[i]=index
          for j in range(k):
               temp_res=data[temp==j]
               num = temp_res.shape[0]
               noise0=laplacenoise(sensitivity,epslion,1)
               num_noise=num+noise0[0]

               sum1=np.sum(temp_res[:,0]) # sum的格式为float64
               noise1=laplacenoise(sensitivity,epslion,1)
               sum1_noise=sum1+noise1[0].astype('float64')
               x1=sum1_noise/num_noise

               sum2=np.sum(temp_res[:,1])
               noise2 = laplacenoise(sensitivity, epslion, 1)
               sum2_noise = sum2 + noise2[0].astype('float64')
               x2=sum2_noise/num_noise

               center_array_noise[j,:]=[x1,x2]
               print('第'+str(N)+'次迭代第'+str(j)+'簇的中心：',center_array_noise[j])
          # 收敛条件 SSE<0.1
          sse=0
          for j in range(k):
               temp_res = data[temp == j]
               cen=center_array_noise[j]
               se=distance(temp_res,cen)
               se2=np.square(se)
               sse=sse+se2
          if abs(minsse - sse) > 1:
               clusterchanged = True
               minsse = sse
          N=N+1

          print('============================================================================')
          labels.append(temp.tolist())
     km=np.c_[data,temp] # 将原数据和标签结合

     return km,temp,sse,labels # temp是ndarray标签,km是原数据+标签