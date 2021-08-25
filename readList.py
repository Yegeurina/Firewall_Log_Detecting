import pandas as pd
import ipaddress

def readEmployeeList():
    employList = pd.read_excel('.\\List\\EMPLOYEE_LIST.xlsx',header=0,usecols=[3,4,5])
    
    koreaEmploy = employList.groupby('지역').get_group('Korea')
    koreaEmploy=koreaEmploy.drop(['지역'],axis=1)
    koreaEmploy['ip'] = koreaEmploy['IP주소'].apply(lambda x: int(ipaddress.ip_address(x.replace('+B2',''))))
    koreaEmploy=koreaEmploy.drop(['IP주소'],axis=1)
    koreaEmploy['mac'] = koreaEmploy['MAC주소'].apply(lambda x : int(x.replace(':',''),16))
    koreaEmploy=koreaEmploy.drop(['MAC주소'],axis=1)
    koreaEmploy.to_csv('.\\List\\koreaEmploy.csv',index=False,header=False)


    USEmploy = employList.groupby('지역').get_group('US')
    USEmploy = USEmploy.drop(['지역'],axis=1)
    USEmploy['ip'] = USEmploy['IP주소'].apply(lambda x: int(ipaddress.ip_address(x.replace('+B2',''))))
    USEmploy = USEmploy.drop(['IP주소'],axis=1)
    USEmploy['mac'] = USEmploy['MAC주소'].apply(lambda x : int(x.replace(':',''),16))
    USEmploy = USEmploy.drop(['MAC주소'],axis=1)
    USEmploy.to_csv('.\\List\\USEmploy.csv',index=False,header=False)

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