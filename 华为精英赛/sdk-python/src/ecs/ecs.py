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
import sys
import re
import math
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

    for i in range(len(ecs_infor_array)):
        try:
        
            data.append(rep(ecs_infor_array[i]))
        except:
            print "are you ok?"
            continue
    
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
    s=line.strip().replace('\n','').replace('\r','').split('\t')

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
    in_copy=copy.deepcopy(input_file_array)
    for i in range(len(in_copy)):
        if in_copy[i].strip()=='':
            input_file_array.remove(in_copy[i])
    
    try:
        hm_info=input_file_array[index].strip().replace('\n','').replace('\r','').split(' ')
        rule.append([int(hm_info[0]),int(hm_info[1]),int(hm_info[2])])
    except:
        hm_info=input_file_array[index].strip().replace('\n','').replace('\r','').split('\t')
        rule.append([int(hm_info[0]),int(hm_info[1]),int(hm_info[2])])
    
    
    index+=1
    
    n=input_file_array[index].strip().replace('\r','').replace('\n','')
    n=int(n)
    rule.append(n)
    index+=1
    rule.append([])
    
    p1='[0-9]+'
    pat1=re.compile(p1)
    
    for i in range(n):
        flavor=[]
        try:
            s=input_file_array[index].strip().replace('\n','').replace('\r','').split(' ')
            s0=pat1.findall(s[0])
            s1=pat1.findall(s[1])   
            s2=pat1.findall(s[2])
            
            flavor.append(int(s0[0]))
            flavor.append(int(s1[0]))
            flavor.append(int(s2[0])/1024)
            rule[2].append(flavor)
        except:
            s=input_file_array[index].strip().replace('\n','').replace('\r','').split('\t')
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
    try:
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
    except:
        time=7
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
#按照周的周期来划分
def sum_week(day,sum_data,train_week):
    week_sum=[]
    start=0
    for i in range(7):
        if train_week[i]==6:
            start=i
            break
    cycle_grap=[]
    cycle=day//7
    for i in range(cycle-1):
        
        iterm=sum(sum_data[start+i*7:start+i*7+7])
        week_sum.append(iterm)
        cycle_grap.append(iterm)
        
    last_index=start+(cycle-1)*7
    
    #注释：最后一周剩余flavor总和;最后一周长度，周几；倒数第二周起始
    last_week_info=[day-last_index-1,train_week[-1]]
    second_week_info=[start+i*7,start+i*7+6]
    last_week=[sum(sum_data[last_index:last_index+7]),last_week_info,second_week_info]
    return week_sum,last_week,cycle-1,start,cycle_grap

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
        
        graph=flavor_distribution(in_data,start+i*7,start+i*7+7)
        partion_group_week.append(graph)
        
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
    
#预测调和参数
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

"""--------------------------分割线----------------------------------"""

if __name__ == "__main__":
    flavor,rule,n,time,resultFilePath=main()
    
    vm_id=[]
    for i in range(len(rule[2])):
        vm_id.append(rule[2][i][0])
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
    """---------------------flavor分布数量--------------------"""
    
    #全局采样flavor
    #f_sum_all=flavor_distribution(in_data,0,day)

    #按照最后所需等同采样各falvor情况
    f_sum=flavor_distribution(in_data,day-time,day)
    #all_f=sum(sum_data) #全局flavor数
    
    
    """------------------------每日均值--------------------------"""        
    #
    #所有flavor数量
    #"""
    all_f=sum(sum_data)
    day_f=sum(sum_data[day-time-1:day-1])#time周期flavor
    partion=[]
    for i in range(num):
        partion.append(f_sum[i]/day_f)
        partion[i]=round(partion[i],4)
    avg_day=round(day_f/time)
   
    """----------------------------------------------------------------"""
    #周几
    """
    train_week=train_week(day,str(flavor[0][0]))
    
    week_sum,last_week,cycle,start,cycle_grap=sum_week(day,sum_data,train_week)
    avg_week=round(sum(week_sum)/len(week_sum))
    """
    
    """
    ---------------------------"""
    #周均值
    """
    avg_week=round(sum(week_sum)/len(week_sum)) 

    #最后一周的均值
    avg_week_last=week_sum[-1]
    
    #预测趋势参数
    ama_num=amazing_num(last_week,sum_data,day)
    """
    """
    
    ---------------------最后一周的flavor比例--------------------------    
    """
    """
    f_sum_week=flavor_distribution(in_data,last_week[2][0],last_week[2][1])
    #week中的flavor比例
    partion_week=[]
    for i in range(num):
        partion_week.append(round(f_sum_week[i]/avg_week,4))
        """
    """--------------------flavor占比调试-----------------------------"""
    """
    #按星期，各flavor分布
    partion_group_week=plot_partion(start,cycle)
    #按星期求flaovr占比
    rate_div=partion_div(cycle,partion_group_week)
    
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
            
    #去0中位数比例
    partion_0_median=[]
    for i in range(num):
        sort=sorted(rate_div[i])
        length=len(sort)
        median_index=length//2
        partion_0_median.append(sort[median_index])
        
        """
    """------------------------周中位数-----------------------------------"""
    #week,weekdays=preweek_info(time,week_start,week_end,rule)
    #median_by_week=week_median(partion_group_week,cycle)
    
    
    
    """----------------------预测----------------------------------"""
    #玄学调参
    """取最后天数"""
    #*1.1+同周期等比例采样，结果最好
    #在比例为周中位数，等采样比例
    if rule[1]==3:
        if rule[3]=='CPU':
            pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*1.1)
        else:
            pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*1.205)
    elif rule[1]==5:
        #暂时1.08为最优解
        if rule[3]=='CPU':
            pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*1.08)
        else:
            pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*1.086)
            
    else:
        if rule[3]=='CPU':
            pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*1.145)
        else:
            pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*1.13)

    """按照星期"""
    #2.3结果最好
    #avg_week(均值)+ama_num+partion_0_median=72.3
    #partion_0_median,avg_week*1.8,train_week=70.1
    #最后一周完全采样
    #*ama_num=63
    #1.6=69.4
    #pre_f,pre_type,h=predictor.predict_f_week(rule,partion_0_median,avg_week*ama_num,train_week)
    
    """按照星期中位数"""
    #纯周中位数54.4
    #乘以ama_num=69.90
    #*1.5=66.0
    #*1.8=69.86
    #*2.0=70.70
    #2.1=69.38
    #pre_f,pre_type,h=predictor.predict_f_week_median(rule,[x*2.0 for x in median_by_week],train_week)
    
    
    #pre_f,pre_type,h=predictor.predict_f_day(rule,partion,avg_day*0.8)
    
    ###
    
    """
    plan_a.train_week=train_week
    plan_a.in_data=in_data
    plan_a.time=time
    plan_a.prepare()
    """
    """
    pre_a=plan_a.predict(vm_id)
    for i in range(rule[1]):
        pre_f[i][3]=pre_a[i]
        
        
    pre_f_copy=copy.copy(pre_f)
    """
    
    """-------------------------------状态转移矩阵---------------------------"""
    """
    pre_code=plan_a.decode(vm_id)
    
    for i in range(rule[1]):
        pre_f[i][3]=pre_code[i]
    """
    #test1=plan_a.train_code(vm_id)
        
        
    """------------------------分case-----------------------------""" 
    """
    pre_c=plan_a.pre_case(vm_id)
    
    pre_f_copy=copy.copy(pre_f)
    for i in range(rule[1]):
        pre_f[i][3]=pre_c[i]
    """
    """----------------------------拟合------------------------------------"""
    """
    pre_n=plan_a.muti_line(vm_id)
    for i in range(rule[1]):
        pre_f[i][3]=pre_n[i]
        """
    pre_f_copy=copy.deepcopy(pre_f)
    
    """--------------------放置-------------------------------"""
    hm,vm,num_h=predictor.divide(h,pre_f,pre_type)
    #hm=predictor.BFD(h,pre_f,pre_type)    
    
    
    
    """--------------------------分组遗传算法--------------------------------"""
    try:
        genetic_ecs.vm=vm
        genetic_ecs.num_vm=len(vm)
        genetic_ecs.info_vm=rule[2]
        vm_id=[]
        for i in range(len(rule[2])):
            vm_id.append(rule[2][i][0])
        genetic_ecs.vm_id=vm_id
        genetic_ecs.type_vm=rule[1]
        new_h=[0]+h
        genetic_ecs.h=new_h
        
        
        genetic_ecs.n=1
        
        best_hm=[]
        #杀鸡焉用牛刀
        if len(hm)>=3:
            ecs_man=genetic_ecs.GA(vm,num_h)
    
            best=ecs_man.evolution(1000)
    
            if hm>=len(best[1]):
                for best_index in range(len(best[1])):
                    best_iterm=best[1][best_index][1:]
                    best_hm.append(best_iterm)
                    hm=best_hm
    except:
        pass
    
    print hm
    
    print num_h
    """-------------------------输出---------------------------------"""
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
    
    
        
    






