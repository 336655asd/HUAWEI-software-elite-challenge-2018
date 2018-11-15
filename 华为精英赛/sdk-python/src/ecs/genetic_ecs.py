# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 14:16:40 2018

@author: cc
"""
from __future__ import division

import random
import collections
import copy
import time
import sys

"""---------------------超参数---------------------------"""
#繁衍交换染色体个数-->物理服务器个数n:2n
n=1
#物理服务器参数,[[资源利用率，cpu,mem,disk,flaovr1,2......],[]]
h=[0,64,128,1200]
#虚拟服务器参数:flavor1(id),cpu,mem,对flavor重新编码
info_vm=[[1, 1, 1.0, 0.0], [2, 1, 2.0, 2.0], [3, 1, 4.0, 2.0], [4, 2, 2.0, 1.0], [5, 2, 4.0, 7.0]]

vm_id=[1,2,3,4,5]

#vm种类，也是编码的字母
type_vm=5
#
vm=[[5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0], [2, 1, 2.0],[5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0], [2, 1, 2.0],[5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0], [2, 1, 2.0],[5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0], [2, 1, 2.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0], [2, 1, 2.0],[5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0], [2, 1, 2.0],[5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0], [2, 1, 2.0],[5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [5, 2, 4.0], [4, 2, 2.0], [3, 1, 4.0], [3, 1, 4.0], [2, 1, 2.0]]



"""
person个体中单个hm定义：[[利用率,cpu,mem,disk,flavor1,2......],[]......]
"""



class GA:
    
    def __init__(self,vm,best_num_hm):
        
        #虚拟机列表
        self.vm=vm
        #物理服务器：[[资源利用率，cpu,mem,disk,flaovr1,2......]]
        self.best_num_hm=best_num_hm
        self.vm_len=len(vm)
        self.rate_cross=0.3
        self.rate_muta=0.1
        self.G=100
        self.population=60
        #包含所有个体：[总利用率,person]
        self.people=[]
        self.gen_ecs_mans()
        
    #编码,因为编码在此处不分顺序，可以考虑用字典编码(待定)
    def encoding_ff(self,flag):
        rand_vm=copy.deepcopy(self.vm)
        #ture为排序,false为未排序
        if flag==False:
            random.shuffle(rand_vm)
        code=self.FF_gen(rand_vm)

        return code
   #解码
    def decoding(self):
       
       return 
       
    #种群初始化
    #部分随机初始化，部分加入FFD,BFD作为优良个体，2:8
    
    def gen_ecs_mans(self):
        
        for i in range(int(self.population*0.8)):
            self.people.append([0,self.encoding_ff(False)])
        ffd_person=self.encoding_ff(True)
        for i in range(int(self.population*0.2)):
            clon_ffd_person=copy.deepcopy(ffd_person)
            self.people.append([0,clon_ffd_person])
        return self.people
    
    #对所有people进行适应度评判
    def evaluate(self):
        #print "适应度评估"
        for i in range(len(self.people)):
            self.people[i][0]=self.fitness(self.people[i][1])
        self.people=sorted(self.people)
        return
        
    #适应度
    def fitness(self,person):
        efficiency_collection=[]
        N=len(person)
        for i in range(N):
            efficiency=self.efficiency(person[i])
            person[i][0]=efficiency
            efficiency_collection.append(efficiency)
            
        fitness=sum(efficiency_collection)/N
        if fitness>1.0:
            print "over fit"
            #f.writelines("######over fit\n")
        
            time.sleep(6)
            sys.exit("over fit")
        person=sorted(person)
        return fitness
    
    #资源利用率
    def efficiency(self,person_head):

        beta=0.5
        f_cpu_mem=self.resource(person_head)
        f_cpu=f_cpu_mem[0]/h[1]
        f_mem=f_cpu_mem[1]/h[2]
        
        efficent=beta*f_cpu+(1-beta)*f_mem
        """
        if efficent>1.0:
            print "over fit"

            sys.exit("over fit")
            """
        return efficent
    
    #某物理服务器的资源总和
    def resource(self,person_head):
        #各vm数量
        counter=collections.Counter(person_head[4:])
        r_cpu=0
        r_mem=0
        for i in range(type_vm):
            index=vm_id[i]
            r_cpu+=counter[index]*info_vm[i][1]
            r_mem+=counter[index]*info_vm[i][2]
        r_cpu_mem=[r_cpu,r_mem]
        return r_cpu_mem
        
        
    #物竞天择,从父代和子代中寻找最利用率高的poplation个个体
    def selection(self):
        self.people=sorted(self.people,reverse=True)
        del self.people[self.population:]
        return
    
    #交叉繁衍,从适应度高的父代中选择：X,Y
    #比例为0.3
    def crossover(self):
        #print "开始繁衍"
        
        z2=[round(self.people[i][0],4) for i in range(len(self.people))]
        z1=range(self.population)
        for i in range(int(self.population*self.rate_cross)):
            index_father=random_choice(z1,z2,True)
            father=self.people[index_father]
            #index_father=self.people.index(father)
            
            index_mather=random.randint(0,49)
            mather=self.people[index_mather]


            #try:
            count=0
            while(index_father==index_mather or z2[index_mather]==0):
                #print "禁止重复"
                #print "index_father:{}   index_mather:{}".format(index_father,index_mather)
                #print "z2[{}]={}".format(index_mather,z2[index_mather])
                count+=1
                index_mather=random.randint(0,49)
                mather=self.people[index_mather]

            
            self.corssover_once(father[1],mather[1])

            #f.writelines(str(index_father)+str(father)+'\n')
            
            #一夫一妻制,不可以重婚
            z2[index_father]=0
            z2[index_mather]=0

        return
    
    #一次繁衍
    def corssover_once(self,father,mather):
        #最优随机插入算法

        father=sorted(father)
        mather=sorted(mather)
        
        #son继承母体
        son=copy.deepcopy(mather)

        #对母体进行改造
        for i in range(n):

            sperm=copy.deepcopy(father[-1])
            egg=copy.deepcopy(son[0:2])
            son=FFD_GA(sperm,egg,son,True)
                
            son=sorted(son)
        fit=self.fitness(son)
        """
        if fit>1.0:

            sys.exit('over in crossover')
            """
        self.people.append([fit,son])
        return son
    
    #变异,从适应度最低的hm中变异部分身体
    #比例为0.1
    def mutation(self):
        #print "开始变异"
        z2=[self.people[i][0] for i in range(len(self.people))]
        for i in range(int(self.population*self.rate_muta)):
            spiderman=random_choice(self.people,z2,False)
            index=self.people.index(spiderman)

            self.mutation_once(spiderman[1])
            z2[index]=0
        return
    
    #一次变异
    def mutation_once(self,son):

        piter=copy.deepcopy(sorted(son))
        egg=copy.deepcopy(piter[0])

        spiderman=FFD_GA([],egg,piter,False)

        fit=self.fitness(spiderman)
        """
        if fit>1:
            print "###over fit"

            sys.exit("over fit")
            """
        self.people.append([fit,spiderman])

        #self.people.append(spiderman)
        return spiderman
    
    #一次进化
    def evolve(self):
        print "开始进化"
        self.evaluate()
        self.crossover()
        self.mutation()
        self.evaluate()
        self.selection()
        return
    
    #生命跃迁
    def evolution(self,max_evolve):
        
        for i in range(max_evolve):
            print "turn {}".format(i)
            self.evolve()
            if len(self.people[0][1])<=self.best_num_hm:
                
                return self.people[0]
        return self.people[0]
    
    #对随机的vm序列进行FF，返回一组hm为person
    def FF_gen(self,vm):
        hm=[]
        hm.append(copy.deepcopy(h))
        num_vm=len(vm)
        for i in range(num_vm):
            num_hm=len(hm)
            index=0
            while hm[index][1]-vm[i][1]<0 or hm[index][2]-vm[i][2]<0:
                index+=1
                if num_hm-1<index:
                    hm.append(copy.deepcopy(h))
            hm[index].append(vm[i][0])    
            hm[index][1]-=vm[i][1]
            hm[index][2]-=vm[i][2]
        return hm

#用于交叉繁衍时，对于被删除的vm进行重新插入
#sperm为插入hm,egg为被删除的n（2）个hm,son为母体
def FFD_GA(sperm,egg,mather,flag):


    counter_sperm=collections.Counter(sperm[4:])
    if flag==True:
        
        counter_egg=collections.Counter(egg[0][4:]+egg[1][4:])
        
        for i in range(len(egg)):

            
            del mather[0]
        mather.append(sperm)
    else:
        counter_egg=collections.Counter(egg[4:])
        del mather[0]
        

    #删除利用率最低的2个，已排序
    
    #
    #mather.append(sperm)
    num_hm_del=len(mather)
    #字典存储被删除的对象
    #i 代表flaovr的id
    
    dic_replace={}
    for i in vm_id:
        dic_replace[i]=counter_egg[i]-counter_sperm[i]
        
    #按照词典值排序,寻出负数
    sort_replace=sorted(dic_replace.items(),key = lambda x:x[1])
    

    for i in range(type_vm):
        #待重新放置的id
        v_id_list=sort_replace[i][0]
        #id在vm_id中的索引
        v_id=vm_id.index(v_id_list)
        #
        #id数量
        v_replace_num=sort_replace[i][1]
        
        #对于数量小于0的值
        if v_replace_num<0:
            abs_v_replace_num=abs(v_replace_num)
            #mather中循环


            for ma_index in range(num_hm_del):
                    
                #此处要考虑，到底是删除哪一hm中的vm,可以优化
                couter_iterm=collections.Counter(mather[ma_index][4:])
                for i_ in range(couter_iterm[v_id_list]):
                    #remove出错

                    remove_index=mather[ma_index][4:]
                    remove_index.remove(v_id_list)
                    mather[ma_index][4:]=remove_index
                    mather[ma_index][1]+=info_vm[v_id][1]
                    mather[ma_index][2]+=info_vm[v_id][2]
                    v_replace_num+=1
                    if v_replace_num==0:
                        break
                if v_replace_num==0:
                    break

        #跳出循环
                    
        #大于0的情况,直接FFD
        else:
            for rp_index in range(v_replace_num):

                num_hm_deleted=len(mather)
                index=0
                while mather[index][1]-info_vm[v_id][1]<0 or mather[index][2]-info_vm[v_id][2]<0:
                    index+=1
                    if num_hm_deleted-1<index:
                        mather.append(copy.copy(h))
                mather[index].append(info_vm[v_id][0])    
                mather[index][1]-=info_vm[v_id][1]
                mather[index][2]-=info_vm[v_id][2]
                """
                if mather[index][1]>100 or mather[index][0]>1 or mather[index][3]!=1200:

                    sys.exit("error")
                    """
    

    """
    for i in range(len(mather)):
        if mather[i][0]>1 or mather[i][1]>100 or mather[i][3]!=1200:

            sys.exit("error")
            """
    return mather    

#轮盘赌选择
#z1为带选项，z2为评估值
def random_choice(z1,z2,flag):

    p_z=[x/sum(z2) for x in z2]
    #true为升序，false为降序
    if flag==False:
        p_z=sorted(p_z,reverse=True)
    z=zip(z1,p_z)
    ran_num=random.random()
    p_sum=0
    for iterm,p in z:

        try:
            p_sum+=p
            if ran_num<p_sum:
                break
            #print iterm
                return iterm
        
        except:
            print "error"
    return iterm
        
if __name__== '__main__':
    ecs_man= GA(vm,1)
    
    best=ecs_man.evolution(1000)
    
    
    
    
    
    
    
    
    
