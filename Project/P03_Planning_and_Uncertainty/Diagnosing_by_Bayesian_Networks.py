import copy


def compare(list1, list2):
    num = len(list1)
    if num == len(list2):
        for i in range(num):
            if list1[i] != list2[i]:
                return False
        return True
    return False


def VE(factorList, queryVariables, orderedList, evidenceList):  # order is wrong
    #restrict
        for ev in evidenceList:
            #Your code here

            popList = []
            pushList = []
            for factor in factorList:

                if ev in factor.varList:
                    popList.append(factor)
                    if factor.varList != [ev]:  # ?
                        pushList.append(factor.restrict(ev, evidenceList[ev]))

            for temp in popList:
                factorList.remove(temp)
            for temp in pushList:
                factorList.append(temp)
        #print("after restrit:")
        #for factor in factorList:
        #        factor.printInf()

        for var in orderedList:
            if var in queryVariables:
                continue
            popList = []
            for factor in factorList:
                if var in factor.varList:
                    popList.append(factor)

            for temp in popList:
                factorList.remove(temp)

            if popList != []:
                resf = popList[0]
                for f in popList[1:]:
                    resf = resf.multiply(f)
                    #if var == 'StrokeType':
                    #    resf.printInf()
                resf = resf.sumout(var)
                if resf.varList != []:
                    factorList.append(resf)
            #print("var:")
            #print(var)
            #for factor in factorList:
            #    factor.printInf()

        res = factorList[0]
        for factor in factorList[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        return res


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}

    def setCpt(self, cpt):
        self.cpt = cpt

    def printInf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print('')

    def multiply(self, factor):  # factor is node
        """function that multiplies with another factor"""
        #Your code here
        variables = [
            var for var in self.varList if var in factor.varList]  # 共有变量

        if variables != []:
            newList = self.varList + \
                [var for var in factor.varList if var not in variables]  # 新的变量表

            #公有变量在两个因子之中的位置
            ind1 = []
            ind2 = []
            for var in variables:
                ind1.append(self.varList.index(var))
                ind2.append(factor.varList.index(var))

            new_cpt = {}

            for k0, v0 in self.cpt.items():
                for k1, v1 in factor.cpt.items():
                    flag = False
                    k0 = k0.split(", ")
                    k1 = k1.split(", ")
                    for i in range(len(ind1)):
                        if k0[ind1[i]] != k1[ind2[i]] :  # 变量值不同，不可相乘
                            flag = True
                            break
                    if flag:
                        k0 = ", ".join(k0)
                        continue
                    k0 = ", ".join(k0)
                    k2 = ", ".join([k1[i]
                                  for i in range(len(k1)) if i not in ind2])
                    new_k = k0
                    if len(k2) != 0:
                        new_k = new_k + ", " + k2
                    new_value = round(v0 * v1, 3)
                    new_cpt[new_k] = new_value

        else:
            newList = self.varList + factor.varList
            new_cpt = {}
            for k0, v0 in self.cpt.items():
                for k1, v1 in factor.cpt.items():
                    new_value = round(v0 * v1, 3)
                    new_cpt[k0 + ", " + k1] = new_value

        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        return new_node

    #finished
    def sumout(self, variable):
        # find the position of variable
        position = self.varList.index(variable)
        new_var_list = copy.deepcopy(self.varList)
        new_var_list.remove(variable)  # delete varable
        new_cpt = {}
        for key, value in self.cpt.items():  # modify the cpt
            for key_, value_ in self.cpt.items():
                new_key = key.split(', ')
                new_key_ = key_.split(', ')
                if not compare(new_key, new_key_):  # two keys are different
                    del new_key[position]
                    del new_key_[position]
                    if compare(new_key, new_key_):  # except the variable, the others are the same
                        new_key = ", ".join(new_key)
                        value = value + value_
                        if not new_cpt.__contains__(new_key):
                            new_cpt[new_key] = round(value, 3)
                        break
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

    #finished
    def restrict(self, variable, value):
        position = self.varList.index(variable)
        new_var_list = copy.deepcopy(self.varList)
        new_var_list.remove(variable)  # delete varable
        new_cpt = {}
        for key, value_ in self.cpt.items():  # modify the cpt
            new_key = key.split(', ')
            if new_key[position] == value:  # item in new cpt
                del new_key[position]
                key_ = ", ".join(new_key)
                new_cpt[key_] = round(value_, 3)  # new cpt
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node


P = Node("PatientAge", ["PatientAge"])
P.setCpt({'0-30': 0.10, '31-65': 0.30, '65+': 0.60})

C = Node("CTScanResult", ["CTScanResult"])
C.setCpt({'Ischemic Stroke': 0.7, 'Hemmorraghic Stroke': 0.3})

MR = Node("MRIScanResult", ["MRIScanResult"])
MR.setCpt({'Ischemic Stroke': 0.7, 'Hemmorraghic Stroke': 0.3})

A = Node("Anticoagulants", ["Anticoagulants"])
A.setCpt({'Used': 0.5, 'Not used': 0.5})

S = Node("StrokeType", ["CTScanResult", "MRIScanResult", "StrokeType"])
S.setCpt({'Ischemic Stroke, Ischemic Stroke, Ischemic Stroke': 0.8,
          'Ischemic Stroke, Hemmorraghic Stroke, Ischemic Stroke': 0.5,
          'Hemmorraghic Stroke, Ischemic Stroke, Ischemic Stroke': 0.5,
          'Hemmorraghic Stroke, Hemmorraghic Stroke, Ischemic Stroke': 0,

          'Ischemic Stroke, Ischemic Stroke, Hemmorraghic Stroke': 0,
          'Ischemic Stroke, Hemmorraghic Stroke, Hemmorraghic Stroke': 0.4,
          'Hemmorraghic Stroke, Ischemic Stroke, Hemmorraghic Stroke': 0.4,
          'Hemmorraghic Stroke, Hemmorraghic Stroke, Hemmorraghic Stroke': 0.9,

          'Ischemic Stroke, Ischemic Stroke, Stroke Mimic': 0.2,
          'Ischemic Stroke, Hemmorraghic Stroke, Stroke Mimic': 0.1,
          'Hemmorraghic Stroke, Ischemic Stroke, Stroke Mimic': 0.1,
          'Hemmorraghic Stroke, Hemmorraghic Stroke, Stroke Mimic': 0.1})

Mo = Node("Mortality", ["StrokeType", "Anticoagulants", "Mortality"])
Mo.setCpt({'Ischemic Stroke, Used, False': 0.28,
          'Hemmorraghic Stroke, Used, False': 0.99,
          'Stroke Mimic, Used, False': 0.1,
          'Ischemic Stroke, Not used, False': 0.56,
          'Hemmorraghic Stroke, Not used, False': 0.58,
          'Stroke Mimic, Not used, False': 0.05,

          'Ischemic Stroke, Used, True': 0.72,
          'Hemmorraghic Stroke, Used, True': 0.01,
          'Stroke Mimic, Used, True': 0.9,
          'Ischemic Stroke, Not used, True': 0.44,
          'Hemmorraghic Stroke, Not used, True': 0.4,
          'Stroke Mimic, Not used, True': 0.95})

D = Node("Disability", ["StrokeType", "PatientAge", "Disability"])
D.setCpt({'Ischemic Stroke, 0-30, Negligible': 0.80,
          'Hemmorraghic Stroke, 0-30, Negligible': 0.70,
          'Stroke Mimic, 0-30, Negligible': 0.9,

          'Ischemic Stroke, 31-65, Negligible': 0.60,
          'Hemmorraghic Stroke, 31-65, Negligible': 0.50,
          'Stroke Mimic, 31-65, Negligible': 0.4,

          'Ischemic Stroke, 65+, Negligible': 0.30,
          'Hemmorraghic Stroke, 65+, Negligible': 0.20,
          'Stroke Mimic, 65+, Negligible': 0.1,

          'Ischemic Stroke, 0-30, Moderate': 0.1,
          'Hemmorraghic Stroke, 0-30, Moderate': 0.20,
          'Stroke Mimic, 0-30, Moderate': 0.05,

          'Ischemic Stroke, 31-65, Moderate': 0.3,
          'Hemmorraghic Stroke, 31-65, Moderate': 0.4,
          'Stroke Mimic, 31-65, Moderate': 0.3,

          'Ischemic Stroke, 65+, Moderate': 0.4,
          'Hemmorraghic Stroke, 65+, Moderate': 0.20,
          'Stroke Mimic, 65+, Moderate': 0.1,

          'Ischemic Stroke, 0-30, Severe': 0.1,
          'Hemmorraghic Stroke, 0-30, Severe': 0.1,
          'Stroke Mimic, 0-30, Severe': 0.05,

          'Ischemic Stroke, 31-65, Severe': 0.1,
          'Hemmorraghic Stroke, 31-65, Severe': 0.1,
          'Stroke Mimic, 31-65, Severe': 0.3,

          'Ischemic Stroke, 65+, Severe': 0.3,
          'Hemmorraghic Stroke, 65+, Severe': 0.6,
          'Stroke Mimic, 65+, Severe': 0.8})

factorList = [P, C, MR, A, S, Mo, D]
#print("initial:")
#for factor in factorList:
#    factor.printInf()
res = VE([P, C, MR, A, S, Mo, D], ["Mortality", "CTScanResult"], ["MRIScanResult", "Anticoagulants", "StrokeType", "Disability"], {
         'PatientAge': '31-65'})
print("p1 = ")
print(res.cpt['Ischemic Stroke, True'])
print()


res = VE([P, C, MR, A, S, Mo, D], ["Disability", "CTScanResult"], ["StrokeType", "Anticoagulants", "Mortality"], {
         'MRIScanResult': 'Hemmorraghic Stroke', 'PatientAge': '65+'})
print("p2 = ")
print(res.cpt['Hemmorraghic Stroke, Moderate'])
print()

res = VE([P, C, MR, A, S, Mo, D], ["StrokeType"], ["Anticoagulants", "Disability", "Mortality"], {
         'MRIScanResult': 'Ischemic Stroke', 'PatientAge': '65+', 'CTScanResult': 'Hemmorraghic Stroke'})
print("p3 = ")
print(res.cpt['Hemmorraghic Stroke'])
print()

res = VE([P, C, MR, A, S, Mo, D], ["Anticoagulants"], ["CTScanResult", "MRIScanResult", "StrokeType", "Disability", "Mortality"], {
         'PatientAge': '31-65'})
print("p4 = ")
print(res.cpt['Used'])
print()

res = VE([P, C, MR, A, S, Mo, D], ["Disability"], ["CTScanResult",
                                                   "MRIScanResult", "StrokeType", "PatientAge", "Anticoagulants", "Mortality"], {})
print("p5 = ")
print(res.cpt['Negligible'])
print()

