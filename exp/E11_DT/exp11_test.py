import numpy as np
import pandas as pd

attribute = ['age', 'workclass', 'fnlwgt', 'education', 
             'education-num', 'marital-status', 'occupation', 
             'relationship', 'race', 'sex', 'capital-gain', 
             'capital-loss', 'hours-per-week', 'native-country', 
             'salary']
continuousList = ['age', 'fnlwgt', 'education-num',
                  'capital-gain', 'capital-loss', 
                  'hours-per-week']


def isContinuous(attr):
    global continuousList
    return attr in continuousList

def classify(inputTree, featLabels, testVec):  # 字典，列表， 列表
    firstStr = list(inputTree)[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = ''
    if isContinuous(firstStr):  # 连续
        for key in secondDict.keys():
            interval = key.split('-')
            min_value = float(interval[0])
            max_value = float(interval[1])
            value = float(testVec[featIndex])
            if value >= min_value and value < max_value:
                if type(secondDict[key]).__name__ == 'dict':
                    classLabel = classify(
                        secondDict[key], featLabels, testVec)
                else:
                    classLabel = secondDict[key]
    else:  # 离散
        for key in secondDict.keys():
            if testVec[featIndex] == key:
                if type(secondDict[key]).__name__ == 'dict':
                    classLabel = classify(
                        secondDict[key], featLabels, testVec)
                else:
                    classLabel = secondDict[key]
    return classLabel

def grabTree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)


myTree = grabTree('Tree.txt')
test_data = pd.read_csv('adult.test', names=attribute)
tol_test = len(test_data)
true_test = 0
for i in range(tol_test):
    testVec = test_data.iloc[i].tolist()
    truth = test_data.iloc[i]['salary']
    prediction = classify(myTree, attribute, testVec)
    prediction = prediction + '.'
    if prediction == truth:
        true_test += 1
print("The number of example for test is:")
print(tol_test)
print("The number of true prediction is:")
print(true_test)
print("The accracy of prediction is:")
print(true_test/tol_test)

