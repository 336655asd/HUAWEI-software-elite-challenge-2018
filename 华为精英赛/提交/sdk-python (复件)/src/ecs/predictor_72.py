# -*- coding=utf-8 -*-
#import tensorflow as tf
import copy

"""
#预测flavor各种类数量
"""
def predict_f(rule,partion,avg_day):
    #预测数量
    pre_f=[]
    h=rule[0]
    #num,虚拟机类型个数
    num=rule[1]
    pre_type=rule[3]
    
    for i in range(num):
        p_index=rule[2][i]
        #flavor型号
        index=rule[2][i][0]
        p_index.append(round(rule[4]*avg_day*partion[index-1],0))
        pre_f.append(p_index)
        #最后一位3,为个数
        
    return pre_f,pre_type,h

"""
----------------------分配--------------------------
"""

def divide(h,pre_f,pre_type):
    num=len(pre_f)

    #冒泡排序
    if pre_type=='CPU':
        flag=1
        for i in range(num):
            for j in range(i+1,num):
                if(pre_f[i][1]<pre_f[j][1]):
                    pre_f[i],pre_f[j]=pre_f[j],pre_f[i]
                if(pre_f[i][1]==pre_f[j][1]):
                    if(pre_f[i][2]<pre_f[j][2]):
                        pre_f[i],pre_f[j]=pre_f[j],pre_f[i]
                    
                    
    elif pre_type=='MEM':
        flag=2
        for i in range(num):
            for j in range(i+1,num):
                if(pre_f[i][2]<pre_f[j][2]):
                    pre_f[i],pre_f[j]=pre_f[j],pre_f[i]
                if(pre_f[i][2]==pre_f[j][2]):
                    if(pre_f[i][1]<pre_f[j][1]):
                        pre_f[i],pre_f[j]=pre_f[j],pre_f[i]
    else:
        print 'error'
    #物理服务器
    hm=[]
    #[id,[f_id,num],[],......]
    #初号机
    #虚拟机池
    vm=[]
    vm_index=0
    #各虚拟机所在
    list_vm=[]
    for i in range(num):
        print pre_f[i][3]
        if pre_f[i][3]!=0.0:
            #list_vm_index=[]
        
            num_v_f=int(pre_f[i][3])
            #list_vm_index.append([vm_index,vm_index+num_v_f-1])
            list_vm.append([vm_index,vm_index+num_v_f-1])
            for j in range(num_v_f):
                vm.append(pre_f[i][0:3])
                vm_index+=1
        else:
            list_vm.append(0)
    
    #new_hm=[56,128,1200]

    print list_vm
    #首次适应法

    hm.append(copy.copy(h))
    num_vm=len(vm)
    for i in range(num_vm):
        flag=0
        num_hm=len(hm)
        for index in range(num_hm):

            if hm[index][0]-vm[i][1]>=1 and hm[index][1]-vm[i][2]>=0:
                hm[index].append(vm[i][0])
                hm[index][0]-=vm[i][1]
                hm[index][1]-=vm[i][2]
                flag=1
                break
        if flag==0:
            hm.append(copy.copy(h))
            index+=1
            hm[index].append(vm[i][0])
            hm[index][0]-=vm[i][1]
            hm[index][1]-=vm[i][2]
        print flag
    
    return hm
    

        
    
