def getVset():#初始化值域
    vset = [[[i+1 for i in range(9)] for row in range(9)] for col in range(9)]
    vset[0][3] = [7,]
    vset[0][4] = [3,]
    vset[0][5] = [8,]
    vset[0][7] = [5,]
    vset[1][2] = [7,]
    vset[1][5] = [2,]
    vset[2][5] = [9,]
    vset[3][3] = [4,]
    vset[4][2] = [1,]
    vset[4][6] = [6,]
    vset[4][7] = [4,]
    vset[5][6] = [2,]
    vset[8][8] = [6,]
    return vset

def getCon():#初始化约束条件
    con = []
    con.append([(0,0),(0,1),-1])
    con.append([(0,2),(0,3),1])
    con.append([(1,3),(1,4),-1])
    con.append([(2,0),(2,1),1])
    con.append([(1,6),(2,6),1]) 
    con.append([(1,6),(1,7),-1])
    con.append([(2,2),(2,3),-1])
    con.append([(2,3),(3,3),-1])
    con.append([(3,2),(3,3),1])
    con.append([(3,4),(3,5),1])
    con.append([(3,5),(3,6),-1])
    con.append([(3,7),(3,8),1])
    con.append([(4,0),(4,1),-1])
    con.append([(3,1),(4,1),1])
    con.append([(3,5),(4,5),1])
    con.append([(5,1),(5,2),-1])
    con.append([(4,4),(5,4),1])
    con.append([(4,8),(5,8),1])
    con.append([(5,4),(5,5),-1])
    con.append([(5,6),(5,7),1])
    con.append([(5,8),(6,8),1])
    con.append([(5,6),(6,6),1])
    con.append([(5,1),(6,1),-1])
    con.append([(6,3),(6,4),-1])
    con.append([(6,7),(7,7),1])
    con.append([(7,8),(8,8),1])
    con.append([(7,5),(8,5),-1])
    con.append([(7,2),(8,2),1])
    con.append([(7,1),(8,1),-1])
    con.append([(8,5),(8,6),-1])
    return con

def getAssigned():#初始化赋值情况
    ass = [[False for i in range(9)] for j in range(9)]
    ass[0][3] = True
    ass[0][4] = True
    ass[0][5] = True
    ass[0][7] = True
    ass[1][2] = True
    ass[1][5] = True
    ass[2][5] = True
    ass[3][3] = True
    ass[4][2] = True
    ass[4][6] = True
    ass[4][7] = True
    ass[5][6] = True
    ass[8][8] = True
    return ass

def preprocess():#调整每个变量的值域
    global conequality
    global Vset
    global assigned
    for i in range(9):
        for j in range(9):
            if not assigned[i][j]:
                x = (i,j)
                for c in conequality:
                    if x in c:
                        temp = c[0] if x == c[1] else c[1]
                        if assigned[temp[0]][temp[1]]:  # x的比较对象已被赋值，调整x的值域
                            if temp == c[0]:
                                if c[2] == 1:
                                    Vset[i][j] = list(range(1,Vset[temp[0]][temp[1]][0]))
                                else:
                                    Vset[i][j] = list(range(Vset[temp[0]][temp[1]][0]+1,10))
                            else:
                                if c[2] == 1:
                                    Vset[i][j] = list(range(Vset[temp[0]][temp[1]][0]+1,10))
                                else:
                                    Vset[i][j] = list(range(1,Vset[temp[0]][temp[1]][0]))
    row =[[7,3,8,5],[7,2],[9],[4],[1,6,4],[2],[],[],[6]]
    col = [[],[],[7,1],[7,4],[3],[8,2,9],[6,2],[5,4],[6]]
    for r in range(9):
        for c in range(9):
            if not assigned[r][c]:
                for i in row[r]:
                    if i in Vset[r][c]:
                        Vset[r][c].remove(i)
                for j in col[c]:
                    if j in Vset[r][c]:
                        Vset[r][c].remove(j)#调整总的值域，避免行列出现重复的值

                    

def getConOf(v):
    con = []
    global conequality
    global assigned
    for c in conequality:
        if (c[1] == v and not assigned[c[0][0]][c[0][1]]) or ( c[0]== v and not assigned[c[1][0]][c[1][1]]):#不等式中，v的对象未赋值
            con.append(c)
    for i in range(9):
        if i!=v[0] and not assigned[i][v[1]]:#与v同列未赋值
            con.append([v,(i,v[1]),0])
    for i in range(9):
        if i != v[1] and not assigned[v[0]][i]:#与v同行未赋值
            con.append([v,(v[0],i),0])
    return con


def pickVariable():#启发式函数，找出值域最小的变量
    global Vset
    global assigned
    minlen = 100
    index = -1
    for i in range(9):
        for j in range(9):
            if  minlen>len(Vset[i][j]) and not assigned[i][j]:
                index = (i,j)
                minlen = len(Vset[i][j])
    return index

def deepcp(vset):#深复制，总体值域
    tmp = []
    for i in range(len(vset)):
        temp = []
        for j in range(len(vset[i])):
            item = []
            for c in range(len(vset[i][j])):
                item.append(vset[i][j][c])
            temp.append(item)
        tmp.append(temp)
    return tmp


def FCCheck(c,x):
    global Vset
    curDomx = Vset[x[0]][x[1]]#x的值域
    tmp = []#x不可能的取值
    for d in curDomx:
        if x == c[0]:
            temp = c[1]
            if c[2] == 1 and d <= Vset[temp[0]][temp[1]][0]:
                tmp.append(d)
            elif c[2] == -1 and d >= Vset[temp[0]][temp[1]][0]:
                tmp.append(d)
            elif c[2] == 0 and d == Vset[temp[0]][temp[1]][0]:#？？，相等关系？
                tmp.append(d)
        else:
            temp = c[0]
            if c[2] == 1 and d >= Vset[temp[0]][temp[1]][0]:
                tmp.append(d)
            elif c[2] == -1 and d <= Vset[temp[0]][temp[1]][0]:
                tmp.append(d)
            elif c[2] == 0 and d == Vset[temp[0]][temp[1]][0]:  # ？？，相等关系？
                tmp.append(d)
    for d in tmp:
        curDomx.remove(d)
    if len(curDomx)==0:
        return False
    return True

def FC(level,flag):
    if level == 68 or len(flag):
        flag.append(True)
        return
    global Vset
    global assigned
    vindex = pickVariable()
    if vindex==-1:
        flag.append(True)
        return
    assigned[vindex[0]][vindex[1]] = True
    curDomv = Vset[vindex[0]][vindex[1]]
    for d in curDomv:
        Vset[vindex[0]][vindex[1]] = [d,]
        temp = deepcp(Vset)
        dwo = False
        con = getConOf(vindex)
        for c in con:
            x = 0
            if c[0]==vindex:
                x = c[1]
            else:
                x = c[0]
            if not FCCheck(c,x):
                dwo = True
                break
        if not dwo:
            FC(level+1,flag)
            if len(flag):
                return
        Vset = temp     #restore
    assigned[vindex[0]][vindex[1]] = False
    
    return
    
def solve():
    global Vset
    global conequality
    global assigned
    flag = []
    FC(0,flag)
    for i in range(9):
        print(Vset[i])

Vset = getVset()
assigned = getAssigned()
conequality = getCon()
preprocess()
solve()
