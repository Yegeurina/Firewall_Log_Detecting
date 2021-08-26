import pandas as pd
import ipaddress

def readEmployeeList():
    employList = pd.read_excel('.\\List\\EMPLOYEE_LIST.xlsx',header=0,usecols=[3,4,5])
    employList['regeion'] = employList['지역']
    employList = employList.drop(['지역'],axis=1)
    employList['ip'] = employList['IP주소'].apply(lambda x: int(ipaddress.ip_address(x.replace('+B2',''))))
    employList=employList.drop(['IP주소'],axis=1)
    employList['mac'] = employList['MAC주소'].apply(lambda x : int(x.replace(':',''),16))
    employList=employList.drop(['MAC주소'],axis=1)
    employList.to_csv('.\\List\\employee.csv',index=False, header=False)

def readServerList():
    serverList = pd.read_excel('.\\List\\SERVER_LIST.xlsx',header=0,usecols=[2,3,4])
    serverList['ip'] = serverList['IP주소'].apply(lambda x: int(ipaddress.ip_address(x.replace('+B2',''))))
    serverList = serverList.drop(['IP주소'],axis=1)
    serverList['mac'] = serverList['MAC주소'].apply(lambda x : int(x.replace(':',''),16))
    serverList = serverList.drop(['MAC주소'],axis=1)
    serverList['port'] = serverList['포트'].apply(lambda x : int(x))
    serverList = serverList.drop(['포트'],axis=1)
    serverList.to_csv('.\\List\\serverList.csv',index=False,header=False)

if __name__ == '__main__' :
    readEmployeeList()
    readServerList()