#-*- coding=utf-8 -*-
import csv
import re
median=[]
p1='[0-9]+'
pat1=re.compile(p1)

with open('median.csv','rb') as f:
    reader=csv.reader(f)
    for row in reader:
        median.append(row)

result=[]
for i in range(1,len(median)):
    flavor=pat1.findall(median[i][0])
    flavor=int(flavor[0])
    row1=int(median[i][1])
    row2=float(median[i][2])
    result.append([flavor,row1,row2])
    
        
    #    except:
    #        pass
        
        
