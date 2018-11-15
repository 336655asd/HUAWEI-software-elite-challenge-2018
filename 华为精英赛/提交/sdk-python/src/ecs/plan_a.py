# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:13:53 2018

@author: cc
"""
from __future__ import division


import copy
import sgd
import math

"""-------------------------------概率转移法--------------------------------"""
#
#参数
#训练日期的周几序列：1,2,3......
train_week=[4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3]

p_start=train_week[-1]+1
if p_start==8:
    p_start=1
#train_week=[2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7]
#[1,周一index,周三index],[2,周四index,周七index]
week_index_list=[]
#周1:3,4:7,1:3,4:7的flavor序列,分flavor类型*15
flavor_data=[]
#状态转移矩阵
state_transfer=[]
#
data_13_47=[]
data_week=[]
data_week_list=[]
time=7
data_week_normal=[]
#
#
#in_data=[[3, 10, 0, 2, 0, 1, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 2, 0, 0, 2, 0, 0, 9, 1, 0, 11, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 3, 0, 1, 3, 1, 1, 0, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 0, 0, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 1, 8, 0, 2, 11, 1, 0, 0, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 3, 0, 2, 4, 0, 6, 0, 0, 1, 1, 4, 0, 1, 0, 6, 0, 0, 0, 0, 3, 1, 0], [7, 1, 0, 18, 2, 0, 2, 22, 1, 11, 2, 0, 0, 3, 0, 0, 0, 5, 0, 0, 3, 2, 0], [26, 1, 0, 1, 1, 0, 2, 2, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 10, 0], [3, 6, 1, 0, 2, 1, 1, 3, 3, 1, 1, 11, 0, 1, 3, 0, 0, 0, 0, 0, 8, 1, 0], [4, 9, 0, 1, 1, 0, 1, 0, 0, 0, 6, 0, 0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 3, 1, 3, 4, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [4, 0, 0, 1, 4, 1, 1, 17, 0, 0, 0, 3, 0, 0, 15, 1, 0, 1, 0, 1, 0, 0, 0], [1, 6, 0, 1, 4, 0, 0, 0, 10, 0, 0, 0, 0, 2, 0, 0, 1, 5, 0, 0, 0, 0, 0], [5, 2, 1, 1, 5, 1, 0, 4, 1, 1, 5, 0, 1, 0, 5, 0, 0, 3, 0, 0, 0, 10, 0], [3, 5, 0, 1, 2, 0, 0, 8, 2, 1, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0], [20, 4, 1, 0, 3, 0, 0, 1, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 10, 2], [3, 1, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [6, 22, 0, 0, 5, 0, 3, 6, 0, 0, 2, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 4, 0], [2, 5, 0, 1, 4, 2, 4, 11, 4, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0], [4, 13, 0, 1, 4, 0, 0, 2, 21, 0, 1, 10, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 1, 1, 2, 4, 7, 0, 12, 0, 0, 1, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0], [7, 8, 0, 0, 0, 0, 0, 20, 8, 1, 0, 16, 1, 1, 0, 8, 4, 0, 0, 1, 0, 14, 0], [2, 3, 0, 2, 2, 0, 11, 8, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 5, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0], [12, 12, 0, 2, 6, 0, 0, 31, 5, 0, 1, 27, 0, 1, 6, 0, 0, 0, 0, 0, 0, 0, 0], [2, 6, 0, 1, 2, 1, 1, 2, 6, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [3, 6, 0, 3, 21, 6, 0, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 1, 0, 1, 0, 0], [1, 5, 0, 1, 3, 0, 0, 17, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 4, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [2, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 2, 1, 0, 3, 0, 0, 1, 5, 0, 2, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 5, 2, 2, 4, 0, 1, 6, 2, 1, 10, 0, 0, 1, 0, 0, 5, 0, 0, 0, 0, 0, 0], [6, 1, 0, 0, 8, 0, 1, 7, 2, 1, 9, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 9, 0, 1, 0, 0, 0, 35, 1, 2, 9, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0], [1, 0, 0, 2, 1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 2], [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 1, 9, 1, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 7, 0, 1, 5, 0, 0, 8, 0, 0, 0, 0, 0, 5, 0, 0, 2, 0, 0, 0, 0, 0, 1], [4, 1, 0, 1, 0, 0, 0, 4, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [3, 9, 0, 6, 5, 1, 1, 11, 1, 1, 3, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 22, 1, 1, 7, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0], [2, 2, 0, 3, 2, 0, 0, 1, 4, 0, 1, 2, 1, 2, 0, 13, 3, 0, 0, 0, 0, 6, 0], [3, 3, 0, 1, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0], [1, 1, 0, 1, 2, 0, 0, 5, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [3, 4, 1, 1, 1, 1, 2, 9, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 16, 7, 0, 4, 1, 0, 0, 1, 10, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [2, 4, 0, 2, 2, 0, 0, 16, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0], [5, 6, 1, 2, 9, 0, 0, 10, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 4, 0, 1, 1, 0, 0, 3, 3, 0, 8, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 6, 8, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 5, 0, 1, 1, 0, 0, 7, 1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 2, 10, 0, 1, 3, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 5, 2, 0, 1, 0, 0, 7, 5, 2, 3, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0], [2, 7, 1, 5, 6, 0, 1, 5, 1, 0, 4, 7, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0], [4, 0, 0, 3, 5, 1, 3, 12, 1, 0, 6, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0], [2, 1, 0, 1, 3, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
in_data=[[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 12, 1, 0, 4, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 3, 6, 0, 0, 5, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 4, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 6, 1, 1, 1, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 2, 0, 11, 0, 0, 7, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 3, 0, 0, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 6, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0], [0, 2, 1, 0, 0, 0, 4, 7, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 8, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 27, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#离散方法
#attention model
attention_time=0
attention_similarity=0
similarity_array=[]
median_list=[]

"""---------------------------数据异常处理----------------------------------"""
def median_process(data_week_list,data_week):
    env_length=len(data_week_list[0])
    for i in range(15):
        d_copy=copy.deepcopy(data_week[i])
        d_copy=sorted(d_copy)
        if env_length%2==0:
            median=(d_copy[env_length//2]+d_copy[(env_length//2)-1])/2
        else:
            median=d_copy[env_length//2]
        median_list.append(int(round(median)))
    return median_list

def abnormal(data_week_list,data_week,data_week_normal):
    data_week_normal=copy.deepcopy(data_week)
    env_length=len(data_week_list[0])
    for i in range(15):
        median=median_list[i]
        for j in range(env_length):
            if data_week[i][j]>2*median:
                if j==0:
                    for h in range(3):
                        data_week_list[i][j][h]=copy.deepcopy((data_week_list[i][j+1][h]+data_week_list[i][j+2][h])//2)
                elif j==env_length-1:
                    for h in range(3):
                        data_week_list[i][j][h]=copy.deepcopy((data_week_list[i][j-1][h]+data_week_list[i][j-2][h])//2)
                else:
                    for h in range(3):
                        data_week_list[i][j][h]=copy.deepcopy((data_week_list[i][j-1][h]+data_week_list[i][j+1][h])//2)
                data_week_normal[i][j]=sum(data_week_list[i][j])
    return data_week_normal


#周期index
def process_week_index_list(train_week):
    for i in range(len(train_week)):
        if train_week[i]==1:
           week_index_list.append([i,1])
        elif train_week[i]==3:
           week_index_list.append([i,3])
        elif train_week[i]==4:
           week_index_list.append([i,4])
        elif train_week[i]==5:
            week_index_list.append([i,5])
    if week_index_list[0][0]==3 or week_index_list[0][0]==7:
        del week_index_list[0]
    return week_index_list
    
#23,45,61采样拟合
def sample_23_45_61(train_week,in_data,flavor_id):
    
    seg=int(math.floor(time/3))
    seg3=seg+time-3*seg
    start=0
    length=len(train_week)
    sample=[]
    sample_sum=[]
    for i in range(length):
        if train_week[i]==p_start:
            start=i
            break
    index=start
    while index+6<length :
        sample1=0
        for i1 in range(seg):
            sample1+=in_data[index+i1][flavor_id-1]
        index+=seg
        sample2=0
        for i2 in range(seg):
            sample2+=in_data[index+i2][flavor_id-1]
        index+=seg
        sample3=0
        for i3 in range(seg3):
            sample3+=in_data[index+i3][flavor_id-1]
        index+=seg3
        sample.append([sample1,sample2,sample3])
        iterm_sum=sample1+sample2+sample3
        sample_sum.append(iterm_sum)
    return sample,sample_sum
#1347采样
#2:3,4:5,6:1
def sample_1347(week_index_list,in_data,flavor_id):
    #周一下标
    data_1347_seg=[]
    data_week_seg=[]
    start=0
    for i in range(4):
        if week_index_list[i][1]==1:
            start=i
    
    before=start
    final=before+2
    while final+3<=len(week_index_list):
        sum_13=0
        for i3 in range(3):
            sum_13+=in_data[week_index_list[before][0]+i3][flavor_id-1]
        sum_47=0
        for i7 in range(4):
            sum_47+=in_data[week_index_list[final][0]+i7][flavor_id-1]
        data_1347_seg.append([sum_13,sum_47])
        data_week_seg.append(sum_13+sum_47)
        before=before+4
        final=final+4
        
    return data_1347_seg,data_week_seg


#求所有flaovr的13_47:[[1_3,4_7]]
def data_3_7(in_data,f_type):
    #作为下标减一

    for f_index in f_type:
        #sample_seg,sample_week=sample_1347(week_index_list,in_data,f_index)
        sample,sample_week=sample_23_45_61(train_week,in_data,f_index)
        #data_week_list.append(sample_23_45_61(train_week,in_data,f_index))
        data_week_list.append(sample)
        
        #data_13_47.append(sample_seg)
        data_week.append(copy.deepcopy(sample_week))
    return data_13_47,data_week


    
"""----------------------------环境相似度-----------------------------------"""

def predict(to_pre_id):
    pre_flavor=[]
    for _id in to_pre_id:
        flavor_id=_id
        iterm=predict_sim_seg(flavor_id,data_week[flavor_id-1])
        pre_flavor.append(iterm)
    
    return pre_flavor

#预测单个flavor,env_data为当前Id的分周总数
def predict_sim_seg(flavor_id,env_data,alfa=0.9):
    pre_flavor=0
    
    #环境矩阵
    env=data_week_list[flavor_id-1]
    
    env_length=len(env_data)
    sim=process_similarity(env,env_length-1)
    sim_copy=copy.deepcopy(sim)
    #count=3
    #对env加下标
    for i in range(len(sim)):
        sim_copy[i].append(i)
    sim_copy=sorted(sim_copy)
    top2=sim_copy[0:2]
    for i in range(2):
        top2[i][0]+=1

    sum_time=top2[0][1]+top2[1][1]+2
    sum_sim=0
    a_time=[]
    a_sim=[]
    for i in range(2):
        
        sum_sim+=top2[i][0]
    s=sum_sim/top2[0][0]+sum_sim/top2[1][0]
    
    s1=s/top2[0][0]
    s2=s/top2[1][0]
    s=s1+s2
    
    a_sim.append(s1/s)
    a_sim.append(s2/s)
    for i in range(2):
        t=(top2[i][1]+1)/sum_time
        a_time.append(t)
        
    #加上拟合
    #pre_flavor=alfa*env_data[-1]+(1-alfa)*(env_data[top2[0][1]+1])
    #pre_flavor=1.1*env_data[-1]    
    pre_flavor=alfa*env_data[-1]*1.1+(1-alfa)*(a_sim[0]*env_data[top2[0][1]+1]+a_sim[1]*env_data[top2[1][1]+1])
    #pre_flavor=alfa*env_data[-1]+(1-alfa)*(a_sim[0]*a_time[0]*env_data[top2[0][1]+1]+a_sim[1]*a_time[1]*env_data[top2[1][1]+1])
    return int(round(pre_flavor))

#生成环境相似度矩阵
def gen_sim(data_week_list,env_index):
    
    for i in  range(15):
        similarity_array.append(process_similarity(data_week_list[i],env_index-1))
    
    return similarity_array


#判断环境相似度
def process_similarity(flavor_env,env_index):
    sim_env=[]
    env_now=flavor_env[env_index]
    for i in range(env_index):
        sim_iterm=distance(flavor_env[i],env_now)
        sim_env.append(sim_iterm)
        
    return sim_env

#一个环境的欧式距离
def distance(env_constast,env_now):
    sim_env=[]
    env_length=len(env_now)
    sim_iterm=0
    for i in range(env_length):
        sim_iterm+=pow((env_now[i]-env_constast[i]),2)
    sim_env.append(sim_iterm)
    return sim_env

"""--------------------------------函数拟合---------------------------------"""
#223切分拟合
def pre_223(to_pre_id):
    pre_flavor=[]
    for i in to_pre_id:
        pre_flavor.append(www(i))
    
    return pre_flavor


#由环境矩阵拟合
def www(flavor_id):
    index=flavor_id-1
    batch=[]
    x=[]
    y=[]
    for i in range(len(data_week[0])-1):
        x_seg=data_week_list[index][i]
        y_seg=data_week[index][i+1]
        x.append(x_seg)
        y.append(y_seg)
    
    batch=sgd.gen_batch(x,y)
    w=sgd.start_train(1000,batch,0.01)
    pre_flavor=sgd.pre_y([1]+data_week_list[index][-1],w)
    return int(pre_flavor)


"""----------------------分case---------------------------------------------"""
def pre_case(to_pre_id):
    pre_flavor=[]
    for i in to_pre_id:
        pre_flavor.append(case(i))
    
    return pre_flavor



def case(flavor_id):
    ##中位数,曲线平稳
    if flavor_id==1:
        return median_list[0]
    elif flavor_id==3:
        return median_list[2]
    elif flavor_id==4:
        return median_list[3]
    elif flavor_id==7:
        return median_list[6]
    elif flavor_id==9:
        return median_list[8]
    elif flavor_id==10:
        return median_list[9]
    elif flavor_id==13:
        return median_list[12]
    elif flavor_id==15:
        return median_list[14]
    
    ###函数,波动性大
    elif flavor_id==2:
        return predict_sim_seg(flavor_id,data_week[flavor_id-1])
    elif flavor_id==5:
        return predict_sim_seg(flavor_id,data_week[flavor_id-1])
    elif flavor_id==8:
        return predict_sim_seg(flavor_id,data_week[flavor_id-1])
    
    #####第三者,特征不明显
    elif flavor_id==6:
        return predict_sim_seg(flavor_id,data_week[flavor_id-1])
    elif flavor_id==11:
        return predict_sim_seg(flavor_id,data_week[flavor_id-1])
    elif flavor_id==12:
        return predict_sim_seg(flavor_id,data_week[flavor_id-1])
    elif flavor_id==14:
        return predict_sim_seg(flavor_id,data_week[flavor_id-1])
    
    
"""---------------------------状态转移--------------------------------------"""
def decode(vm_id):
    alfa=0.9
    pre_flavor=[]
    code_matrix=train_code(vm_id)
    
    for i in range(len(vm_id)):
        code=code_matrix[i]
        w1_1=code[0]/sum(code)
        w0_9=code[1]/sum(code)
        w_t=1.2*w1_1+0.9*w0_9
        now_data=copy.deepcopy(data_week[vm_id[i]-1][-1])
        if now_data<=3:
            if now_data>1.1:
                now_data+=1
            elif now_data<1.1:
                now_data-=1
                if now_data<=0:
                    now_data=0
        else:
            iterm=predict_sim_seg(vm_id[i]-1,data_week[vm_id[i]-1])
            now_data=alfa*(now_data*w_t)+(1-alfa)*iterm
            if data_week[vm_id[i]-1][-1]>3*median_list[vm_id[i]-1]:
                now_data=median_list[vm_id[i]-1]
        
        flavor_seg=int(round(now_data))
        pre_flavor.append(flavor_seg)
    
    
    return pre_flavor

def train_code(vm_id):
    code_matrix=[]
    for i in vm_id:
        code_matrix.append(turn_code(i))
    return code_matrix
    
def turn_code(flavor_id):
    length=len(data_week[0])
    code_data=data_week[flavor_id-1]
    base=copy.deepcopy(code_data[-1])
    code=[0,0]
    for i in range(length-1):
        if code_data[i]>base:
            code[0]+=1
        elif code_data[i]<=base:
            code[1]+=1
    return code

"""-----------------------------偏置补偿------------------------------------"""
def line(flavor_id):
    index=flavor_id-1
    y=data_week[index]
    x=[]
    for i in range(1,len(y)+1):
        x.append([i])
    batch=sgd.gen_batch(x,y)
    w=sgd.start_train(3000,batch,0.1)
    pre_flavor=sgd.pre_y([1,len(y)],w)
    pre_flavor_p=sgd.pre_y([1,len(y)-1],w)
    p=y[-1]/pre_flavor_p
    r=int(round(pre_flavor*p))
    if data_week[flavor_id-1][-1]>3*median_list[flavor_id-1]:
        r=median_list[flavor_id-1]
    return r
"""
def bias_line(flavor_id):
    index=flavor_id-1
    y=data_week[index]
    y_label=data_week[index]
    length=len(y)
    x=[]
    for i in range(1,length+1):
        x.append([i])
    batch=sgd.gen_batch(x,y)
    w=sgd.start_train(3000,batch,0.1)
    pre_f_all=[]
    error=[]
    for i in range(length):
        pre_f_all.append(sgd.pre_y([1,i+1],w))
    error0=pre_f_all[length-3]-y_label[length-3]
    error1=pre_f_all[length-2]-y_label[length-2]
    pre_flavor=pre_f_all[-1]
    compensate=[0]

    return int(round(pre_flavor)),pre_f_all
    """
    
    
def muti_line(vm_id):
    pre_flavor=[]
    for i in vm_id:
        pre_flavor.append(line(i))

    return pre_flavor


def bias_return(flavor_id):
    
    return 
    
    





"""---------------------------数据处理-------------------------------------"""


def prepare():

    f_type=range(1,16)
    #week_index_list=process_week_index_list(train_week=train_week)
    p_start=train_week[-1]+1
    if p_start==8:
        p_start=1
    data_13_47,data_week=data_3_7(in_data,f_type)
    median_list=median_process(data_week_list,data_week)
    #abnormal(data_week_list,data_week,data_week_normal)
    length=len(data_week[0])
    gen_sim(data_week_list,length)
    return median_list,data_week_normal

if __name__=="__main__":

    prepare()
    flavor_id=5
    
    future=predict_sim_seg(flavor_id,data_week[flavor_id-1])
    future=int(round(future))
    print future
    
    pre_plan_a=predict(range(1,6))
    print pre_plan_a
    
    pre_flavor=www(5)
    print pre_flavor
    
    #flavor_case=pre_case(range(1,6))
    #print flavor_case
    
    pre_t=decode(range(1,8))
    print "转移编码"
    print pre_t
    
    
    print "线性回归"
    pre_line=bias_line(flavor_id)
    print pre_line
    pre_muti_line=muti_line(range(1,6))
    print pre_muti_line