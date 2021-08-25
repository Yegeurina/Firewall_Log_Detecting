import re

from datetime import datetime as dt
from datetime import timedelta

import ipaddress

import csv


filePath = '.\\LineSplit\\lineSplit_'
fileNum = 157


regex = re.compile('(?P<datetime>\D+\s\D+\s+\d+\s\d+:\d+:\d+\s\d+)\s\D+\w\D+\s(?P<srcIP>\w+[.]\w+[.]\w+[.]\d+)\s(?P<srcMAC>\w+:\w+:\w+:\w+:\w+:\w+)\s(?P<srcPort>\d+)\s\w+\s\w+\s(?P<dstIP>\w+[.]\w+[.]\w+[.]\w+)\s(?P<dstMAC>\w+:\w+:\w+:\w+:\w+:\w+)\s(?P<dstPort>\d+)\s(?P<PacketSize>\d+)')

for i in range(0,fileNum) :
    fileName = filePath+str(i)+'.csv'
    with open(fileName,'r') as file :
        
        print(fileName + " file Open")
        line = None
        linenum = 0

        logfile = '.\\Log\\log_'+str(i)+'.csv'
        print(logfile + " is Create")
        f = open(logfile,'w')

        w=csv.writer(f)
        while True : 
            line = file.readline()
            if line == '' :
                break
            elif line!='\n' :
                line = line.replace('+B2','')
                param = regex.search(line)
                logline= [0]*9

                date = param.group('datetime')
                date  = dt.strptime(date,"%a %b  %d %H:%M:%S %Y")

                logline[0] = (date-dt(1970,1,1)+timedelta(hours = 9)).total_seconds()
                logline[1] = (date-dt(1970,1,1)+timedelta(hours = -7)).total_seconds()
                 
                srcIP = param.group('srcIP')
                logline[2] = int(ipaddress.ip_address(srcIP)) #srcIP
                srcMAC = param.group('srcMAC')
                logline[3] = int(srcMAC.replace(':',''),16) #srcMAC
                srcPort = param.group('srcPort')
                logline[4] = int(srcPort) #srcPort

                dstIP = param.group('dstIP')
                logline[5] = int(ipaddress.ip_address(dstIP)) #dstIP
                dstMAC = param.group('dstMAC')
                logline[6] = int(dstMAC.replace(':',''),16) #dstMAC
                dstPort = param.group('dstPort')
                logline[7] = int(dstPort) #dstaPort

                size = param.group('PacketSize')
                logline[8] = int(size) #packetsize

                w.writerow(logline)
        f.close()


        