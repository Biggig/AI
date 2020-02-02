#include<iostream>
#include<stack>
#include<list>
#include<stdlib.h>
#include<time.h>
using namespace std;

class node
{
public:
    node()
    {
        for(int i = 0;i < 4;i++)
            for(int n = 0;n < 4;n++)
                    state[i][n] = i * 4 + n + 1;
        state[3][3] = 0;
        g = 0;
        movement = 0;
    }
    node& operator=(const node& m)//重载赋值运算符
    {
        for(int i = 0;i < 4;i++)
            for(int n = 0;n < 4;n++)
                    this->state[i][n] = m.state[i][n];
        this->g = m.g;
        this->movement = m.movement;
        return *this;
    }
    bool operator == (const node& m)
    {
        bool result = true;
        for(int i = 0;i < 4;i++)
            for(int n = 0;n < 4;n++)
                    if(this->state[i][n] != m.state[i][n])
                        result = false;
        return result;
    }
    int state[4][4];//数字位置
    int g; //cost
    int movement;//移动的块
};

int h(const node it) //启发式函数
{
    int num = 0;
    for(int i = 1;i < 16;i++)
    {
        int x = (i - 1) / 4;
        int y = (i + 3) % 4;
        for(int n = 0;n < 4;n++)
        {
            for(int m = 0;m < 4;m++)
            {
                if(it.state[n][m] == i)
                {
                    num = num + abs(n - x) + abs(m - y);
                }
            }
        }
    }
    return num;
}

class cmp
{
public:
    bool operator()(const node n1, const node n2)
    {
        return h(n1) < h(n2);
    }
};

bool is_goal(node m)
{
    bool result = true;
    for(int i = 0;i < 4;i++)
        for(int n = 0;n < 4;n++)
            if(m.state[i][n] != i*4 + n + 1 && i*4 + n + 1 != 16)
                    result = false;
    return  result;
}

bool in_Path(node &n, list<node> &path)
{
    bool result = false;
    list<node>::iterator i;
    for(i = path.begin(); i != path.end(); i++)
        if(n == *i)
         {
             result = true;
             break;
         }
    return result;
}

list<node> successor(node &n)
{
    list<node> result;
    int i, m;
    int xx, yy;
    for(i = 0;i < 4;i++)//找出空格
    {
        for(m = 0;m < 4;m++)
            if(n.state[i][m] == 0)
            {
                xx = i;
                yy = m;
            }
    }
    if(xx + 1 < 4)//将后继都加进列表中
    {
        node x = n;
        x.movement = x.state[xx+1][yy];
        x.state[xx][yy] = x.state[xx+1][yy];
        x.state[xx+1][yy] = 0;
        x.g++;
        result.push_back(x);
    }
    if(xx - 1 >= 0)
    {
        node x = n;
        x.movement = x.state[xx-1][yy];
        x.state[xx][yy] = x.state[xx-1][yy];
        x.state[xx-1][yy] = 0;
        x.g++;
        result.push_back(x);
    }
    if(yy + 1 < 4)
    {
        node x = n;
        x.movement = x.state[xx][yy + 1];
        x.state[xx][yy] = x.state[xx][yy + 1];
        x.state[xx][yy + 1] = 0;
        x.g++;
        result.push_back(x);
    }
    if(yy - 1 >= 0)
    {
        node x = n;
        x.movement = x.state[xx][yy-1];
        x.state[xx][yy] = x.state[xx][yy-1];
        x.state[xx][yy-1] = 0;
        x.g++;
        result.push_back(x);
    }
    result.sort(cmp());//排序
    return result;
}

int search_path(list<node> &path, int g, int bound)
{
    node n = path.back();
    int f = g + h(n);
    if(f > bound)
        return f;
    if(is_goal(n))
        return -1;//found
    int mini = -2; //无穷
    list<node> successors = successor(n);
    list<node>::iterator it;
    for(it = successors.begin(); it != successors.end(); it++)
    {
        if(!in_Path(*it, path))
        {
            path.push_back(*it);
            //cout << (*it).movement << endl;
            int t;
            t = search_path(path, g + 1, bound);
            if(t == -1)//found
                return -1;
            if(t < mini || mini < 0)
                mini = t;
            path.pop_back();
        }
    }
    return mini;
}

int main()
{
    time_t start, stop;
    start = time(NULL);
    node root;

    root.state[0][0] = 5;
    root.state[0][1] = 1;
    root.state[0][2] = 7;
    root.state[0][3] = 3;

    root.state[1][0] = 2;
    root.state[1][1] = 0;
    root.state[1][2] = 6;
    root.state[1][3] = 4;

    root.state[2][0] = 9;
    root.state[2][1] = 10;
    root.state[2][2] = 11;
    root.state[2][3] = 8;

    root.state[3][0] = 13;
    root.state[3][1] = 14;
    root.state[3][2] = 15;
    root.state[3][3] = 12;

    for(int i = 0; i < 4; i++ )
    {
        for(int n = 0; n < 4; n++)
            cout << root.state[i][n] << ' ';
        cout << endl;
    }

    int bound = h(root);
    list<node> path;
    path.push_back(root);
    int t;
    while(true)
    {
        t = search_path(path, 0, bound);
        if(t == -1)
        {
            break;
        }
        if(t == -2)
        {
            cout << "not found" << endl;
            break;
        }
        bound = t;
    }
    stop = time(NULL);
    list<node>::iterator it;
    cout << "LowerBound " << bound << " moves" << endl;
    cout << "A optimal solution " << path.size() - 1 << " moves" << endl;
    cout << "Used time " << stop - start << " sec" << endl;
    for(it = path.begin();it != path.end(); it++)
        if((*it).movement != 0)
            cout << (*it).movement << ' ';
    cout << endl;
    return 0;
}
