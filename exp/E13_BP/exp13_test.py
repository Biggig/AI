import pandas as pd
import numpy as np

data = pd.read_csv('train.data', header=None)
result = data[22]
num = len(data)

#去除无用属性及结果
del data[2]
del data[22]
del data[24]
del data[25]
del data[26]
del data[27]



