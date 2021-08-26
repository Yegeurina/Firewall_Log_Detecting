Days = {'Mon':'\nMon',
            'Tue':'\nTue',
            'Wed':'\nWed',
            'Thu':'\nThu',
            'Fri':'\nFri',
            'Sat':'\nSat',
            'Sun':'\nSun'}

filepath = "firewall.log"
    
roop = True
readbyte = 100000000
remain = ''
num=0
with open(filepath,'r') as file :
    while roop :
        data = file.read(readbyte)
        data = remain+data
        for key in Days :
                data = data.replace(key,Days[key])
        if len(data)<readbyte : 
            roop = False
        else : 
            nullPoint = data.rfind('\n')
            remain = data[nullPoint:]
            data=data[:nullPoint]
        
        filename = '.\\LineSplit\\lineSplit_'+str(num)+'.csv'
        num+=1
        print(num)
        with open(filename,'w') as logfile :
            logfile.write(data)

    if len(remain)!=0 :
        for key in Days :
                data = remain.replace(key,Days[key])
        filename = '.\\LineSplit\\lineSplit_'+str(num)+'.csv'
        with open(filename,'w') as logfile :
            logfile.write(data)