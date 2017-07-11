###
### DXE SQL Database Management (DB)
###

### Import necessary packages and scripts ###
import DXE_SC as sc
import MySQLdb
#import sqlite3
import time as t
import numpy as np
import os
import sys

def path():### path() returns current directory in string format
	return os.path.dirname(os.path.realpath(sys.argv[0]))

###
### SQLITE3 VERSION
###
# ### Create/Open database, Create query cursor (database interactor) ###
# path_db = "%s/DXE_OUTPUT/DXE_OUT_DB.db"%(path())
# db = sqlite3.connect(path_db)
# qc = db.cursor()

###
### MYSQL VESRION (p/w handling insecure?)
###
### Create/Open database, Create query cursor (database interactor)
db = MySQLdb.connect(host="localhost",user="",passwd="",db="DXE_DB")
qc = db.cursor()

###
### UNFINISHED! EFFICIENCY IMPROVEMENTS: Perform certain operations only if table had been made
###				SECURITY CHECKS/IMPROVEMENTS: Secure against injection attacks?
###
### Construct table class; Call creates table such that it's name and columns are passed as separate strings
### addData function accepts a single comma separated string as input, parses and stores in rows per column specifications
###
### Example:: Create table titled "test" with 3 columns (entry number, time (a real number), data (a string)), add data and save:
### test = Table("test","TimeUNITs REAL,DataUNIT TEXT")
### test.addData("'%f','%s'"%(t.time(),"someData"))
###
### IMPORTANT NOTE: Always append units of measure in all lower-case after "UNIT" to column name, append only "UNIT" if entry is dimensionless
###
### IMPORTANT NOTE: Always designate first column (neglecting primary key) to be the time in seconds since epoc labeled "TimeUNITs"
###
### IMPORTANT NOTE: This database may not be properly secured, access thereto must be restricted
###
class Table(object):

	def __init__(self,tableName,tableColumns):

		###
		###	Determine if table has been made prior NN
		###

		### Create list of tables: tableList
		qc.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='DXE_DB'")
		tableList = []
		for table in qc:
			tableList.append(table)

		### Scan tableList for table whose creation is being attempted 
		### Note: Innefficiency improvement: qc can be read and tableFound incremented from directly
		tableFound = 0
		for table in tableList:
			if (tableName in table):    # If table present; Increment tableFound
				tableFound = 1
			else:    # If table present;
				None

		###
		###	James table check
		###

		# table_check_command =	'''
		# SELECT *  FROM information_schema.tables WHERE table_schema = 'DXE_DB' AND table_name = %s LIMIT 1;
		# '''%(tableName)
		# qc.execute(table_check_command)
		# ret = qc.fetchall()
		# if ret[0][2] == tableName:
		# 	tableFound = 1
		# else:
		# 	tableFound = 0


		###
		### Format input columns, format placeholder text, store instance parameters, create table of argument-provided specifications ###	
		###

		### Format table columns 1 ###
		colsFormatted = tableColumns
		colsFormatted = colsFormatted.split(",")
		foundArr = []
		for l in range(0,len(colsFormatted)):
			if "VARCHAR(45)" in colsFormatted[l]:
				foundArr.append(1)
			if "VARCHAR(45)" not in colsFormatted[l]:
				foundArr.append(0)

		for l in range(0, len(colsFormatted)):
			if foundArr[l] == 1:
				colsFormatted[l] = colsFormatted[l].strip(" ")
				colsFormatted[l] = colsFormatted[l].strip(" ")
				colsFormatted[l] = colsFormatted[l].strip(" ")
				colsFormatted[l] = colsFormatted[l].strip(" ")
				colsFormatted[l] = "NOPLT" + colsFormatted[l]
			if foundArr[l] == 0:
				colsFormatted[l] = colsFormatted[l].strip(" ")
				colsFormatted[l] = colsFormatted[l].strip(" ")
				colsFormatted[l] = colsFormatted[l].strip(" ")
				colsFormatted[l] = colsFormatted[l].strip(" ")

		colsPasser = ""
		for l in range(0,len(colsFormatted)):
			colsPasser += colsFormatted[l]
			if l < len(colsFormatted)-1:
				colsPasser += ","
		self.tableColumnsNOPLT = colsPasser

		### Format table columns 2 ###
		tableColumnsNOPLT_formatted1 = self.tableColumnsNOPLT.replace("DOUBLE","")
		tableColumnsNOPLT_formatted1 = tableColumnsNOPLT_formatted1.replace("VARCHAR(45)","")
		self.tableColumnsNOPLT_formatted1 = tableColumnsNOPLT_formatted1.replace(" ","")

		### Format placeholder text ###
		self.placeholders = "("
		for i in range (1,1+len(self.tableColumnsNOPLT_formatted1.split(","))):
			self.placeholders += "?,"
		self.placeholders = self.placeholders.strip(",")
		self.placeholders += ")"

		### Store remaining variables as instance-global ###
		self.tableName = tableName

		### Create table ###
		if tableFound == 0:
			qc.execute('''CREATE TABLE {tn}
						(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
						{tc})'''
						.format(tn=self.tableName,tc=self.tableColumnsNOPLT))

	def addData(self,dataIn):
		DBaddDataPhrase = '''INSERT INTO %s (%s) VALUES (%s);'''%(self.tableName,self.tableColumnsNOPLT_formatted1,dataIn)
		qc.execute(DBaddDataPhrase)
		db.commit()

###
### Outside Class Table Interaction Functions
###
###	NOTE:	CHECK 	=> has been verified to work with MySQL,
###			CHECK? 	=> has been verified so to a lesser extent,
###			!CHECK 	=> has been verified to not yet work.
###

###
### tableList()		CHECK
###
### Creates returned list of tables
###
def tableList():
	qc.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='DXE_DB'")
	tableStr = ""
	tableList = []
	for table in qc:
		tableStr += str(table)
		tableStr = tableStr.replace("u'","")
		tableStr = tableStr.replace("'","")
		tableStr = tableStr.replace(")","")
		tableStr = tableStr.replace("(","")
		tableList = tableStr.split(",")
		tableList = tableList[0:(len(tableList)-1)]

	return tableList

###
### columnList("tableName")		CHECK
###
### Creates returned list of column names of table specified in argument
###
def columnList(tableName):
	qc.execute('''SELECT column_name FROM information_schema.columns WHERE table_schema='DXE_DB' AND TABLE_NAME="%s"'''%(tableName))
	columnStr = ""
	columnList = []
	for column in qc:
		columnStr += str(column)
		columnStr = columnStr.replace("'","")
		columnStr = columnStr.replace(")","")
		columnStr = columnStr.replace("(","")
		columnList = columnStr.split(",")
		columnList = columnList[0:(len(columnList)-1)]

	return columnList

###
### tableToArray("tableName")		CHECK?
###
### Function that assigns database table specified in argument to array that is then returned
###
### Note: Indexing format is [row][column], standard matrix format
###
def tableToArray(tableName):

	### Determine size of table, Alert: Possible inefficiency in colAmt ###
	qc.execute('SELECT id FROM %s'%(tableName))
	rowAmt = len(qc.fetchall())
	qc.execute('SELECT * FROM %s'%(tableName))
	for row in qc:
	   colAmt = len(row)
	    
	### Create array that will hold table ###
	arrayTable = [["" for x in range(colAmt)] for x in range(rowAmt)]

	### Position cursor, Fill array ###
	qc.execute('SELECT * FROM %s'%(tableName))
	i = 0
	j = 0
	for row in qc:
	    j = 0
	    for column in row:
	        arrayTable[i][j] = column
	        j += 1
	    i += 1

	return arrayTable

###
### tableToArrayTR("tableName") tableToArray, Time Range 		CHECK
###
### Function that assigns database table specified in argument to array that is then returned. Only values within plot time range are selected.
###
### Note: Indexing format is [row][column], standard matrix format
###
def tableToArrayTR(tableName):

	### Determine size of table ###
	qc.execute('SELECT * FROM %s WHERE TimeUNITs BETWEEN %f AND %f'%(tableName,sc.par.plotTimeStart,sc.par.plotTimeEnd))
	rowAmt = len(qc.fetchall())
	colAmt = len(columnList("%s"%(tableName)))

	### Create array that will hold table ###
	arrayTable = [["" for x in range(colAmt)] for x in range(rowAmt)]

	### Position cursor, Fill array ###
	qc.execute('SELECT * FROM %s WHERE TimeUNITs BETWEEN %f AND %f'%(tableName,sc.par.plotTimeStart,sc.par.plotTimeEnd))
	i = 0
	j = 0
	for row in qc:
		j = 0
		for column in row:
			arrayTable[i][j] = column
			j += 1
		i += 1

	return arrayTable

###
### printTable("tableName")		CHECK?
###
### Function that prints a table to console.
###
def printTable(tableName):

	### Determine size of table, Alert: Possible inefficiency in colAmt ###
	qc = db.cursor() ### query cursor, interacts with DB
	qc.execute('SELECT id FROM %s'%(tableName))
	rowAmt = len(qc.fetchall())
	qc.execute('SELECT * FROM %s'%(tableName))
	for row in qc:
	   colAmt = len(row)
	    
	### Create array that will hold table ###
	arrayTable = [["" for x in range(colAmt)] for x in range(rowAmt)]

	### Position cursor, Fill array ###
	qc.execute('SELECT * FROM %s'%(tableName))
	i = 0
	j = 0
	for row in qc:
	    j = 0
	    for column in row:
	        arrayTable[i][j] = column
	        j += 1
	    i += 1

	for row in qc:
	   colAmt = len(row)
	i = 0
	j = 0
	while i < rowAmt:
	    j = 0
	    while j < colAmt:
	        print str(arrayTable[i][j]) + "\t" ### PRINT TABLE ARRAY
	        j += 1
	    i += 1
	    print "\n"

###
### tableToFile("tableName")		CHECK
###
### Function to write database table to file, typically for backup purposes
###
def tableToFile(tableName):

	def path():### path() returns current directory in string format
		return os.path.dirname(os.path.realpath(sys.argv[0]))

	### Position cursor, open file ###
	qc.execute('SELECT * FROM %s'%(tableName))
	fout = open("%s/DXE_OUTPUT/DXE_OUT_BACKUP/DXE_OUT_MONITOR_%s_tAll.txt"%(path(),tableName),"w") 

	### Write table to file ###
	for row in qc:
	    fout.write("\n")
	    for column in row:
	        fout.write("%s\t"%(column)) 

	### Close file ###
	fout.close()

###
### tableToFileTR("tableName") tableToFile, Time Range 		!CHECK
###
### Function to write database table to file within plot time range, TR.
###
def tableToFileTR(tableName):

	def path():### path() returns current directory in string format
		return os.path.dirname(os.path.realpath(sys.argv[0]))

	### Position cursor, open file ###
	qc.execute('SELECT * FROM %s WHERE TimeUNITs BETWEEN %f AND %f'%(tableName,sc.par.plotTimeStart,sc.par.plotTimeEnd))
	fout = open("%s/DXE_OUTPUT/DXE_OUT_MONITOR/DXE_OUT_MONITOR_%s_tRANGE.txt"%(path(),tableName),"w") 

	### Write table to file ###
	for row in qc:
		fout.write("\n")
		for column in row:
			fout.write("%s\t"%(column))

	### Close file ###
	fout.close()
