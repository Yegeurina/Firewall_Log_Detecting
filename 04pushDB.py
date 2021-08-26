import MySQLdb

filenum = 157

connection = MySQLdb.Connect(host='localhost', 
                                user='root', 
                                passwd='root', 
                                db='analysisfw',
                                local_infile=True)

cursor = connection.cursor()

for i in range(0,157) :
    logfile = 'log_'+str(i)+'.csv'
    print(logfile)
    query = "LOAD DATA INFILE '%s' INTO TABLE analysisfw.log FIELDS TERMINATED BY ',';" %(logfile)
    cursor.execute( query )

connection.commit()