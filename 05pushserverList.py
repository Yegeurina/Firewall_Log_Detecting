import MySQLdb

filenum = 157

connection = MySQLdb.Connect(host='localhost', 
                                user='root', 
                                passwd='root', 
                                db='analysisfw',
                                local_infile=True)

cursor = connection.cursor()

logfile = 'serverList.csv'
query = "LOAD DATA INFILE '%s' INTO TABLE analysisfw.server FIELDS TERMINATED BY ',';" %(logfile)
cursor.execute( query )

connection.commit()
print("server")
