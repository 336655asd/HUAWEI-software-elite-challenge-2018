# coding=utf-8
from __future__ import division
import os
import predictor
import genetic_ecs
import plan_a
import sgd
import datetime
import copy
import collections
import re
import numpy as np
from matplotlib import pyplot as plt
import math
#flavor种类
num=23
#n为待预测的种类
x=0
y=17.895*pow(x,3)-355.86*pow(x,2)+1993.5*x-1350.1
#多项式拟合

median=[[1, 1, 3.5], [1, 2, 2.0], [1, 3, 3.0], [1, 4, 2.0], [1, 5, 2.0], [1, 6, 2.0], [1, 7, 1.5], [2, 1, 2.0], [2, 2, 5.0], [2, 3, 5.5], [2, 4, 4.0], [2, 5, 3.0], [2, 6, 2.0], [2, 7, 1.5], [3, 1, 1.0], [3, 2, 1.0], [3, 3, 1.0], [3, 4, 1.0], [3, 5, 1.0], [3, 6, 1.5], [3, 7, 1.0], [4, 1, 1.0], [4, 2, 1.0], [4, 3, 2.0], [4, 4, 1.0], [4, 5, 1.0], [4, 6, 1.0], [4, 7, 1.0], [5, 1, 4.5], [5, 2, 3.5], [5, 3, 2.5], [5, 4, 3.5], [5, 5, 2.5], [5, 6, 2.0], [5, 7, 3.0], [6, 1, 1.0], [6, 2, 1.5], [6, 3, 1.0], [6, 4, 1.0], [6, 5, 1.0], [6, 6, 2.0], [6, 7, 1.0], [7, 1, 1.0], [7, 2, 1.0], [7, 3, 1.0], [7, 4, 1.5], [7, 5, 1.0], [7, 6, 6.0], [7, 7, 3.0], [8, 1, 2.5], [8, 2, 3.0], [8, 3, 3.0], [8, 4, 6.0], [8, 5, 2.0], [8, 6, 2.0], [8, 7, 3.5], [9, 1, 3.0], [9, 2, 2.0], [9, 3, 1.0], [9, 4, 1.0], [9, 5, 2.5], [9, 6, 1.5], [9, 7, 1.5], [10, 1, 1.0], [10, 2, 2.0], [10, 3, 1.0], [10, 4, 1.0], [10, 5, 1.0], [10, 6, 0.0], [10, 7, 1.0], [11, 1, 1.0], [11, 2, 3.0], [11, 3, 2.5], [11, 4, 2.0], [11, 5, 2.0], [11, 6, 1.0], [11, 7, 2.0], [12, 1, 4.0], [12, 2, 1.5], [12, 3, 3.0], [12, 4, 2.0], [12, 5, 3.5], [12, 6, 1.5], [12, 7, 1.5], [13, 1, 1.0], [13, 2, 10.0], [13, 3, 1.0], [13, 4, 5.0], [13, 5, 1.0], [13, 6, 0.0], [13, 7, 0.0], [14, 1, 1.0], [14, 2, 3.0], [14, 3, 2.0], [14, 4, 1.0], [14, 5, 3.0], [14, 6, 0.0], [14, 7, 1.5], [15, 1, 5.0], [15, 2, 2.0], [15, 3, 3.5], [15, 4, 2.5], [15, 5, 3.0], [15, 6, 1.0], [15, 7, 1.0]]


def main():
    print 'main function begin.'

    #TrainData_2015.1.1_2015.2.19.txt input_5flavors_cpu_7days.txt output2.txt
    ecsDataPath = 'TrainData_2015.1.1_2015.2.19.txt'
    ecsDataPath = 'data3.txt'
    testDataPath = 'TestData_2015.2.20_2015.2.27.txt'

    inputFilePath ='input_5flavors_cpu_7days.txt'
    inputFilePath = 'rule1.txt'    
    
    data=[]
    test_data=[]
    #训练数据流
    ecs_infor_array = read_lines(ecsDataPath)
    #测试数据流
    test_infor_array = read_lines(testDataPath)
    #输入数据流
    input_file_array = read_lines(inputFilePath)

    """------------------------"""
    #训练数据
    for i in range(len(ecs_infor_array)):
        try:
            data.append(rep(ecs_infor_array[i]))
        except:
            print "are you ok?"
            continue
    #测试数据
    for i in range(len(test_infor_array)):
        test_data.append(rep(test_infor_array[i]))
    
    print ('rule start')
    rule,n,time,week_start,week_end=cut2(input_file_array)
        
    print 'main function end.'
    return data,test_data,rule,n,time,week_start,week_end

#写入结果
def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\n" % item)

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
def p_line(line):
    for i in range(len(line)):
        print '{}\t{}'.format(i,line[i])
    return

#
def rep(line):
    p1='[0-9]+'
    pat1=re.compile(p1)
    s=line.strip().replace('\n','').replace('\r','').split('\t')

    f=pat1.findall(s[1])
    date=s[2][0:4]+s[2][5:7]+s[2][8:10]
    
    return [int(date),int(f[0])]

def change_rule(line):
    line=list(line)
    length=len(line)
    data=[]
    #个位，十位标示，默认各位
    index=[[0,13],[14,22],[23,42]]
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
        cutdata.append(data[i][1][6:8]+data[i][2][0:4]+data[i][2][5:7]+data[i][2][8:10])
    return cutdata

def summary(cutdata):
    flavor=[]
    for i in range(len(cutdata)):
        #print i
        try:
            sf=''.join(cutdata[i][0:2])
            f=int(sf)
            sd1=''.join(cutdata[i][2:10])
            d1=int(sd1)
            flavor.append([d1,f])
        except:
            pass
    return flavor

#截取规则
def cut2(input_file_array):
    index=0
    rule=[]
    in_copy=copy.deepcopy(input_file_array)
    for i in range(len(in_copy)):
        
        if in_copy[i]=='\r\n':
            input_file_array.remove('\r\n')
        elif in_copy[i]=='\n':
            input_file_array.remove('\n')
    hm_info=input_file_array[0].strip().replace('\n','').replace('\r','').split(' ')
    #rule.append([int(input_file_array[0][0:2]),int(input_file_array[0][3:6]),int(input_file_array[0][7:11])])
    rule.append([int(hm_info[0]),int(hm_info[1]),int(hm_info[2])])    
    index+=1
    #如果是两位数的flavor
    n=input_file_array[index].strip().replace('\r','').replace('\n','')
    n=int(n)
    rule.append(n)
    index+=1
    rule.append([])
    
    p1='[0-9]+'
    pat1=re.compile(p1)
    
    for i in range(n):
        flavor=[]
        s=input_file_array[index].strip().replace('\r','').replace('\n','').split(' ')
        s0=pat1.findall(s[0])
        s1=pat1.findall(s[1])   
        s2=pat1.findall(s[2])

        flavor.append(int(s0[0]))
        flavor.append(int(s1[0]))
        flavor.append(int(s2[0])/1024)
        rule[2].append(flavor)
        index+=1
   
    rule.append(input_file_array[index].strip().replace('\r','').replace('\n',''))
    index+=1
        #预测时间
    
    #print index
    start_string=input_file_array[index].strip().replace('\r','').replace('\n','').split(' ')
    start_year=int(start_string[0][0:4])
    start_mon=int(start_string[0][5:7])
    steat_day=int(start_string[0][8:10])
    index+=1    
    
    end_string=input_file_array[index].strip().replace('\r','').replace('\n','').split(' ')
    end_year=int(end_string[0][0:4])
    end_mon=int(end_string[0][5:7])
    end_day=int(end_string[0][8:10])
    time=(datetime.date(end_year,end_mon,end_day)-datetime.date(start_year,start_mon,steat_day)).days
    week_end=datetime.date(end_year,end_mon,end_day).weekday()
    week_start=datetime.date(start_year,start_mon,steat_day).weekday()
    rule.append(time)
    return rule,n,time,week_start,week_end


#flavor数量group by 天
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


#根据flavor种类
def div(in_data,day):
    ditrib=[]
    for i in range(23):
        ditrib.append(in_data[:,i])
    return ditrib


#待预测天数的，周几collection
def preweek_info(time,week_start,week_end,rule):
        flavor_type=[]
        for i in range(rule[1]):
            flavor_type.append(rule[2][i][0])
        week_days=[]
        index=week_start+1
        for i in range(time):
            if index==7:
                week_days.append(index)
                index=1
            else:
                week_days.append(index)
                index+=1
        week=collections.Counter(week_days)
        print week

        return week,week_days

#选取周期（周）中的各flavor中位数
def week_median(partion_group_week,cycle):
    
    median_by_week=[]
    for i in range(num):
        median_seg=[]
        for j in range(cycle):
            median_seg.append(partion_group_week[j][i])
        median_seg=sorted(median_seg)
        index_median=int(math.ceil(cycle/2))
        median_now=median_seg[index_median]
        """
        for seg_i in range(cycle):
            if median_seg[seg_i]>2*median_now:
            """
                
        median_by_week.append(median_now)
    return median_by_week
    
    
#训练日期按照周几序列
def train_week(day,start):
    train_week=[]
    index=datetime.datetime(int(start[0:4]),int(start[4:6]),int(start[6:8])).weekday()+1
    for i in range(day):
        if index==7:
            train_week.append(index)
            index=1
        else:
            train_week.append(index)
            index+=1
    return train_week
    
    

def pre_week(week,median,f_num,f_type,week_days,time):
    pre_f=[]
    for i in range(f_num):
        index=0
        for j in range(1,8):
            index+=week[j]*median[(f_type[i]-1)*7+j-1][2]
            index=int(index)
        pre_f.append([f_type[i],index])
    return pre_f

#按照周的周期来划分
def sum_week(day,sum_data,train_week):
    week_sum=[]
    start=0
    """自动寻找谷底
    for i in range(10):
        if sum_data[start]>sum_data[i]:
            start=i
    """
    #按照周六为谷底
    for i in range(7):
        if train_week[i]==6:
            start=i
            break
    cycle=day//7
    cycle_grap=np.zeros(day)
    div_grap=np.zeros(day)
    for i in range(cycle-1):
        index=start+i*7+3
        iterm=sum(sum_data[start+i*7:start+i*7+7])
        week_sum.append(iterm)
        cycle_grap[index]=iterm
        try:
            div_grap[start+i*7]=200
            
        except:
            pass
    div_grap[start+(i+1)*7]=200
    last_index=start+(cycle-1)*7
    #注释：最后一周剩余flavor总和;最后一周长度，周几；倒数第二周起始
    last_week_info=[day-last_index,train_week[-1]]
    second_week_info=[start+i*7,start+i*7+6]
    last_week=[sum(sum_data[last_index:last_index+7]),last_week_info,second_week_info]
    return week_sum,last_week,cycle-1,cycle_grap,start,div_grap
    
#预测精度评价函数：
def accurate(y,label):
    y=np.array(y,float)
    label=np.array(label,float)
    z=y-label
    precise_seg=z/label
    precise=np.mean(precise_seg)
    return precise_seg,precise
    
#比例
def train_partion(fid,day,in_data):
    fid=fid-1
    seg_partion=[]
    seg_flavor=[]
    for i in range(day):
        seg_partion.append(in_data[i][fid]/sum(in_data[i]))
        seg_flavor.append(in_data[i][fid])
    return seg_partion,seg_flavor
   
#flavor分布
def flavor_distribution(in_data,start,end):
    flavor_dist=[]
    for i in range(num):
        sum_index=0
        for j in range(start,end):#此处是全局均值
            sum_index+=in_data[j][i]
        flavor_dist.append(sum_index)    

    return flavor_dist

#对partion的周分布情况作图
def plot_partion(start,cycle):
    partion_group_week=[]
    
    for i in range(cycle):
        plt.figure('seg_week_partion_'+str(i))
        graph=flavor_distribution(in_data,start+i*7,start+i*7+7)
        partion_group_week.append(graph)
        plt.pie(graph,labels=range(num))
    return partion_group_week
    
#每个flavor的partion分布情况
def partion_div(cycle,partion_group_week):
    rate_div=[]
    for i in range(num):
        rate_div.append([])
        for j in range(cycle):
            sum_flavor_i=sum(partion_group_week[j])
            rate=partion_group_week[j][i]/sum_flavor_i
            rate_div[i].append(round(rate,4))
    return rate_div
    
#预测参数       
def amazing_num(last_week,sum_data,day):
    ama_num=0
    number_of_left=last_week[1][0]
    reference=sum(sum_data[last_week[2][0]:number_of_left+last_week[2][0]])
    devide_num=sum(sum_data[last_week[2][1]+1:day])
    ama_num=devide_num/reference
    return ama_num
#数据格式
#in_data为每天的floavor增长情况
#rule为input_file_arrays数据的转换


"""-----------------------------不专业的分割线-------------------------------"""
if __name__ == "__main__":
    flavor,test_flavor,rule,n,time,week_start,week_end=main()
    vm_id=[]
    for i in range(len(rule[2])):
        vm_id.append(rule[2][i][0])
    #flavor型号
    f_num=rule[1]
    f_type=[]
    for i in range(n):
        f_type.append(rule[2][i][0])

    """-------------训练数据，测试数据-------------------------"""
    in_data,day=input_data(flavor,num)
    out_data,out_day=input_data(test_flavor,num)
    
    #周序列
    train_week=train_week(day,str(flavor[0][0]))
    
####每天的flavor总数
    sum_data=[]
    for i in range(day):
        sumi=0
        for j in range(num):
            sumi+=in_data[i][j]
        sum_data.append(sumi)
        
    
    
    """---------------------flavor分布数量--------------------"""
    
    #全局采样flavor
    f_sum_all=flavor_distribution(in_data,0,day)

    #按照最后所需等同采样各falvor情况
    f_sum=flavor_distribution(in_data,day-time,day)
    
    ##测试数据集
    f_sum_test=flavor_distribution(out_data,0,out_day)


    """------------------------每日均值--------------------------"""        
    #
    #所有flavor数量
    all_f=sum(sum_data)
    day_f=sum(sum_data[day-time-1:day-1])#time周期flavor
    partion=[]
    for i in range(num):
        partion.append(f_sum[i]/day_f)
        partion[i]=round(partion[i],4)
    avg_day=round(day_f/time)
    
    
    """--------------------------作图--------------------------------"""
    plt.figure('cycle')
    plt.plot(range(day),sum_data)
    week_sum,last_week,cycle,cycle_grap,start,div_grap=sum_week(day,sum_data,train_week)
    
    plt.plot(range(day),cycle_grap,color='r')
    plt.bar(range(day),div_grap,color='g')
    

    """---------------------------周均值---------------------------------"""
    #周均值
    avg_week=round(sum(week_sum)/len(week_sum)) 

    #最后一周的均值
    avg_week_last=week_sum[-1]
    
    #预测趋势参数
    ama_num=amazing_num(last_week,sum_data,day)
    
    #
 
    
    """-------------------最后一周的flavor比例--------------------------"""

    f_sum_week=flavor_distribution(in_data,last_week[2][0],last_week[2][1])
    #week中的flavor比例
    partion_week=[]
    for i in range(num):
        partion_week.append(round(f_sum_week[i]/avg_week,4))

    """--------------------flavor占比研究------------------------------"""
    
    fid=5
    seg_partion,seg_flavor=train_partion(fid,day,in_data)
    
    plt.figure('seg_partion_5')
    plt.pie(f_sum_week,labels=range(23))
    plt.figure('all_partion')
    plt.pie(f_sum_all,labels=range(23))
    
    #flavor按照周的分布情况
    partion_group_week=plot_partion(start,cycle)
    rate_div=partion_div(cycle,partion_group_week)
    rate=np.array(rate_div)
    
    """--------------------flavor占比调试-----------------------------"""
    #去0均值比例
    partion_0=[]
    for i in range(num):
        p_num=0
        p_seg=0
        p_seg_sum=0
        for j in range(cycle):
            if rate_div[i][j]!=0:
                p_num+=1
                p_seg=rate_div[i][j]
                p_seg_sum+=p_seg
        if p_num!=0:
            partion_0.append(round(p_seg_sum/p_num,4))
        else:
            partion_0.append(0)
    
    """------------------------周中位数-----------------------------------"""
    #weekdays为预测周几序列
    week,weekdays=preweek_info(time,week_start,week_end,rule)
    median_by_week=week_median(partion_group_week,cycle)
    
    
    
    
    
    """----------------------预测----------------------------------"""
    #玄学调参
    #取最后天数1.1
    pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*1.1)
    #按照星期,2.3
    #pre_f,pre_type,h=predictor.predict_f_week(rule,partion_week,avg_week*ama_num,train_week)
    #按照星期中位数
    #pre_f,pre_type,h=predictor.predict_f_week_median(rule,median_by_week,train_week)
    
    #pre_f_copy=copy.copy(pre_f)
    
    
    """-------------------------------plan-A--------------------------------"""
    plan_a.train_week=train_week
    plan_a.in_data=in_data
    plan_a.prepare()
    #pre_a=plan_a.predict(vm_id)
    #for i in range(rule[1]):
    #    pre_f[i][3]=pre_a[i]
    
    
    
    
    ###
    
    """-------------------------------状态转移矩阵---------------------------"""
    matrix=plan_a.train_code(vm_id)
    pre_code=plan_a.decode(vm_id)
    for i in range(rule[1]):
        pre_f[i][3]=pre_code[i]
        
    

    """------------------------分case-----------------------------"""  
    """
    pre_c=plan_a.pre_case(vm_id)
    
    pre_f_copy=copy.copy(pre_f)
    for i in range(rule[1]):
        pre_f[i][3]=pre_c[i]
        """
    """----------------------------拟合------------------------------------"""
    """
    vm_id_a=range(1,16)
    pre_n=plan_a.pre_223(vm_id_a)
    #for i in range(rule[1]):
    #    pre_f[i][3]=pre_n[i]
    
    """
    pre_f_copy=copy.copy(pre_f)
    """----------------------放置---------------------------------"""
    
    
    
    
    hm,vm,avg_error,now_rh,num_h=predictor.divide(h,pre_f,pre_type)
    
    #hm,vm,left_source=predictor.BFD(h,pre_f,pre_type)
    
    ##精度预测：f_sum_test,pre_f
    
    #分组遗传算法！
    """--------------------------分组遗传算法--------------------------------"""
    genetic_ecs.vm=vm
    genetic_ecs.num_vm=len(vm)
    genetic_ecs.info_vm=rule[2]
    
    genetic_ecs.vm_id=vm_id
    genetic_ecs.type_vm=rule[1]
    new_h=[0]+h
    genetic_ecs.h=new_h
    
    genetic_ecs.n=2
    best_hm=[]
    if len(hm)>=3:
        ecs_man=genetic_ecs.GA(vm,num_h)
    
        best=ecs_man.evolution(100)
    
        if hm>=len(best[1]):
            for best_index in range(len(best[1])):
                best_iterm=best[1][best_index][1:]
                best_hm.append(best_iterm)
            hm=best_hm
    
    print hm
    
    label=[]
    y=[]
    lable_index=[]
    for i in range(len(pre_f)):
        index=pre_f[i][0]
        y.append(pre_f[i][3])
        label.append(f_sum_test[pre_f[i][0]-1])
        lable_index.append(index)
    
    
    print "----------------------精确度---------------------------"
    precise_seg,precise=accurate(y,label)
    print 'flavor编号{}'.format(lable_index)
    print '预测数据:{}'.format(y)
    print '测试数据：{}'.format(label)
    print precise_seg
    print precise
        
    
    
    """------------------------输出文本格式处理-------------------------------"""
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
        counter=collections.Counter(hm[i][4:len(hm[i])])
        hm_f_id=sorted(counter)
        for j in hm_f_id:
            iterm_f=['flavor'+str(j)+' '+str(counter[j])+' ']
            pre_hm.append(iterm_f)
        pre_hm.append('\n')
    string_h=str(sum_hm_num)+'\n'
    for i in range(len(pre_hm)):
        string_h=string_h+''.join(pre_hm[i])
    string=string_v+string_h
    with open('test_cpu.txt','wb') as f:
        f.write(string_v+string_h)

    """----------------最终分析--------------------------------"""
    ow=np.array(partion_group_week)
    p=[]
    o=[]
    for i in range(15):
        p.append([])
        o.append([])
        for j in range(cycle):
            p[i].append(ow[j][i]/sum(ow[j]))
            o[i].append(ow[j][i])
            
    
        
    





