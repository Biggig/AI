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
        for k, v in self.cpt.items():
            if k[ind] == '0':
                new_cpt[k[0:ind] + k[ind+1:]] = v
            else:
                v1[k[0:ind] + k[ind+1:]] = v
        for k, v in new_cpt.items():
            new_cpt[k] = v + v1[k]



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
# create nodes for Bayes Net
B = Node("B", ["B"])
E = Node("E", ["E"])
A = Node("A", ["A", "B","E"])
J = Node("J", ["J", "A"])
M = Node("M", ["M", "A"])

# Generate cpt for each node
B.setCpt({'0': 0.999, '1': 0.001})
E.setCpt({'0': 0.998, '1': 0.002})
A.setCpt({'111': 0.95, '011': 0.05, '110':0.94,'010':0.06,
'101':0.29,'001':0.71,'100':0.001,'000':0.999})
J.setCpt({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})
M.setCpt({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})

def printRes(res, arg):
    temp = dict(res.cpt.items())
    for a in arg:
        ind = res.varList.index(a)
        for t in res.cpt:
            if t[ind] != str(arg[a]) and t in temp:
                temp.pop(t)
    
    print (list(temp.values())[0])


print ("P(A) **********************")
res1 = VariableElimination.inference([B,E,A,J,M], ['A'], ['B', 'E', 'J','M'], {})
arg1 = {'A':1}
printRes(res1, arg1)

print ("P(J~M) **********************")
res2 = VariableElimination.inference([B,E,A,J,M], ['J','M'], ['E','A','B'], {})
arg2 = {'J':1, 'M':0}
printRes(res2, arg2)

print ("P(A | J~M) **********************")
res3 = VariableElimination.inference([B,E,A,J,M], ['A'], ['E','B'], {'J':1,'M':0})
arg3 = {'A':1}
printRes(res3, arg3)

print ("P(B | A) **********************")
res4 = VariableElimination.inference([B,E,A,J,M], ['B'], ['E','J','M'], {'A':1})
arg4 = {'B':1}
printRes(res4, arg4)

print ("P(B | J~M) **********************")
res5 = VariableElimination.inference([B,E,A,J,M], ['B'], ['E','A'], {'J':1,'M':0})
arg5 = {'B':1}
printRes(res5, arg5)

print ("P(J~M | ~B) **********************")
res6 = VariableElimination.inference([B,E,A,J,M], ['B'], ['E','A'], {'B':0})
arg6 = {'J':1, 'M':0}
printRes(res6, arg6)
