import numpy as np

f = open("MazeData.txt", 'r')
data = []
for i in range(18):
    data.append(f.readline())
datas = []
for i in data:
    for n in i:
        if n != '\n':
            datas.append(n)
f.close()

data = [[0 for i in range(36)] for j in range(18)]
for i in range(18):
    for n in range(36):
        data[i][n] = datas[36 * i + n]

start_x = 0
start_y = 0
end_x = 0
end_y = 0

for i in range(18):
    for n in range(36):
        if data[i][n] == 'S':
            start_x = i
            start_y = n
        elif data[i][n] == 'E':
            end_x = i
            end_y = n

path = []
if start_x >= end_x and start_y >= end_y:
    move = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])
elif start_x >= end_x and start_y <= end_y:
    move = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])
elif start_x <= end_x and start_y >= end_y:
    move = np.array([[1, 0], [0, -1], [-1, 0], [0, 1]])
else:
    move = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])

print(move)


def inPath(x, y, path):
    if [x, y] in path:
        return True
    else:
        return False


def overBorder(x, y):
    if x >= 0 and x <= 17 and y >= 0 and y <= 35:
        return False
    else:
        return True


mark = [[[-1, -1] for i in range(36)] for j in range(18)]
mark[start_x][start_y] = [start_x, start_y]
queue = []
queue.append([start_x, start_y])

while not len(queue):
    front = queue[0]
    del queue[0]

    if data[front[0] + move[0][0]][front[1] + move[0][1]] != '%' and not overBorder(front[0] + move[0][0], front[1] + move[0][1]):
        if(mark[front[0] + move[0][0]][front[1] + move[0][1]] == [-1, -1]):
            mark[front[0] + move[0][0]][front[1] + move[0][1]] = front
            queue.append([front[0] + move[0][0], front[1] + move[0][1]])
            if([front[0] + move[0][0], front[1] + move[0][1]] == [end_x, end_y]):
                break

    if data[front[0] + move[1][0]][front[1] + move[1][1]] != '%' and not overBorder(front[0] + move[1][0], front[1] + move[1][1]):
        if(mark[front[0] + move[1][0]][front[1] + move[1][1]] == [-1, -1]):
            mark[front[0] + move[1][0]][front[1] + move[1][1]] = front
            queue.append([front[0] + move[1][0], front[1] + move[1][1]])
            if([front[0] + move[1][0], front[1] + move[1][1]] == [end_x, end_y]):
                break

    if data[front[0] + move[2][0]][front[1] + move[2][1]] != '%' and not overBorder(front[0] + move[2][0], front[1] + move[2][1]):
        if(mark[front[0] + move[2][0]][front[1] + move[2][1]] == [-1, -1]):
            mark[front[0] + move[2][0]][front[1] + move[2][1]] = front
            queue.append([front[0] + move[2][0], front[1] + move[2][1]])
            if([front[0] + move[2][0], front[1] + move[2][1]] == [end_x, end_y]):
                break

    if data[front[0] + move[3][0]][front[1] + move[3][1]] != '%' and not overBorder(front[0] + move[3][0], front[1] + move[3][1]):
        if(mark[front[0] + move[3][0]][front[1] + move[3][1]] == [-1, -1]):
            mark[front[0] + move[3][0]][front[1] + move[3][1]] = front
            queue.append([front[0] + move[3][0], front[1] + move[3][1]])
            if([front[0] + move[3][0], front[1] + move[3][1]] == [end_x, end_y]):
                break

if not len(queue):
    path.append([end_x, end_y])
    x = end_x
    y = end_y
    while not (mark[x][y] == [start_x, start_y]):
        path.append(mark[x][y])
        x = mark[x][y][0]
        y = mark[x][y][1]
    path.append([start_x], [start_y])


print(path)
print(start_x, start_y)
print(end_x, end_y)
for i in path:
    data[i[0]][i[1]] = '*'

doc = open('out.txt', 'w')
for i in range(18):
    for n in range(36):
        print(data[i][n], end='', file=doc)
    print('', file=doc)
doc.close()
