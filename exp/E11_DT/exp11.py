from math import log
import pandas as pd
import numpy as np 


def calEnt(dataSet):  # dataSet 为列表，列表中每个元素为一列数据
    numEntries = len(dataSet)
    if numEntries == 0:
        return 0
    retDataSet = dataSet[dataSet['salary'] == ' >50K']
    retDataSet_ = dataSet[dataSet['salary'] == ' <=50K']
    Ent = 0.0
    value = len(retDataSet)
    value_ = len(retDataSet_)
    prob = float(value) / numEntries
    prob_ = float(value_) / numEntries
    if prob == 1 or prob_ == 1:
        return 0
    Ent = Ent - (prob * log(prob, 2) + prob_ * log(prob_, 2))
    return Ent


def spiltDataSet(dataSet, axis, value):  # 划分数据集，离散
    retDataSet = dataSet[dataSet[axis] == value]
    del retDataSet[axis]
    return retDataSet


def spiltDataSet_con(dataSet, axis, min_value, max_value):  # 划分数据集，连续
    retDataSet = dataSet[(dataSet[axis] >= min_value)
                         & (dataSet[axis] <= max_value)]
    del retDataSet[axis]
    return retDataSet

def isContinuous(attr):
    global continuousList
    return attr in continuousList

def calCon(dataSet, name):
    global baseEnt
    data = dataSet[name]
    data = data.sort_values()
    min_value = min(data)
    max_value = max(data) + 1
    num = len(data)
    counter = 0
    bestFeature = -1
    bestInfoGain = 0.0    
    while counter < num:
        if counter + 100 < num:
            counter += 100
            data_ = data[counter:counter+100]
            mean = data_.mean(axis=0) #求均值
            subDataSet = spiltDataSet_con(
                dataSet, name, min_value, mean)
            subDataSet_ = spiltDataSet_con(
                dataSet, name, mean, max_value)
            prob = len(subDataSet)/float(num)
            prob_ = len(subDataSet_) / float(num)
            new_Ent = prob * calEnt(subDataSet) + \
                    prob_ * calEnt(subDataSet_)
            infoGain = baseEnt - new_Ent
            if infoGain > bestInfoGain:
                bestInfoGain = infoGain
                bestFeature = mean
        else:
            data_ = data[counter:]
            mean = data_.mean(axis=0)  # 求均值
            subDataSet = spiltDataSet_con(
                dataSet, name, min_value, mean)
            subDataSet_ = spiltDataSet_con(
                dataSet, name, mean, max_value)
            prob = len(subDataSet)/float(num)
            prob_ = len(subDataSet_) / float(num)
            new_Ent = prob * calEnt(subDataSet) + \ 
                    prob_ * calEnt(subDataSet_)
            infoGain = baseEnt - new_Ent
            if infoGain > bestInfoGain:
                bestInfoGain = infoGain
                bestFeature = mean
            break
    return [min_value, bestFeature, max_value]


def chooseBestSpilt(dataSet):
    global interval
    attr = dataSet.columns.values.tolist()
    num_attr = len(attr) - 1
    baseEnt = calEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1.0
    tol_num = len(dataSet) #总行数
    for i in range(num_attr):#对数据集中的每个属性都做一次划分，计算划分后的熵
        name = attr[i]
        if isContinuous(name):#若属性为连续
            cur_interval = interval[name]#连续属性对应的区间
            interval_num = len(cur_interval)
            new_Ent = 0.0
            for x in range(interval_num - 1):#按区间划分
                subDataSet = spiltDataSet_con(
                    dataSet, name, cur_interval[x], cur_interval[x+1])
                prob = len(subDataSet)/float(tol_num)
                new_Ent += prob * calEnt(subDataSet)
            infoGain = baseEnt - new_Ent
            if infoGain > bestInfoGain:
                bestInfoGain = infoGain
                bestFeature = i
        else:#若属性为离散
            value_list = dataSet[name].drop_duplicates()  # 该属性的值域
            value_list = value_list.tolist()
            new_Ent = 0.0
            for value in value_list:
                subDataSet = spiltDataSet(dataSet, name, value)
                prob = len(subDataSet)/float (tol_num)
                new_Ent += prob * calEnt(subDataSet)
            infoGain = baseEnt - new_Ent
            if infoGain > bestInfoGain:
                bestInfoGain = infoGain
                bestFeature = i
    return attr[i] #返回最佳划分的属性

def majorCnt(classList):#传进来的参数是标签列表，功能为返回出现次数较多的标签
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    result = 0
    max_value = -1
    for key, value in classCount.items():
        if value > max_value:
            max_value = value
            result = key
    return result #返回出现次数最多的标签

def createTree(dataSet):
    classList = dataSet['salary'].tolist()
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet.columns.values.tolist()) == 1:#只剩一个属性
        return majorCnt(classList)
    bestFeat = chooseBestSpilt(dataSet)
    myTree = {bestFeat:{}}
    if isContinuous(bestFeat): #连续属性
        cur_interval = interval[bestFeat]  # 连续属性对应的区间
        interval_num = len(cur_interval)
        for x in range(interval_num - 1):
            min_value = str(cur_interval[x])
            max_value = str(cur_interval[x+1])
            interval_string = min_value + '-' + max_value
            subDataSet = spiltDataSet_con(
                dataSet, bestFeat, cur_interval[x], cur_interval[x+1])
            if len(subDataSet) != 0:
                myTree[bestFeat][interval_string] = createTree(subDataSet)
    else: #离散属性
        featValues = dataSet[bestFeat]
        uniqueVals = featValues.drop_duplicates()
        for value in uniqueVals:
            subDataSet = spiltDataSet(dataSet, bestFeat, value)
            myTree[bestFeat][value] = createTree(subDataSet)
    return myTree    

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

attribute = ['age', 'workclass', 'fnlwgt', 'education', 
             'education-num', 'marital-status', 'occupation', 
             'relationship', 'race', 'sex', 'capital-gain', 
             'capital-loss', 'hours-per-week', 'native-country', 
             'salary']
continuousList = ['age', 'fnlwgt', 'education-num',
                  'capital-gain', 'capital-loss', 
                  'hours-per-week']
dataSet = pd.read_csv('adult.data', names=attribute)
baseEnt = calEnt(dataSet)
interval = {}
for name in continuousList:
    interval[name] = calCon(dataSet, name)
myTree = createTree(dataSet)
storeTree(myTree, 'Tree.txt')
print('Finished')

