
from numpy import int64
import pandas as pd
import csv

import time as tm

korEmployee = pd.read_csv(".\\List\\koreaEmploy.csv",names=['ip','mac'],header=None)
kor = korEmployee.set_index('ip').T.to_dict('list')
usEmployee = pd.read_csv(".\\List\\USEmploy.csv",names=['ip','mac'],header=None)
us = usEmployee.set_index('ip').T.to_dict('list')
server = pd.read_csv(".\\List\\serverList.csv",names=['ip','mac','port'],header=None)

def korCaseTest(row) :
    row = list(row)

    cmpCase1 = row[:]
    cmpCase2 = row[:]

    del cmpCase1[0]
    del cmpCase1[0]
    del cmpCase1[2]
    del cmpCase1[5]

    del cmpCase2[0]
    del cmpCase2[0]
    del cmpCase2[5]
    del cmpCase2[5]


    try :
        src = kor[cmpCase1[0]]
        dst = server.loc[server['port']==cmpCase1[4]]
        if(len(src)!=0) & (len(dst)!=0) :
            if (src[0]==cmpCase1[1]) & (dst['ip']==cmpCase1[2]).bool() & (dst['mac']==cmpCase1[3]).bool() :
                return False


        src = server.loc[server['port']==cmpCase2[2]]
        dst = kor[cmpCase2[3]]
        if(len(src)!=0) & (len(dst)!=0) :
            if ((src['ip']==cmpCase1[0]).bool() & (src['mac']==cmpCase1[1]).bool() & (dst[0]==cmpCase1[4])) :
                return False
    
    except :
        pass

    return  True

def usCaseTest(row) :
    row = list(row)

    cmpCase3 = row[:]
    cmpCase4 = row[:]

    del cmpCase3[0]
    del cmpCase3[0]
    del cmpCase3[2]
    del cmpCase3[5]

    del cmpCase4[0]
    del cmpCase4[0]
    del cmpCase4[5]
    del cmpCase4[5]
    
    try : 
        src = us[cmpCase3[0]]
        dst = server.loc[server['port']==cmpCase3[4]]
        if(len(src)!=0) & (len(dst)!=0) :
            if ((src[0]==cmpCase3[1]) & (dst['ip']==cmpCase3[2]).bool() & (dst['mac']==cmpCase3[3])).bool() :
                return False
        
        src = server.loc[server['port']==cmpCase4[2]]
        dst = us[cmpCase4[3]]
        if(len(src)!=0) & (len(dst)!=0) :
            if ((src['ip']==cmpCase4[0]).bool() & (src['mac']==cmpCase4[1]).bool() & (dst[0]==cmpCase4[4])) :
                return False
    except :
        pass
    
    return True
    

def analyze():
    
    for i in range(0,157) :
        
        logfile = pd.read_csv('.\\Log\\log_'+str(i)+'.csv',names=['korTime','usTime','srcIP','srcMAC','srcPort','dstIP','dstMAC','dstPort','size'],header=None)
        logfile[['korTime','usTime']]=logfile[['korTime','usTime']].astype(int64)
        
        suspected = '.\\suspectedLog\\suspectedLog_'+str(i)+'.csv'
        print(suspected + " is Create")
        f = open(suspected,'w')
        w=csv.writer(f)
        
        for index,row in logfile.iterrows():
            koreaTime =  tm.gmtime(row['korTime'])
            usTime = tm.gmtime(row['usTime'])
            flag = True
            #case1,2
            if(koreaTime.tm_wday<5) : # 평일인가?
                if((koreaTime.tm_hour>=7 & koreaTime.tm_hour<21) | (koreaTime.tm_hour==21 & koreaTime.tm_min==0 & koreaTime.tm_sec==0)): #출근시간대인가?
                    flag=korCaseTest(row)

            #case3,4
            if(usTime.tm_wday<5 & flag==True) : # 평일인가?
                if((usTime.tm_hour>=7 & usTime.tm_hour<21) | (usTime.tm_hour==21 & usTime.tm_min==0 & usTime.tm_sec==0)): #출근시간대인가?
                    flag=usCaseTest(row)


            if (flag==True) :  
                w.writerow(row)
        
    


if __name__=='__main__' :
    analyze()