from typing import Type
import pandas as pd
import ipaddress
from datetime import datetime as dt

for i in range(0,157) :
        logfile = pd.read_csv('.\\suspectedLog\\suspectedLog_'+str(i)+'.csv',names=['korTime','usTime','srcIP','srcMAC','srcPort','dstIP','dstMAC','dstPort','size'],header=None)
        
        logfile['korTime'] = logfile['korTime'].apply(lambda x : dt.fromtimestamp(x))
        logfile['usTime'] = logfile['usTime'].apply(lambda x : dt.fromtimestamp(x))
        logfile['srcIP'] = logfile['srcIP'].apply(lambda x : ipaddress.IPv4Address(x))
        logfile['srcMAC'] = logfile['srcMAC'].apply(lambda x : hex(x)[2:].rjust(12,'0'))
        logfile['dstIP'] = logfile['dstIP'].apply(lambda x : ipaddress.IPv4Address(x))
        logfile['dstMAC'] = logfile['dstMAC'].apply(lambda x : hex(x)[2:].rjust(12,'0'))

        logfile.to_csv('.\\easyTosee\\easy2see_'+str(i)+'.csv',header=None,index=False)
        print(i)