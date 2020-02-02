import pandas as pd
import numpy as np
import random
import copy 

def compare(matrix1, matrix2):
    num_row = len(matrix1)
    num_col = len(matrix1[0])
    for i in range(num_row):
        for j in range(num_col):
            if matrix1[i,j] != matrix2[i,j]:
                return False
    return True

def findPath(room, goal, Q_matrix):
    path = []
    path.append(str(room))
    while room != goal:
        next_room = np.argmax(Q_matrix[room, :])
        path.append(str(next_room))
        room = next_room
    return "-".join(path)

R = pd.read_csv('R_matrix.txt', header=None)
gamma = 0.8
Q = [[0 for i in range(6)] for j in range(6)]
Q = np.mat(Q)
start_room = 1
goal_room = 5
all_room = [0,1,2,3,4,5]
num = len(R)
counter = 0
while 1:
    if start_room == goal_room:
        start_room = random.choice(all_room)
    Q_copy = copy.deepcopy(Q)
    possible_action = []
    for i in range(num):
        if R.iloc[start_room][i] != -1:
            possible_action.append(i) 
    
    next_room = random.choice(possible_action)
    Q_next = Q[next_room,:].max()
    Q[start_room,next_room] = R.iloc[start_room][next_room] + gamma * Q_next
    start_room = next_room
    if compare(Q, Q_copy) and counter > 1000:
        break
    counter += 1
Q_max = Q.max()
Q = Q / Q_max * 100
print("matrix Q:")
print(Q)
for i in range(num):
    print('Path for room ' + str(i) + ' :')
    print(findPath(i, goal_room, Q))

