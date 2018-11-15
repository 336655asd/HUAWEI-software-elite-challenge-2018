# -*- coding=utf-8 -*-
#import tensorflow as tf
import copy

#预测flavor各种类数量

def predict_f_day(rule,partion,avg_day):
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

#按照星期
def predict_f_week(rule,partion,avg_week,train_week):
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
        #p_index.append(round((rule[4]//7+1-(pow(0.5,abs[6-train_week))*avg_week)*partion[index-1]))
        p_index.append(round((rule[4]/7*avg_week)*partion[index-1]))        
        pre_f.append(p_index)
        #最后一位3,为个数
        
    return pre_f,pre_type,h


#按照星期中位数

def predict_f_week_median(rule,median_by_week,train_week):
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
        #p_index.append(round((rule[4]//7+1-(pow(0.5,abs[6-train_week))*avg_week)*partion[index-1]))
        p_index.append(round((rule[4]/7*median_by_week[index-1])))        
        pre_f.append(p_index)
        #最后一位3,为个数
        
    return pre_f,pre_type,h
    
    
    
def divide(h,pre_f,pre_type):
    num=len(pre_f)

#CPU还是MEM完全对结果没有影响啊喂!
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
        num_hm=len(hm)
        index=0
        while hm[index][0]-vm[i][1]<0 or hm[index][1]-vm[i][2]<0:
            index+=1
            if num_hm-1<index:
                hm.append(copy.copy(h))
        hm[index].append(vm[i][0])    
        hm[index][0]-=vm[i][1]
        hm[index][1]-=vm[i][2]

    num_h=0
    """------------------------------求最优资源量----------------------------"""    
    #rv,rh,资源总量 
    rv=0
    rv_c=0
    rv_m=0
    seg_rh=0
    flag=0
    now_rh=[]#每台物理服务器当前剩余资源
    if pre_type=='CPU':
        flag=1
        seg_rh=h[0]
        for i in range(len(pre_f)):
            rv_c+=pre_f[i][1]*pre_f[i][3]
        for i in range(len(hm)):
            now_rh.append(hm[i][0])
        rv=rv_c
    elif pre_type=='MEM':
        flag=2
        seg_rh=h[1]
        for i in range(len(pre_f)):
            rv_m+=pre_f[i][2]*pre_f[i][3]
            
        for i in range(len(hm)):
            now_rh.append(hm[i][1])
        rv=rv_m
    else:
        print ("error")
    num_h=max(int(rv_c//h[0]),int(rv_m//h[1]))+1
    
    return hm,vm,num_h
    
    
    
"""-----------------------------最佳适应算法--------------------------------"""    
def BFD(h,pre_f,pre_type):
    num=len(pre_f)

#CPU还是MEM完全对结果没有影响啊喂!
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

            num_v_f=int(pre_f[i][3])

            list_vm.append([vm_index,vm_index+num_v_f-1])
            for j in range(num_v_f):
                vm.append(pre_f[i][0:3])
                vm_index+=1
        else:
            list_vm.append(0)
    
    #new_hm=[56,128,1200]
    num_vm=len(vm)
    print list_vm
    #最佳适应算法
    """------------分割线----------"""
    #rv,rh,资源总量 
    rv=0
    rv_c=0
    rv_m=0
    seg_rh=0
    flag=0
    if pre_type=='CPU':
        flag=1
        seg_rh=copy.copy(h[0])
        for i in range(len(pre_f)):
            rv_c+=pre_f[i][1]*pre_f[i][3]
        rv=rv_c
    elif pre_type=='MEM':
        flag=2
        seg_rh=copy.copy(h[1])
        for i in range(len(pre_f)):
            rv_m+=pre_f[i][2]*pre_f[i][3]
        rv=rv_m
    else:
        print ("error")
    best_num=max(int(rv_c//h[0]),int(rv_m//h[1]))+1
    
    left_resource=[]
    for i in range(best_num):
        hm.append(copy.copy(h))
        if pre_type=='CPU':
            left_resource.append([hm[i][0],i])
        else:
            left_resource.append([hm[i][1],i])
        
    for i in range(num_vm):
        flag=0
        sorted(left_resource)
        index=left_resource[0][1]
        if hm[index][0]-vm[i][1]>=1 and hm[index][1]-vm[i][2]>=0:
            hm[index].append(vm[i][0])
            hm[index][0]-=vm[i][1]
            hm[index][1]-=vm[i][2]
            
            flag=1
        else:
            flag=2
            for j in range(1,len(hm)):
                if flag==2:
                    index=left_resource[j][1]
                    if hm[index][0]-vm[i][1]>=1 and hm[index][1]-vm[i][2]>=0:
                        hm[index].append(vm[i][0])
                        hm[index][0]-=vm[i][1]
                        hm[index][1]-=vm[i][2]
                        flag=1
                        break
                    else:
                        continue
        if flag==2:
            hm.append(copy.copy(h))
            if pre_type=='CPU':
                left_resource.append([hm[-1][0],len(hm)-1])
            else:
                left_resource.append([hm[-1][1],len(hm)-1])
            hm[-1].append(vm[i][0])
            hm[-1][0]-=vm[i][1]
            hm[-1][1]-=vm[i][2]
            flag=1
        

    return hm