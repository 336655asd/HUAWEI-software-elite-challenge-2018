# coding=utf-8
from __future__ import division
import os
import predictor_72
import datetime
import copy
import collections

import re
#flavor种类
num=23
#n为待预测的种类

    
def main():
    print 'main function begin.'

    ecsDataPath = 'TrainData_2015.1.1_2015.2.19.txt'
    ecsDataPath = 'data2.txt'
    inputFilePath ='input_5flavors_cpu_7days.txt'
    resultFilePath = 'output2.txt'
    data=[]

    #训练数据流
    ecs_infor_array = read_lines(ecsDataPath)
    #输入数据流
    input_file_array = read_lines(inputFilePath)

    for i in range(len(ecs_infor_array)):
        
        data.append(rep(ecs_infor_array[i]))
    
    print ('rule start')
    rule,n,time=cut2(input_file_array)
        
    print 'main function end.'
    return data,rule,n,time,resultFilePath

#写入结果
def write_result(string, resultFilePath):
    with open(resultFilePath, 'w') as output_file:
        output_file.write(string)

#读取数据，返回list
def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None
        
def rep(line):
    p1='[0-9]+'
    pat1=re.compile(p1)
    s=line.strip().replace('\n','').split('\t')

    f=pat1.findall(s[1])
    date=s[2][0:4]+s[2][5:7]+s[2][8:10]
    
    return [int(date),int(f[0])]
#

#截取
def cut(data):
    cutdata=[]
    for i in range(len(data)):
        cutdata.append(data[i][1][6:8]+data[i][2][0:4]+data[i][2][5:7]+data[i][2][8:10])
    return cutdata



#截取规则
def cut2(input_file_array):
    index=0
    rule=[]
    hm_info=input_file_array[0].replace('\n','').split(' ')
    rule.append([int(hm_info[0]),int(hm_info[1]),int(hm_info[2])])    
    index+=2
    #如果是两位数的flavor
    n=input_file_array[index].replace('\r','').replace('\n','')
    n=int(n)
    rule.append(n)
    index+=1
    rule.append([])
    

    for i in range(n):
        flavor=[]
        j=6
        #flavorid
        if input_file_array[index][j+1]==' ':
            flavor.append(int(input_file_array[index][j]))
    
            j+=2
        else:
            flavor.append(int(input_file_array[index][j:j+2]))
            j+=3
        #cpu
            #rule[2][i].append([1])
        if input_file_array[index][j+1]==' ':
            flavor.append(int(input_file_array[index][j]))
            j+=2
        else:
            flavor.append(int(input_file_array[index][j:j+2]))
            j+=1
        #memory
        #rule[2][i].append([1])
        mem=input_file_array[index][j:].replace('\r','').replace('\n','')
        flavor.append(int(mem)/1024)
        rule[2].append(flavor)
        index+=1
        
    index+=1    
    rule.append(input_file_array[index].replace('\r','').replace('\n',''))
    index+=2
        #预测时间
    
    #print index
    start_year=int(input_file_array[index][0:4])
    start_mon=int(input_file_array[index][5:7])
    steat_day=int(input_file_array[index][8:10])
    index+=1    
    end_year=int(input_file_array[index][0:4])
    end_mon=int(input_file_array[index][5:7])
    end_day=int(input_file_array[index][8:10])
    time=(datetime.date(end_year,end_mon,end_day)-datetime.date(start_year,start_mon,steat_day)).days
    rule.append(time)
    return rule,n,time
    #flavor种类
    
    
    
def input_data(flavor,num):
    #num为种类
    c_flag=[]

    flag1=flavor[0][0]
    c_flag.append(flag1)
    for i in flavor:
        if i[0] not in c_flag:
            c_flag.append(i[0])
    #总天数
    day=len(c_flag)
    index_i=0
    #index_j=0
    
    index_d1=flavor[0][0]

          
    data=[]
    df=[0]*num
    for i in range(day):
        data.append(copy.copy(df))
    
    #data=np.zeros([day,num])
    for i in range(len(flavor)):
        #print "第{}个".format(i)
        now_d1=flavor[i][0]
        fl=flavor[i][1]
        #print i
        if now_d1==index_d1:
            data[index_i][fl-1]+=1
        else:
            index_d1=now_d1
            index_i+=1
            data[index_i][fl-1]+=1
        #print '----{}'.format(i)
        #print data[index_i]

    return data,day



#数据格式
#in_data为每天的floavor增长情况
#rule为input_file_arrays数据的转换

if __name__ == "__main__":
    flavor,rule,n,time,resultFilePath=main()
    #flavor型号
    f_type=[]
    for i in range(n):
        f_type.append(rule[2][i][0])

    in_data,day=input_data(flavor,num)
    sum_data=[]
    for i in range(day):
        sumi=0
        for j in range(num):
            sumi+=in_data[i][j]
        
        sum_data.append(sumi)
        #print sumi
    #sum_data=sum(in_data,1)
    #比例
    """此处可优化"""
    f_sum=[]
    for i in range(num):
        sum_index=0
        #for j in range(day):#此处是全局均值
        for j in range(day-time,day):#最后time周期均值
            sum_index+=in_data[j][i]
        f_sum.append(sum_index)
    #all_f=sum(sum_data) #全局flavor数
    all_f=sum(sum_data[day-time-1:day-1])#time周期flavor
    day_f=sum(sum_data[day-time-1:day-1])
    partion=[]
    for i in range(num):
        partion.append(f_sum[i]/all_f)
        partion[i]=round(partion[i],4)
    avg_day=round(day_f/time)
    
    #玄学调参
    pre_f,pre_type,h=predictor_72.predict_f(rule,partion,avg_day)
    pre_f_copy=copy.copy(pre_f)
    hm=predictor_72.divide(h,pre_f,pre_type)
    print hm
    #虚拟机个数
    sum_pre_f=0
    #虚拟机输出:sum_pre_f+'\n',pre_flavor_num
    for i in range(len(pre_f_copy)):
        sum_pre_f+=pre_f_copy[i][3]
    pre_flavor_num=[]
    for i in range(len(pre_f_copy)):
        pre_flavor_num.append('flavor'+str(pre_f_copy[i][0])+' '+str(int(pre_f_copy[i][3]))+'\n')
    pre_flavor_num.append('\n')
    
    string_v=str(int(sum_pre_f))+'\n'+''.join(pre_flavor_num)
    #物理服务器输出
    sum_hm_num=len(hm)
    pre_hm=[]
    for i in range(sum_hm_num):
        hm_id=i+1
        pre_hm.append(str(hm_id)+' ')
        counter=collections.Counter(hm[i][3:len(hm[i])])
        hm_f_id=sorted(counter)
        for j in hm_f_id:
            iterm_f=['flavor'+str(j)+' '+str(counter[j])+' ']
            pre_hm.append(iterm_f)
        pre_hm.append('\n')
    string_h=str(sum_hm_num)+'\n'
    for i in range(len(pre_hm)):
        string_h=string_h+''.join(pre_hm[i])
    string=string_v+string_h
    
    write_result(string,resultFilePath)
    
    
        
    







        
    






