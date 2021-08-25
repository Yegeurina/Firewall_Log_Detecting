import pandas as pd

import csv

korEmployee = pd.read_csv(".\\List\\koreaEmploy.csv",names=['ip','mac'],header=None)
usEmployee = pd.read_csv(".\\List\\USEmploy.csv",names=['ip','mac'],header=None)
server = pd.read_csv(".\\List\\serverList.csv",names=['ip','mac','port'],header=None)


#case 1. 한국 직원 -> 서버 (평일 7:00~21:00)
f = open('.\\Cases\\madeCase1.csv','w')
w=csv.writer(f)
for sidx,src in korEmployee.iterrows() :  
    for didx,dst in server.iterrows() :
        line = list(src)+list(dst)
        w.writerow(line)
f.close()
#case 2. 서버 ->  한국직원 (평일 7:00~21:00)
f = open('.\\Cases\\madeCase2.csv','w')
w=csv.writer(f)
for sidx,src in server.iterrows() :
    for didx,dst in korEmployee.iterrows() :
        ine = list(src)+list(dst)
        w.writerow(line)
f.close()
#case 3. 미국 직원 -> 서버 (평일 7:00~21:00)
f = open('.\\Cases\\madeCase3.csv','w')
w=csv.writer(f)
for sidx,src in usEmployee.iterrows() :
    for didx,dst in server.iterrows() :
        ine = list(src)+list(dst)
        w.writerow(line)
f.close()
#case 4. 서버 -> 미국 직원 (평일 7:00~21:00)
f = open('.\\Cases\\madeCase4.csv','w')
w=csv.writer(f)
for sidx,src in server.iterrows() :
    for didx,dst in usEmployee.iterrows() :
        ine = list(src)+list(dst)
        w.writerow(line)
f.close()