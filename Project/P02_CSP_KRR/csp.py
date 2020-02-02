import time

def initial_domain(num):#return a 3-D list
    domain = [[[i + 1 for i in range(num)] for row in range(num)] for col in range(num)]
    return domain  

def initial_remarked(num):#2-D list for sign
    remarked = [[False for i in range(num)] for j in range(num)]
    return remarked

def MRU(domain,num,remark):
    x = 0
    y = 0
    mini = 10000
    for i in range(num):
        for j in range(num):
            if remark[i][j] == False:
                counter = len(domain[i][j])
                if counter < mini:
                    mini = counter
                    x = i
                    y = j
    return x, y

def finished(remark,num):
    for i in range(num):
        for j in range(num):
            if remark[i][j] == False:
                return False
    return True

def change_domain(con, domain, remark, num):
    for i in range(num):#row col constraint
        for j in range(num):
            if remark[i][j] == True:
                for k in range(num):
                    if k != i and domain[i][j][0] in domain[k][j]:
                        domain[k][j].remove(domain[i][j][0])
                    if k != j and domain[i][j][0] in domain[i][k]:
                        domain[i][k].remove(domain[i][j][0])
                    
    for i in con:
        a = i[0]
        b = i[1]
        relation = i[2]
        x_a, y_a = a
        x_b, y_b = b
        if len(domain[x_b][y_b]) == 0 or len(domain[x_a][y_a]) == 0:
            return domain
        if relation == 1: # a > b
            b_min = min(domain[x_b][y_b])
            a_max = max(domain[x_a][y_a])
            for i in domain[x_a][y_a]:
                if i <= b_min:
                    domain[x_a][y_a].remove(i)
            for i in domain[x_b][y_b]:
                if i >= a_max:
                    domain[x_b][y_b].remove(i)
        if relation == -1:# a < b
            a_min = min(domain[x_a][y_a])
            b_max = max(domain[x_b][y_b])
            for i in domain[x_a][y_a]:
                if i >= b_max:
                    domain[x_a][y_a].remove(i)
            for i in domain[x_b][y_b]:
                if i <= a_min:
                    domain[x_b][y_b].remove(i)
    return domain

def check(domain,num):
    for i in range(num):
        for j in range(num):
            if len(domain[i][j]) == 0:
                return False
    return True


def cp_domain(domain, num):  # 深复制，总体值域
    tmp = []
    for i in range(num):
        temp = []
        for j in range(num):
            item = []
            for c in range(len(domain[i][j])):
                item.append(domain[i][j][c])
            temp.append(item)
        tmp.append(temp)
    return tmp

def GAC(con, domain, remark, num):
    if not check(domain, num):
        return []
    if finished(remark, num):#if finish, return domain
        return domain
    x, y = MRU(domain, num, remark)#position to get value
    for value in domain[x][y]:
        domain_ = cp_domain(domain, num)
        domain_[x][y] = [value, ]
        remark[x][y] = True
        domain_ = change_domain(con, domain_, remark, num) #problem of copy?
        domain_ = GAC(con, domain_, remark, num)
        if len(domain_) != 0:
            return domain_
        else:
            remark[x][y] = False
    return []

start = time.clock()
domain = initial_domain(4)
remark = initial_remarked(4)
domain[0][2] = [3,]
remark[0][2] = True
con = []
con.append([(0, 1), (1, 1), -1])
con.append([(0, 2), (0, 3), 1])
con.append([(1, 2), (2, 2), -1])
con.append([(3, 0), (3, 1), 1])
con.append([(3, 1), (3, 2), 1])

domain = change_domain(con,domain,remark,4)
domain = GAC(con, domain, remark, 4)
for i in range(4):
    for j in range(4):
        print(domain[i][j][0], end = '')
    print('')
print('')



domain_1 = initial_domain(5)
remark_1 = initial_remarked(5)
domain_1[4][4] = [4,]
remark_1[4][4] = True
con_1 = []
con_1.append([(0, 0), (0, 1), 1])
con_1.append([(0, 0), (1, 0), -1])
con_1.append([(1, 1), (1, 2), -1])
con_1.append([(1, 2), (1, 3), -1])
con_1.append([(1, 3), (1, 4), -1])
con_1.append([(2, 1), (2, 2), -1])
con_1.append([(4, 0), (4, 1), 1])
   
domain_1 = change_domain(con_1, domain_1, remark_1, 5)
domain_1 = GAC(con_1, domain_1, remark_1, 5)
for i in range(5):
    for j in range(5):
        print(domain_1[i][j][0], end='')
    print('')
print('')



domain_2 = initial_domain(6)
remark_2 = initial_remarked(6)

domain_2[0][4] = [2, ]
remark_2[0][4] = True
domain_2[0][5] = [6, ]
remark_2[0][5] = True
domain_2[1][5] = [3, ]
remark_2[1][5] = True
domain_2[2][0] = [3, ]
remark_2[2][0] = True
domain_2[3][2] = [4, ]
remark_2[3][2] = True


con_2 = []
con_2.append([(0, 0), (0, 1), 1])
con_2.append([(1, 3), (1, 4), 1])
con_2.append([(1, 1), (2, 1), 1])
con_2.append([(2, 0), (2, 1), -1])
con_2.append([(1, 5), (2, 5), -1])
con_2.append([(3, 2), (3, 3), 1])
con_2.append([(3, 3), (3, 4), 1])
con_2.append([(5, 3), (5, 4), -1])
con_2.append([(5, 4), (5, 5), -1])

domain_2 = change_domain(con_2, domain_2, remark_2, 6)
domain_2 = GAC(con_2, domain_2, remark_2, 6)
for i in range(6):
    for j in range(6):
        print(domain_2[i][j][0], end='')
    print('')
print('')


domain_3 = initial_domain(7)
remark_3 = initial_remarked(7)

domain_3[0][6] = [6, ]
remark_3[0][6] = True
domain_3[3][6] = [2, ]
remark_3[3][6] = True
domain_3[5][1] = [5, ]
remark_3[5][1] = True

con_3 = []
con_3.append([(0, 0), (0, 1), -1])
con_3.append([(0, 1), (0, 2), 1])
con_3.append([(0, 5), (0, 6), 1])
con_3.append([(1, 4), (1, 5), 1])
con_3.append([(1, 2), (2, 2), 1])
con_3.append([(2, 0), (2, 1), -1])
con_3.append([(2, 1), (2, 2), -1])
con_3.append([(2, 5), (2, 6), 1])
con_3.append([(2, 4), (3, 4), -1])
con_3.append([(3, 1), (3, 2), -1])
con_3.append([(3, 4), (3, 5), 1])
con_3.append([(3, 1), (4, 1), 1])
con_3.append([(3, 3), (4, 3), -1])
con_3.append([(4, 1), (4, 2), 1])
con_3.append([(4, 2), (5, 2), 1])
con_3.append([(5, 0), (5, 1), -1])
con_3.append([(5, 4), (6, 4), -1])
con_3.append([(5, 5), (6, 5), 1])
con_3.append([(6, 5), (6, 6), 1])
domain_3 = change_domain(con_3, domain_3, remark_3, 7)
domain_3 = GAC(con_3, domain_3, remark_3, 7)
for i in range(7):
    for j in range(7):
        print(domain_3[i][j][0], end='')
    print('')
print('')

domain_4 = initial_domain(8)
remark_4 = initial_remarked(8)

domain_4[1][4] = [6, ]
remark_4[1][4] = True
domain_4[1][6] = [7, ]
remark_4[1][6] = True
domain_4[2][3] = [4, ]
remark_4[2][3] = True
domain_4[4][7] = [6, ]
remark_4[4][7] = True
domain_4[5][5] = [4, ]
remark_4[5][5] = True
domain_4[6][7] = [3, ]
remark_4[6][7] = True

con_4 = []
con_4.append([(0, 1), (0, 2), 1])
con_4.append([(0, 2), (0, 3), 1])
con_4.append([(0, 4), (0, 5), -1])
con_4.append([(0, 5), (0, 6), -1])
con_4.append([(0, 6), (0, 7), -1])

con_4.append([(1, 0), (1, 1), -1])
con_4.append([(1, 2), (2, 2), -1])
con_4.append([(1, 3), (2, 3), -1])
con_4.append([(1, 5), (2, 5), 1])
con_4.append([(1, 5), (1, 6), -1])
con_4.append([(1, 6), (2, 6), 1])
con_4.append([(2, 2), (2, 3), -1])
con_4.append([(2, 3), (3, 3), 1])
con_4.append([(3, 0), (3, 1), 1])
con_4.append([(3, 1), (3, 2), 1])
con_4.append([(3, 3), (4, 3), 1])
con_4.append([(3, 7), (4, 7), 1])
con_4.append([(4, 0), (4, 1), 1])
con_4.append([(4, 5), (5, 5), -1])
con_4.append([(4, 6), (4, 7), -1])
con_4.append([(4, 7), (5, 7), -1])
con_4.append([(5, 4), (5, 5), -1])
con_4.append([(5, 5), (5, 6), 1])
con_4.append([(5, 4), (6, 4), 1])
con_4.append([(6, 2), (6, 3), 1])
domain_4 = change_domain(con_4, domain_4, remark_4, 8)
domain_4 = GAC(con_4, domain_4, remark_4, 8)
for i in range(8):
    for j in range(8):
        print(domain_4[i][j][0], end='')
    print('')
print('')

elapsed = (time.clock() - start)
print("Time used:", elapsed)