#include <iostream>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

int const MAX = 65534;

int deepth = 10; //最大搜索深度  （可调节）

//基本元素   棋子，颜色，数字变量

enum Option
{
    WHITE = -1,
    SPACE,
    BLACK //是否能落子  //黑子
};

struct Do
{
    pair<int, int> pos;
    double score;
    bool equal;
};

struct WinNum
{
    enum Option color;
    int stable; // 此次落子赢棋个数
};

//主要功能    棋盘及关于棋子的所有操作，功能
struct Othello
{

    WinNum cell[6][6]; //定义棋盘中有6*6个格子
    int whiteNum;      //白棋数目
    int blackNum;      //黑棋数

    void Create(Othello *board);                                //初始化棋盘
    void Copy(Othello *boardDest, const Othello *boardSource);  //复制棋盘
    void Show(Othello *board);                                  //显示棋盘
    int Rule(Othello *board, enum Option player);               //判断落子是否符合规则
    int Action(Othello *board, Do *choice, enum Option player); //落子,并修改棋盘
    void Stable(Othello *board);                                //计算赢棋个数
    double Judge(Othello *board);                               //计算本次落子分数
};                                                              //主要功能

double max(double A, Do *choice)
{
    if (A > choice->score)
        return A;
    else
        return choice->score;
}

double min(double B, Do *choice)
{
    if (B < choice->score)
        return B;
    else
        return choice->score;
}

Do* Find(Othello* board, enum Option player, int step, int B, int A, Do* choice)
{
    choice->pos.first = -1;
    choice->pos.second = -1;
    choice->equal = false;
    if(step <= 0)
    {
        choice->score = board->Judge(board);
        return choice;
    }
    Othello* temp;
    int num;
    num = board->Rule(board, player);
    if(num == 0)//无棋可下
    {
        if(board->Rule(board, (enum Option) - player) == 0)//双方都无棋可下
        {
            if(temp->whiteNum < temp->blackNum)//黑子赢
                choice->score = MAX;
            else if(temp->blackNum < temp->whiteNum)//白子赢
                choice->score = -MAX;
            else//平局
                choice->equal = true;
        }
        else
        {
            temp->Copy(temp, board);
            Do* choice_ = Find(temp, (enum Option)- player, step - 1, B, A, choice_);
            choice->score = choice_->score;
        }
    }    
    else
    {
        Do *allChoices = (Do *)malloc(sizeof(Do) * num);
        int k = 0;
        int i, j;
        for(i = 0; i < 6; i++)
        {
            for(j = 0; j < 6; j++)
            {
                if (board->cell[i][j].color == SPACE && board->cell[i][j].stable)
                {
                    allChoices[k].score = -MAX;
                    allChoices[k].pos.first = i;
                    allChoices[k].pos.second = j;
                    allChoices[k].equal = false;
                    k++;
                }
            }
        }
        if (player == BLACK) //max
        {
            for (k = 0; k < num; k++)
            {
                Othello tempBoard;
                Do thisChoice, nextChoice;
                Do *pNextChoice = &nextChoice;
                thisChoice = allChoices[k];
                board->Copy(&tempBoard, board);
                board->Action(&tempBoard, &thisChoice, player);
                A = max(A, Find(&tempBoard, (enum Option) - player, step - 1, B, A, pNextChoice));
                if (B <= A)
                    break;
            }
            choice->score = A;
            choice->pos.first = allChoices[k].pos.first;
            choice->pos.second = allChoices[k].pos.second;
        }
        else //min
        {
            for (k = 0; k < num; k++)
            {
                Othello tempBoard;
                Do thisChoice, nextChoice;
                Do *pNextChoice = &nextChoice;
                thisChoice = allChoices[k];
                board->Copy(&tempBoard, board);
                board->Action(&tempBoard, &thisChoice, player);
                B = min(B, Find(&tempBoard, (enum Option) - player, step - 1, B, A, pNextChoice));
                if (B <= A)
                    break;
            }
            choice->score = B;
            choice->pos.first = allChoices[k].pos.first;
            choice->pos.second = allChoices[k].pos.second;
        }
        free(allChoices);
        return choice;
}