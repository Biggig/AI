class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables, 
    orderedListOfHiddenVariables, evidenceList):
        for ev in evidenceList:
            #Your code here
            
            popList = []
            pushList = []
            for factor in factorList:
                
                if ev in factor.varList:
                    popList.append(factor)
                    if factor.varList != [ev]:                      
                        pushList.append(factor.restrict(ev, evidenceList[ev]))
                    
            for temp in popList:
                factorList.remove(temp)
            for temp in pushList:
                factorList.append(temp)
        for var in orderedListOfHiddenVariables:
            #Your code here
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
                resf = resf.sumout(var)
                if resf.varList != []:
                    factorList.append(resf)



        #print ("RESULT:")
        res = factorList[0]
        for factor in factorList[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        return res
    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.printInf()
class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')
class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}
    def setCpt(self, cpt):
        self.cpt = cpt
    def printInf(self):
        print ("Name = " + self.name)
        print (" vars " + str(self.varList))
        for key in self.cpt:
            print ("   key: " + key + " val : " + str(self.cpt[key]))
        print ("")
    def multiply(self, factor):
        """function that multiplies with another factor"""
        #Your code here
        variables = [var for var in self.varList if var in factor.varList]
        if variables != []:
            newList = self.varList + [var for var in factor.varList if var not in variables]
            ind1 = []
            ind2 = []
            for var in variables:
                ind1.append(self.varList.index(var))
                ind2.append(factor.varList.index(var))

            new_cpt = {}
            
            for k0, v0 in self.cpt.items():
                for k1, v1 in factor.cpt.items():
                    flag = False
                    
                    for i in range(len(ind1)):
                        if k0[ind1[i]] != k1[ind2[i]]:
                            flag = True
                            break
                    if flag:
                        continue
                    
                    k2 = "".join([k1[i] for i in range(len(k1)) if i not in ind2])
                    
                    new_cpt[k0+k2] = v0 * v1
                    
        else:
            newList = self.varList + factor.varList
            new_cpt = {}
            for k0, v0 in self.cpt:
                for k1, v1 in factor.cpt:
                    new_cpt[k0 + k1] = v0 * v1

        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        return new_node
    def sumout(self, variable):
        """function that sums out a variable given a factor"""
        #Your code here
        new_var_list = [var for var in self.varList if var != variable]
        ind = self.varList.index(variable)
        new_cpt = {}
        v1 = {}
        v2 = {}
        for k, v in self.cpt.items():
            if k[ind] == '0':
                new_cpt[k[0:ind] + k[ind+1:]] = v
            elif k[ind] == '1':
                v1[k[0:ind] + k[ind+1:]] = v
            elif k[ind] == '2':
            	v2[k[0:ind] + k[ind+1:]] = v
        for k, v in new_cpt.items():
            new_cpt[k] = v + v1[k]
        if v2 != {}:
        	for k, v in new_cpt.items():
        		new_cpt[k] = v + v2[k]


        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node
    def restrict(self, variable, value):
        """function that restricts a variable to some value 
        in a given factor"""
        #Your code here
        new_var_list = [var for var in self.varList if var != variable]
        ind = self.varList.index(variable)
        new_cpt = {}
        for k, v in self.cpt.items():
            if k[ind] == str(value):
                new_cpt[k[0:ind] + k[ind+1:]] = v

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

def printRes(res, arg):
    temp = dict(res.cpt.items())
    for a in arg:
        ind = res.varList.index(a)
        for t in res.cpt:
            if t[ind] != str(arg[a]) and t in temp:
                temp.pop(t)
    
    print (list(temp.values())[0])



PatientAge = Node("PatientAge", ["PatientAge"])
CTScanResult = Node("CTScanResult", ["CTScanResult"])
MRIScanResult = Node("MRIScanResult", ["MRIScanResult"])
StrokeType = Node("StrokeType", ["StrokeType", "CTScanResult", "MRIScanResult"])
Anticoagulants = Node("Anticoagulants", ["Anticoagulants"])
Mortality = Node("Mortality", ["Mortality", "StrokeType", "Anticoagulants"])
Disability = Node("Disability", ["Disability", "StrokeType", "PatientAge"])

'''
(1)PatientAge:['0-30','31-65','65+']
(2)CTScanResult:['Ischemic Stroke','Hemmorraghic Stroke']
(3)MRIScanResult: ['Ischemic Stroke','Hemmorraghic Stroke']
(4)StrokeType: ['Ischemic Stroke','Hemmorraghic Stroke', 'Stroke Mimic']
(5)Anticoagulants: ['Used','Not used']
(6)Mortality:['True', 'False']
(7)Disability: ['Negligible', 'Moderate', 'Severe']
'''

PatientAge.setCpt({'0': 0.1, '1': 0.3, '2': 0.6})
CTScanResult.setCpt({'0': 0.7, '1': 0.3})
MRIScanResult.setCpt({'0': 0.7, '1': 0.3})
StrokeType.setCpt({'000': 0.8, '001': 0.5, '010': 0.5, '011': 0, '100': 0, '101': 0.4, '110': 0.4, '111': 0.9, '200': 0.2, '201': 0.1, '210': 0.1, '211': 0.1})
Anticoagulants.setCpt({'0': 0.5, '1': 0.5})
Mortality.setCpt({'100': 0.28, '110': 0.99, '120': 0.1, '101': 0.56, '111': 0.58, '121': 0.05, '000': 0.72, '010': 0.01, '020': 0.9, '001': 0.44, '011': 0.42, '021': 0.95})
Disability.setCpt({'000': 0.8, '010': 0.7, '020': 0.9, '001': 0.6, '011': 0.5, '021': 0.4, '002': 0.3, '012': 0.2, '022': 0.1, '100': 0.1, '110': 0.2, '120': 0.05, '101': 0.3, '111': 0.4, '121': 0.3, '102': 0.4, '112': 0.2, '122': 0.1, '200': 0.1, '210': 0.1, '220': 0.05, '201': 0.1, '211': 0.1, '221': 0.3, '202': 0.3, '212': 0.6, '222': 0.8})


#p1 = P(Mortality='True' ^ CTScanResult='Ischemic Stroke' | PatientAge='31-65' )
reslist = [PatientAge, CTScanResult, MRIScanResult, StrokeType, Anticoagulants, Mortality, Disability]
res1 = VariableElimination.inference(reslist, ['Mortality', 'CTScanResult'], ['MRIScanResult', 'StrokeType', 'Anticoagulants', 'Disability'], {'PatientAge':1})
arg1 = {'Mortality':0, 'CTScanResult':0}
print('p1 = ',end='')
printRes(res1, arg1)

#p2 = P(Disability='Moderate' and CTScanResult='Hemmorraghic Stroke' | PatientAge='65+' and  MRIScanResult='Hemmorraghic Stroke')
reslist = [PatientAge, CTScanResult, MRIScanResult, StrokeType, Anticoagulants, Mortality, Disability]
res2 = VariableElimination.inference(reslist, ['Disability', 'CTScanResult'], ['Mortality', 'StrokeType', 'Anticoagulants'], {'PatientAge':2, 'MRIScanResult':1})
arg2 = {'Disability':1, 'CTScanResult':1}
print('p2 = ',end='')
printRes(res2, arg2)

#p3 = P(StrokeType='Hemmorraghic Stroke' $|$ PatientAge='65+' $\land$ CTScanResult='Hemmorraghic Stroke' $\land$ MRIScanResult='Ischemic Stroke')
reslist = [PatientAge, CTScanResult, MRIScanResult, StrokeType, Anticoagulants, Mortality, Disability]
res3 = VariableElimination.inference(reslist, ['StrokeType'], ['Mortality', 'Disability', 'Anticoagulants'], {'PatientAge':2, 'CTScanResult':1, 'MRIScanResult':0})
arg3 = {'StrokeType':1}
print('p3 = ',end='')
printRes(res3, arg3)

#p4 = P(Anticoagulants='Used' $|$ PatientAge='31-65')
reslist = [PatientAge, CTScanResult, MRIScanResult, StrokeType, Anticoagulants, Mortality, Disability]
res4 = VariableElimination.inference(reslist, ['Anticoagulants'], ['Mortality', 'StrokeType', 'Disability', 'MRIScanResult', 'CTScanResult'], {'PatientAge':1})
arg4 = {'Anticoagulants':0}
print('p4 = ',end='')
printRes(res4, arg4)

#p5 = P(Disability='Negligible')
reslist = [PatientAge, CTScanResult, MRIScanResult, StrokeType, Anticoagulants, Mortality, Disability]
res5 = VariableElimination.inference(reslist, ['Disability'], ['Mortality', 'StrokeType', 'Anticoagulants', 'MRIScanResult', 'CTScanResult', 'PatientAge'], {})
arg5 = {'Disability':0}
print('p5 = ',end='')
printRes(res5, arg5)