#include <iostream>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

int const MAX = 65534;

int deepth = 10; //����������  ���ɵ��ڣ�

//����Ԫ��   ���ӣ���ɫ�����ֱ���

enum Option
{
    WHITE = -1,
    SPACE,
    BLACK //�Ƿ�������  //����
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
    int stable; // �˴�����Ӯ�����
};

//��Ҫ����    ���̼��������ӵ����в���������
struct Othello
{

    WinNum cell[6][6]; //������������6*6������
    int whiteNum;      //������Ŀ
    int blackNum;      //������

    void Create(Othello *board);                                //��ʼ������
    void Copy(Othello *boardDest, const Othello *boardSource);  //��������
    void Show(Othello *board);                                  //��ʾ����
    int Rule(Othello *board, enum Option player);               //�ж������Ƿ���Ϲ���
    int Action(Othello *board, Do *choice, enum Option player); //����,���޸�����
    void Stable(Othello *board);                                //����Ӯ�����
    double Judge(Othello *board);                               //���㱾�����ӷ���
};                                                              //��Ҫ����

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
    if(num == 0)//�������
    {
        if(board->Rule(board, (enum Option) - player) == 0)//˫�����������
        {
            if(temp->whiteNum < temp->blackNum)//����Ӯ
                choice->score = MAX;
            else if(temp->blackNum < temp->whiteNum)//����Ӯ
                choice->score = -MAX;
            else//ƽ��
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