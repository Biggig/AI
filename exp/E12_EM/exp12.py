import pandas as pd
import numpy as np
import random

def prob(x, mu, sigma):
    n = 7
    expOn = float(-0.5 * (x - mu) * (sigma.I) * ((x - mu).T))
    divBy = pow(2 * np.pi, n / 2) * pow(np.linalg.det(sigma),
                                        0.5)  # np.linalg.det 计算矩阵的行列式
    result = pow(np.e, expOn) / divBy
    return result


def calGamma(x, i, Alpha, Sigma, Mu, k):  # 计算后验概率
    top = Alpha[i] * prob(x, Mu[i], Sigma[i])
    down = 0
    for j in range(k):
        down += Alpha[j] * prob(x, Mu[j], Sigma[j])
    return top / down


def calMu(i, data, Gamma):  # 计算新的均值向量
    top = 0
    down = 0
    num = len(data)
    for j in range(num):
        x = data.iloc[j].tolist()
        x = np.mat(x)
        top += Gamma[i][j] * x
        down += Gamma[i][j]
    return top / down


def calSigma(i, data, Gamma, Mu):#计算新的协方差矩阵
    top = 0
    down = 0
    num = len(data)
    for j in range(num):
        x = data.iloc[j].tolist()
        x = np.mat(x)
        x = x.T
        top += Gamma[i][j] * (x - Mu[i]) * (x - Mu[i]).T
        down += Gamma[i][j]
    return top / down

def calAlpha(i, Gamma, num):#计算新的混合系数
    top = 0
    for j in range(num):
        top += Gamma[i][j]
    return top / num

attribute = ['Country', '2006WorldCup', '2010WorldCup', 
                '2014WorldCup', '2018WorldCup', '2007AsianCup', 
                '2011AsianCup', '2015AsianCup']
data = pd.read_csv(
    "data.txt", names=attribute, index_col='Country')
k = 3 #分类数
n = 7 #维度
#print(data.index[0])

#initialize
Alpha = [0 for i in range(3)]
Alpha[0] = 0.1
Alpha[1] = 0.4
Alpha[2] = 0.5
Mu = [0 for i in range(3)]
Mu[0] = np.mat(data.iloc[0].tolist())
Mu[1] = np.mat(data.iloc[2].tolist())
Mu[2] = np.mat(data.iloc[9].tolist())
Sigma = [0 for i in range(3)]
for i in range(3):
    Sigma[i] = np.eye(7)
    Sigma[i] = np.mat(Sigma[i]) 
num = len(data)
Gamma = [[0 for i in range(num)] for j in range(k)]
C = [[] for i in range(k)]

while True:
    counter = 0 #迭代次数
    for i in range(num):
        x = data.iloc[i].tolist()
        x = np.mat(x)
        for j in range(k):
            # 例子i由第j个高斯混合成分生成的后验概率
            Gamma[j][i] = calGamma(x, j, Alpha, Sigma, Mu, k)
    
    for i in range(k):
        Mu[i] = calMu(i, data, Gamma)
    for i in range(k):
        Sigma[i] = calSigma(i, data, Gamma, Mu)
        if np.linalg.det(Sigma[i]) == 0:
            bias = np.eye(7) * 0.1
            Sigma[i] = Sigma[i] + bias
    for i in range(k):
        Alpha[i] = calAlpha(i, Gamma, num)

    C = [[] for i in range(k)]
    for i in range(num):
        country = data.index[i]
        Gamma_4_i = []
        x = data.iloc[i].tolist()
        x = np.mat(x)
        for j in range(k):
            Gamma_ = calGamma(x, j, Alpha, Sigma, Mu, k)
            Gamma_4_i.append(Gamma_)
        max_value = max(Gamma_4_i)
        if max_value > 0.999:
            counter += 1
        index = Gamma_4_i.index(max_value)
        C[index].append(country)
    
    if counter == 16:
        break

for i in range(k):
    print("class " + str(i) + ":")
    print(C[i])

print("\nGamma:")
for i in range(num):
    country = data.index[i]
    print('  ' + country + ": ")
    for j in range(k):
        print(
            '    ' + "For class " + str(j) + ": " + str(Gamma[j][i]))

print("\nMu:")
for j in range(k):
    print(
        '  ' + "For class " + str(j) + ": " + str(Mu[j]))

print("\nCov_matrix:")
for j in range(k):
    print(
        '  ' + "For class " + str(j) + ": ")
    print(Sigma[j])




