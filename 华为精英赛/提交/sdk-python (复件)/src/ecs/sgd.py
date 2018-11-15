# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 08:54:04 2018

@author: cc
"""
from __future__ import division
import copy

x=[[1, 2],[2, 1],[2, 3],[3, 5],[1, 3],[4, 2]]
y=[7, 8, 10, 14, 8, 13, 20, 16, 28, 26]
w=[1,1,1,1]
test_x=[]

epoch=10000
min_loss=0.01
rate=0.001

#其中，x[0]为b
#待拟合函数
def pre_y(x,w):
    y=0
    y=w[0]*x[0]+w[1]*x[1]+w[2]*x[2]+w[3]*x[3]
    return y


#loss函数
def loss(x,w,y_label):
    loss=y_label-pre_y(x,w)
    return loss


#随机梯度下降法
def train(x,origion_w,y_label):
    w=copy.deepcopy(origion_w)
    train_loss=loss(x,origion_w,y_label)
    w[0]=origion_w[0]+rate*train_loss*x[0]
    w[1]=origion_w[1]+rate*train_loss*x[1]
    w[2]=origion_w[2]+rate*train_loss*x[2]
    w[3]=origion_w[3]+rate*train_loss*x[3]

    return w

#评价
def evulate(x,origion_w,y_label,w):
    loss_origion=loss(x,origion_w,y_label)
    loss_new=loss(x,w,y_label)
    if loss_new-loss_origion<1:
        print "符合要求"
    return True
    
#产生batch
def gen_batch(x,y):
    length=len(x)
    for i in range(length):
        x[i].insert(0,1)
    
    return zip(x,y)
    
#主程序
def start_train(epoch,batch,min_loss):
    w=[1,1,1,1]
    for eh in range(epoch):
        print "turn-{}".format(eh)
        loss_all=[]
        for bh in batch:
            w=train(bh[0],w,y_label=bh[1])
            loss_=loss(bh[0],w,bh[1])
            loss_all.append(loss_)
        avg_loss=sum(loss_all)/len(batch)
        
        if abs(avg_loss)<min_loss:
            print "符合要求"
            break
            
    return w





if __name__=="__main__":

    batch=gen_batch(x,y)
    w=start_train(epoch,batch,min_loss)    
    
    
