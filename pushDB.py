import MySQLdb

filenum = 157

connection = MySQLdb.Connect(host='localhost', 
                                user='root', 
                                passwd='root', 
                                db='firewall',
                                local_infile=True)

cursor = connection.cursor()

for i in range(0,157) :
    logfile = 'easy2see_'+str(i)+'.csv'
    query = "LOAD DATA INFILE '%s' INTO TABLE firewall.filteredlog FIELDS TERMINATED BY ',';" %(logfile)
    cursor.execute( query )

connection.commit()