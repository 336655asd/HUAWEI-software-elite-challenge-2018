# -*-coding=utf-8 -*-
from __future__ import division
import os
import sys
import predictor
import datetime
import copy
import collections


#flavor种类
num=23
#n为待预测的种类

def main():
    print 'main function begin.'
    if len(sys.argv) != 4:
        print 'parameter is incorrect!'
        print 'Usage: python esc.py ecsDataPath inputFilePath resultFilePath'
        exit(1)
    # Read the input files
    ecsDataPath = sys.argv[1]
    inputFilePath = sys.argv[2]
    resultFilePath = sys.argv[3]

    data=[]
    #训练数据流
    ecs_infor_array = read_lines(ecsDataPath)
    #输入数据流
    input_file_array = read_lines(inputFilePath)
    # implementation the function predictVm
    #预测，待完成
    """
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)
    # write the result to output file
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)
    """
    for i in range(len(ecs_infor_array)):
        
        data.append(change_rule(ecs_infor_array[i]))
    
    print ('rule start')
    rule,n,time=cut2(input_file_array)
        
    print 'main function end.'
    return data,rule,n,time,resultFilePath

#写入结果
def write_result(string, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
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
        
#(t,t,t,n)
#(13,21,41,42),(13,22,42,43)
#
def change_rule(line):
    line=list(line)
    length=len(line)
    data=[]
    #个位，十位标示，默认各位
    index=[[0,13],[15,22],[23,42]]
    #十位判断
    #是否为长短序列
    if(length==43):
         line.insert(20,'0')
    for i in range(3):
        data.append(line[index[i][0]:index[i][1]])
    return data

#截取
def cut(data):
    cutdata=[]
    for i in range(len(data)):
        cutdata.append(data[i][1][5:7]+data[i][2][5:7]+data[i][2][8:10]+data[i][2][11:13])
    return cutdata

def summary(cutdata):
    flavor=[]
    for i in range(len(cutdata)):
        #print i
        sf=''.join(cutdata[i][0:2])
        f=int(sf)
        sd1=''.join(cutdata[i][2:6])
        d1=int(sd1)
        sd2=''.join(cutdata[i][6:8])
        d2=int(sd2)
        flavor.append([d1,d2,f])
    return flavor

#截取规则
def cut2(input_file_array):
    index=0
    rule=[]
    rule.append([int(input_file_array[0][0:2]),int(input_file_array[0][3:6]),int(input_file_array[0][7:11])])
    index+=2
    #如果是两位数的flavor
    n=input_file_array[index].replace('\r','').replace('\n','')
    n=int(n)
    rule.append(n)
    index+=1
    rule.append([])
    

    for i in range(n):
        flavor=[]
        #rule[2][i].append([1])
        j=6
        #flavorid
        if input_file_array[index][j+1]==' ':
            flavor.append(int(input_file_array[index][j:j+2]))
    
            j+=2
        else:
            flavor.append(int(input_file_array[index][j]))
            j+=1
        #cpu
            #rule[2][i].append([1])
        if input_file_array[index][j+1]==' ':
            flavor.append(int(input_file_array[index][j:j+2]))
            j+=2
        else:
            flavor.append(int(input_file_array[index][j]))
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
    
    
    return
    
    
    
def input_data(flavor,num):
    #num为种类
    c_flag=[]
    #三个时间段
    seg=3
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
        now_d1=flavor[i][0]
        fl=flavor[i][2]
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

#根据flavor种类
def div(in_data,day):
    ditrib=[]
    for i in range(23):
        ditrib.append(in_data[:,i])
    return ditrib

#数据格式
#in_data为每天的floavor增长情况
#rule为input_file_arrays数据的转换

if __name__ == "__main__":
    
    data,rule,n,time,resultFilePath=main()
    #flavor型号
    f_type=[]
    for i in range(n):
        f_type.append(rule[2][i][0])
    cutdata=cut(data)
    flavor=summary(cutdata)
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
    f_sum=[]
    for i in range(num):
        sum_index=0
        for j in range(day):
            sum_index+=in_data[j][i]
        f_sum.append(sum_index)
    all_f=sum(sum_data)
    partion=[]
    for i in range(num):
        partion.append(f_sum[i]/all_f)
        partion[i]=round(partion[i],4)
    avg_day=round(sum(sum_data)/day)
    
    #作图
    """
    plt.plot(range(day),sum_data,label='sum',color='r')
    ditrib=div(in_data,data)
    for i in range(len(ditrib)):
        plt.plot(range(day),ditrib[i])
    """
    pre_f,pre_type,h=predictor.predict_f(rule,partion,day)
    pre_f_copy=copy.copy(pre_f)
    hm=predictor.divide(h,pre_f,pre_type)
    #print hm
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
        counter=collections.Counter(hm[i][3:-1])
        hm_f_id=sorted(counter)
        for j in hm_f_id:
            iterm_f=['flavor'+str(j)+' '+str(counter[j])+' ']
            pre_hm.append(iterm_f)
        pre_hm.append('\n')
    string_h=str(sum_hm_num)+'\n'
    for i in range(len(pre_hm)):
        string_h=string_h+''.join(pre_hm[i])
    with open('test.txt','wb') as f:
        f.write(string_v+string_h)
    out_string=string_v+string_h
    write_result(out_string,resultFilePath)