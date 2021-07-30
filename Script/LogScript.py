from os import access
import re
import time
from datetime import datetime, timezone
from datetime import timedelta
import ipaddress
import numpy as np
import pandas as pd
import traceback



employList = pd.read_excel('EMPLOYEE_LIST.xlsx',header=0,usecols=[0,3,4])
serverList = pd.read_excel('SERVER_LIST.xlsx',header=0,usecols=[0,2,3,4])
month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def nomalConnectionCheck(line) :
    KST =  timezone(timedelta(hours=9))

    #해당 행 번호 가져오기
    found_raw_employ = list(set(employList.index[employList['MAC주소'] == line[7]].tolist()).intersection(employList.index[employList['IP주소']==line[6]].tolist()))
    if len(found_raw_employ) ==0 :
        return True

    found_raw_server = list(set(serverList.index[serverList['포트'] == int(line[13])].tolist()).intersection(serverList.index[serverList['IP주소'] == line[11]].tolist()))
    if len(found_raw_server) == 0 :
        return True

    #행 번호로 행 가져오기
    raw_employ = employList.loc[found_raw_employ, : ]

    # 서버는 기록이 많아서 여러개가 나옴
    raw_server = serverList.loc[found_raw_server, :]

    # 여기서 시간 체크 UTC + 9 시간 체크해서 07~21 시 이내 사원 -> 서버 접속 필터링(정상 접속)
    if datetime( int(line[4]), month.index(line[1])+1, int(line[2]) ).weekday() > 4 : #Weekend
        return True
    else : #Weekdays
       
        #사원리스트, 서버리스트, 시간 정상 접속 확인

        if (raw_employ['MAC주소']==line[7]).bool() & (raw_employ['IP주소']==line[6]).bool() :
            if (raw_server['IP주소'] == line[11]).bool() & (raw_server['MAC주소'] == line[12]).bool() & (raw_server['포트'] == int(line[13])).bool() :
                accessHMS = line[3].split(':')
                for i in range(0,3) :
                    accessHMS[i]=int(accessHMS[i])
                accessTime = datetime(int(line[4]), month.index(line[1])+1, int(line[2]),accessHMS[0],accessHMS[1],accessHMS[2],tzinfo=KST)
                workingTime =  datetime(int(line[4]), month.index(line[1])+1, int(line[2]),22,0,0,tzinfo=KST)-timedelta(1)
                worktime = datetime(int(line[4]), month.index(line[1])+1, int(line[2]),12,0,0,tzinfo=KST)
                if ((worktime-accessTime).total_seconds() > 0.0) & ((accessTime-workingTime).total_seconds() > 0.0) :
                    return False
                else:
                    return True
            else :
                return True
        else :
            return True

def makeLogRow(line) :
    

    logRow = [0]*11
    
    datetime_str = line[4]+'-'+str(month.index(line[1])+1)+'-'+line[2]+' '+line[3]
    timestamp = time.mktime((datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')-timedelta(hours=-9)).timetuple())

    logRow[0] = timestamp#timestamp
    logRow[1] = line[5] #sourcehost
    
    #src_ip 주소 제대로 들어왔는지 확인
    try :
        logRow[2] = int(ipaddress.ip_address(line[6])) #source IP
    except ValueError : 
        return ['Fail']

    logRow[3] = line[7].replace(':','') #source mac
    logRow[4]=line[8]
    logRow[5] = line[9] #NIC
    logRow[6] = line[10] #destination host
    
    #dst_ip 주소 제대로 들어왔는지 확인
    try :
        logRow[7] = int(ipaddress.ip_address(line[11])) #destination ip
    except ValueError : 
        return ['Fail']

    
    logRow[8] = line[12].replace(':','') #destinaion mac
    logRow[9] = line[13]
    logRow[10] = line[14]
    

    if nomalConnectionCheck(line) == True :
        return logRow
    else :
        return ['Fail']


def SplitLog() :
    file = open("firewall.log")

    re_num = re.compile("\d+")
    re_str = re.compile("[a-zA-z]+")

    readLenth = 1000000
    savingSize = 1000000 #CSV 저장갯수 설정

    lines = []
    last = ''
    remain_line = []

    FileNum = 0
    fileName = "./filterLog/firewallLog_div"
    saveName = fileName + "_" + str(FileNum) + '.csv'

    doAttach = ''
    line_cp = ''

    roop=True
    while roop:
        
        while roop:
            
            line = file.read(readLenth)
            if len(line) < readLenth : 
                roop=False

            # 이게 존나 개중요
            doAttach = line_cp
            line_cp = line[-1]

            # 1. 이전 read의 마지막 값이 ' ' 이면 line에서 새로운 원소가 시작되므로 그냥 append 해주면됨
            # 2. 만약 ' '이 아니라면
            # 3. read한 line에서 이어지는 값이 나올 수도 있고
            # 4. ' ' 이 나와서 새로운 원소가 시작할 수도 있음
            
            # 1, 2 조건을 쉽게 찾을려면 split 하기 전에 line[0] 을 보고 공백인지 아닌지
            # 만약 공백이면 1번, 공백이 아니면 2번으로간다

            # 2번에서 3, 4 조건을 찾으려면
            # doAttach 값이 공백인지 아닌지를 보면 될 것 이다. 아마? 시발 돼라좀

            # 이 분기문을 좀 깔끔하게도 할수있을거같은데 너무헷갈린다 ㅁㄴㅇㄹ
            if line[0] == ' ':

                line = line.split()
                line = remain_line + line

            else :

                line = line.split()
                # 공백이면 별개의 리스트 원소니까 안붙임
                if doAttach == ' ':
                    line = remain_line + line
        
                #안공백이면 붙임
                elif doAttach != ' ' and len(remain_line):

                    last = remain_line.pop()
                    last = last + line[0]
                    del line[0]
                    remain_line.append(last)
                    line = remain_line + line
                

            # 기준을 16 로 잡는게 안전할듯다.. 마직막 원소 짤라줄까?
            while len(line) >= 16:
                temp = line[0:15]
                del line[0:15]
                
               
                
                parse = temp.pop()

                
                packet = re_num.search(parse).group()
                day = re_str.search(parse).group()
                
                temp.append(packet)

                line = [day] + line

                log = makeLogRow(temp)

                

                if not('Fail' in log) :
                    # print('============')
                    # print('[tmep]')
                    # print (temp)
                    # print('[log]')
                    # print(log)
                    # print('============')
                    lines.append(log.copy())
                
                temp.clear()
                 
                if len(lines) == savingSize :
                    print("===[Save CSV]===")
                    np.savetxt( saveName, lines, delimiter=",", fmt ='%s')
                    FileNum = FileNum+1
                    saveName = fileName + "_" + str(FileNum) + '.csv'
                    lines.clear()


            #remain = len(line)%15
            remain_line = line
        
          
    if not(len(line) == 0) :
       np.savetxt( saveName, lines, delimiter=",", fmt ='%s') 

if __name__ == '__main__' :
    SplitLog()
