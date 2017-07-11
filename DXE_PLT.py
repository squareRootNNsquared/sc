###
### DXE PLOT GENERATOR (PLT)
###

###	Import necessary packages and scripts ###
import DXE_SC as sc	
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import Image as im
import numpy as np
import os
import sys
import time

def path():### path() returns current directory in string format
		return os.path.dirname(os.path.realpath(sys.argv[0]))

### Plot module ###
def op_plt():

	### Generate standardized plots from database ###
	###	Note: MFC1 is not prepared to gather data.
	plotEngine("HVC","HighVoltageControl")
	plotEngine("VAC1","~VacuumPressure")
	plotEngine("CAP1","Capacitance")
	plotEngine("STR","Strain")
	plotEngine("VAC2","~AtmPressure")
	plotEngine("TMP","Temperature")
	plotEngine("MFC1","FlowParameters")

###
###	UNFINISHED! REMAINING TO DO: Format Graphic as desired
###
### plotEngine("tableName1,tableName2, ... ,tableNameK","verticalAxisLabel")
###
### Accepts table names in a commma separated string as first input argument and produces a standardized plot accordingly, second argument is y-axis (a general) label.
###
def plotEngine(input1,input2):

	### Draw columns in tables as functions of time ###
	if "," in input1:
		tableNames = input1.split(",")
		if tableNames[1] == "":
			tableNames = [tableNames[0]]
	if "," not in input1:
		tableNames = [input1]
	for i in range(0, len(tableNames)):

		table = np.array(sc.db.tableToArrayTR(tableNames[i]))
		if table != []:
			for j in range(2,len(sc.db.columnList(tableNames[i]))):
				if "NOPLT" not in sc.db.columnList(tableNames[i])[j]:
					pl.plot(table[:,1],table[:,j], label='%s ((elem %s))'%(sc.db.columnList(tableNames[i])[j],tableNames[i]))

	### Format Plot ###
	pl.legend(loc='best', fancybox=True, framealpha=.5)
	pl.xlabel('Time (Seconds)')
	if len(tableNames) > 1:
		note1 = " (multiple data sets)"
	if len(tableNames) == 1:
		note1 = ""
	pl.ylabel('%s%s'%(input2,note1))
	pl.savefig('%s/DXE_OUTPUT/DXE_OUT_MONITOR/DXE_OUT_MONITOR_%s.png' %(path(),input2))
	pl.clf()
	pl.cla()