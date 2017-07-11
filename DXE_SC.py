###
### DXE SLOW CONTROL (SC)
###
### NOTE: Enable/Disable operation of computer interfaced devices with "op_..." variables in file DXE_LIB_SC_PAR
###
###	NOTE: Only most recent errors are logged in ~DXE/DXE_OUTPUT/DXE_OUT_MONITOR
###

###	Import necessary packages and scripts ###
import DXE_LIB_SC_PAR as par
import DXE_LIB_DB as db
import DXE_LIB_COM as com
if par.op_sm == 1:
	import DXE_LIB_SM_INI as com_sm
import time as t
import os
import sys
import logging
import math
import pyaudio

def path():
	### Returns current directory in string format.
	return os.path.dirname(os.path.realpath(sys.argv[0]))

def RS():
    ### Non-returning function that restarts current-running python script
    cur = sys.executable
    os.execl(cur, cur, * sys.argv)

def ToneGen(frequency,timeLength):
	###
	###	ToneGen, a tone generator
	###
	###	Dependencies: math, pyaudio(terminal input: sudo apt-get install python-pyaudio)
	###
	BITRATE = 16000    
	FREQUENCY = frequency
	LENGTH = timeLength
	NUMBEROFFRAMES = int(BITRATE * LENGTH)
	RESTFRAMES = NUMBEROFFRAMES % BITRATE
	WAVEDATA = ''    

	for x in xrange(NUMBEROFFRAMES):
		WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+127))    

	for x in xrange(RESTFRAMES): 
		WAVEDATA = WAVEDATA+chr(128)

	### Suppress terminal output
	devnull = os.open(os.devnull, os.O_WRONLY)
	old_stderr = os.dup(2)
	sys.stderr.flush()
	os.dup2(devnull, 2)
	os.close(devnull)

	p = pyaudio.PyAudio()

	### Unsuppress terminal output
	os.dup2(old_stderr, 2)
	os.close(old_stderr)

	stream = p.open(format = p.get_format_from_width(1),
					channels = 1, 
					rate = BITRATE, 
					output = True)
	stream.write(WAVEDATA)
	stream.stop_stream()
	stream.close()
	p.terminate()

def AudibleError():
	###
	###	Warning Sound Submodule
	###
	### Dependency: ToneGen
	###
	startTone = 1000.0
	octaveMultiple = 1.367879441
	initialTime = 0.20
	ToneGen(startTone,initialTime)
	ToneGen(startTone/(octaveMultiple*1.5),initialTime)
	ToneGen(startTone/(octaveMultiple*2.0),initialTime*2.0)

if __name__ == '__main__':

	#######################
	###					###
	###	INITIALIZATION 	###
	###					###
	#######################

	### Slow Control pre-initializations ###
	timeKeeper_sc = t.time()
	EL_PLT = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_PLT.txt"%(path()),"r+")
	EL_CAP1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_CAP1.txt"%(path()),"r+")
	EL_HVC = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_HVC.txt"%(path()),"r+")
	EL_MFC1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_MFC1.txt"%(path()),"r+")
	EL_STR = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_STR.txt"%(path()),"r+")
	EL_TMP = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_TMP.txt"%(path()),"r+")
	EL_VAC1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_VAC1.txt"%(path()),"r+")
	EL_VAC2 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_VAC2.txt"%(path()),"r+")
	ERI_PLT = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_PLT.txt"%(path()),"r+")
	ERI_CAP1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_CAP1.txt"%(path()),"r+")
	ERI_HVC = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_HVC.txt"%(path()),"r+")
	ERI_MFC1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_MFC1.txt"%(path()),"r+")
	ERI_STR = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_STR.txt"%(path()),"r+")
	ERI_TMP = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_TMP.txt"%(path()),"r+")
	ERI_VAC1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_VAC1.txt"%(path()),"r+")
	ERI_VAC2 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_VAC2.txt"%(path()),"r+")
	ERO_PLT = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_PLT.txt"%(path()),"r+")
	ERO_CAP1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_CAP1.txt"%(path()),"r+")
	ERO_HVC = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_HVC.txt"%(path()),"r+")
	ERO_MFC1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_MFC1.txt"%(path()),"r+")
	ERO_STR = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_STR.txt"%(path()),"r+")
	ERO_TMP = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_TMP.txt"%(path()),"r+")
	ERO_VAC1 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_VAC1.txt"%(path()),"r+")
	ERO_VAC2 = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_VAC2.txt"%(path()),"r+")

	def fileClose():
		fileList = [EL_PLT,EL_CAP1,EL_HVC,EL_MFC1,EL_STR,EL_TMP,EL_VAC1,EL_VAC2,ERI_PLT,ERI_CAP1,ERI_HVC,ERI_MFC1,ERI_STR,ERI_TMP,ERI_VAC1,ERI_VAC2,ERO_PLT,ERO_CAP1,ERO_HVC,ERO_MFC1,ERO_STR,ERO_TMP,ERO_VAC1,ERO_VAC2]
		for file in fileList:
			file.close()

	###
	###	Initialization specifications
	###
	###	[0]	:	operation enabled bit (in memory)
	###	[1]	:	initialization performed bit (in memory)
	###	[2]	:	initialization procedure (executable string in memory)
	### [3]	:	initialization error reported bit (non-volatile)
	###	[4]	:	error log (non-volatile)
	###
	initializations = {	"PLT":[par.op_plt,0,"timeKeeper_plt = t.time()\nimport DXE_PLT as plt",ERI_PLT,EL_PLT],
						"CAP1":[par.op_cap1,0,"timeKeeper_cap1 = t.time()\nimport DXE_LIB_CAP1_INI as INI_CAP1\nINI_CAP1.ini_cap1()\nimport DXE_LIB_CAP1_OP",ERI_CAP1,EL_CAP1],
						"HVC":[par.op_hvc,0,"timeKeeper_hvc = t.time()\nimport DXE_LIB_HVC_INI as INI_HVC\nINI_HVC.ini_hvc()\nimport DXE_LIB_HVC_OP",ERI_HVC,EL_HVC],
						"MFC1":[par.op_mfc1,0,"timeKeeper_mfc1 = t.time()\nimport DXE_LIB_MFC1_INI as INI_MFC1\nINI_MFC1.ini_mfc1()\nimport DXE_LIB_MFC1_OP",ERI_MFC1,EL_MFC1],
						"STR":[par.op_str,0,"timeKeeper_str = t.time()\nimport DXE_LIB_STR_INI as INI_STR\nINI_STR.ini_str()\nimport DXE_LIB_STR_OP",ERI_STR,EL_STR],
						"TMP":[par.op_tmp,0,"timeKeeper_tmp = t.time()\nimport DXE_LIB_TMP_INI as INI_TMP\nINI_TMP.ini_tmp()\nimport DXE_LIB_TMP_OP",ERI_TMP,EL_TMP],
						"VAC1":[par.op_vac1,0,"timeKeeper_vac1 = t.time()\nimport DXE_LIB_VAC1_INI as INI_VAC1\nINI_VAC1.ini_vac1()\nimport DXE_LIB_VAC1_OP",ERI_VAC1,EL_VAC1],
						"VAC2":[par.op_vac2,0,"timeKeeper_vac2 = t.time()\nimport DXE_LIB_VAC2_INI as INI_VAC2\nINI_VAC2.ini_vac2()\nimport DXE_LIB_VAC2_OP",ERI_VAC2,EL_VAC2], 	}

	###
	###	Perform initializations
	###
	for i in range(0,len(initializations)):
		curIni = initializations.keys()[i]
		if initializations[initializations.keys()[i]][0] == 1:
			maxAttempts = 5
			attempts = 0
			while (attempts < maxAttempts):

				try:
					exec(initializations[initializations.keys()[i]][2])

				except Exception as err:
					attempts = attempts + 1
					errBitStream = open("%s"%(initializations[initializations.keys()[i]][3].name),"r")
					errBit = errBitStream.read()
					errBitStream.close()
					errBit = errBit.strip(" ")
					errBit = errBit.strip("\n")
					errBit = errBit.strip(" ")
					errBit = errBit.strip("\n")
					if (errBit == ""):
						errBit = 0
					if (isinstance(errBit,basestring)):
						if (eval(errBit) == 1):
							errBit = 1
					if (errBit == 0):
						print "DAXSC:: ! ! Initialization of %s failed [[ t=%d ]]\n %d remaining initialization attempts of before reporting/logging error\nError: %s\n"%(curIni,t.time(),maxAttempts-attempts,err)
					if (attempts >= maxAttempts)&(errBit == 0):
						initializations[initializations.keys()[i]][3].close()
						initializations[initializations.keys()[i]][3] = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_%s.txt"%(path(),curIni),"w")
						errBit = 1
						initializations[initializations.keys()[i]][3].write("%d"%(errBit))
						initializations[initializations.keys()[i]][3].close()
						AudibleError()
						###
						### Email regarding initialization failure
						###
						subject = "Error"
						messageBody = " ! ! Initialization of %s failed with error %s, INTERVENTION REQUIRED"%(curIni,err)
						com.email(subject,messageBody)
						print "DAXSC:: ! ! Error reported [[ t=%s ]]\n"%(t.strftime("%H:%M:%S")) + messageBody
						###
						### Log error
						###
						if (err != ""):
							logging.getLogger('').handlers = []
							logging.basicConfig(level=logging.ERROR, filename='%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_%s.txt'%(path(),curIni), filemode='w')
							logging.exception(" ! ! ! ! TERMINATING ERROR during INITIALIZATION of %s at %s ! ! ! ! "%(curIni,t.strftime("%H:%M:%S %Y-%m-%d")))
					if (errBit == 0):
						t.sleep(3)
					if (errBit == 1):
						t.sleep(0.1)

				else:
					attempts = maxAttempts
					initializations[initializations.keys()[i]][1] = 1
					initializations[initializations.keys()[i]][3] = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_I_%s.txt"%(path(),curIni),"w")
					initializations[initializations.keys()[i]][3].close()

	###
	###	Assess state of initialization
	###
	opSum = 0
	initializedSum = 0
	for d in range(0,len(initializations)):
		opSum = opSum + initializations[initializations.keys()[d]][0]
		initializedSum = initializedSum + initializations[initializations.keys()[d]][1]

	#######################
	###					###
	###    OPERATION 	###
	###					###
	#######################
	while 1:
		
		if par.run == 1:

			###
			###	Operation Specifications
			###
			###	[0]	:	operation enabled bit (in memory)
			###	[1]	:	operation performed bit (in memory) [[ set to 1 if performed before opPeriod_* elapsed ]]
			###	[2]	:	operation procedure (executable string in memory)
			###	[3]	:	operation error reported bit (non-volatile)
			###	[4]	:	error log (non-volatile)
			###	[5]	:	operational minimum time (in memory)
			###	[6]	:	timeKeeper (in memory)
			###	[7]	:	initialization performed bit (in memory)
			###
			operations = {	"PLT":[par.op_plt,0,"null",ERO_PLT,EL_PLT,par.opPeriod_plt,"null",initializations["PLT"][1]],
							"CAP1":[par.op_cap1,0,"null",ERO_CAP1,EL_CAP1,par.opPeriod_cap1,"null",initializations["CAP1"][1]],
							"HVC":[par.op_hvc,0,"null",ERO_HVC,EL_HVC,par.opPeriod_hvc,"null",initializations["HVC"][1]],
							"MFC1":[par.op_mfc1,0,"null",ERO_MFC1,EL_MFC1,par.opPeriod_mfc1,"null",initializations["MFC1"][1]],
							"STR":[par.op_str,0,"null",ERO_STR,EL_STR,par.opPeriod_str,"null",initializations["STR"][1]],
							"TMP":[par.op_tmp,0,"null",ERO_TMP,EL_TMP,par.opPeriod_tmp,"null",initializations["TMP"][1]],
							"VAC1":[par.op_vac1,0,"null",ERO_VAC1,EL_VAC1,par.opPeriod_vac1,"null",initializations["VAC1"][1]],
							"VAC2":[par.op_vac2,0,"null",ERO_VAC2,EL_VAC2,par.opPeriod_vac2,"null",initializations["VAC2"][1]], 	}

			###
			### Slow Control routine
			###
			if ( (t.time()-timeKeeper_sc) > (par.routineTime-1) ):
				timeKeeper_sc = t.time()
				print "DAXSC:: Live [[ t=%d routineTime=%.2f ]]"%(t.time(),par.routineTime)

				###
				###	Update operations to be iterated through according to interactions enabled
				###
				if (par.op_plt	== 1):
					operations["PLT"] 	=	[par.op_plt,0,"plt.op_plt()",ERO_PLT,EL_PLT,par.opPeriod_plt,timeKeeper_plt,initializations["PLT"][1]]
				if (par.op_cap1 == 1):
					operations["CAP1"] 	=	[par.op_cap1,0,"DXE_LIB_CAP1_OP.op_cap1()",ERO_CAP1,EL_CAP1,par.opPeriod_cap1,timeKeeper_cap1,initializations["CAP1"][1]]
				if (par.op_hvc	== 1):
					operations["HVC"] 	=	[par.op_hvc,0,"DXE_LIB_HVC_OP.op_hvc()",ERO_HVC,EL_HVC,par.opPeriod_hvc,timeKeeper_hvc,initializations["HVC"][1]]
				if (par.op_mfc1	== 1):
					operations["MFC1"] 	=	[par.op_mfc1,0,"DXE_LIB_MFC1_OP.op_mfc1()",ERO_MFC1,EL_MFC1,par.opPeriod_mfc1,timeKeeper_mfc1,initializations["MFC1"][1]]
				if (par.op_str  == 1):
					operations["STR"] 	=	[par.op_str,0,"DXE_LIB_STR_OP.op_str()",ERO_STR,EL_STR,par.opPeriod_str,timeKeeper_str,initializations["STR"][1]]
				if (par.op_tmp  == 1):
					operations["TMP"] 	=	[par.op_tmp,0,"DXE_LIB_TMP_OP.op_tmp()",ERO_TMP,EL_TMP,par.opPeriod_tmp,timeKeeper_tmp,initializations["TMP"][1]]
				if (par.op_vac1	== 1):
					operations["VAC1"] 	=	[par.op_vac1,0,"DXE_LIB_VAC1_OP.op_vac1()",ERO_VAC1,EL_VAC1,par.opPeriod_vac1,timeKeeper_vac1,initializations["VAC1"][1]]
				if (par.op_vac2 == 1):
					operations["VAC2"] 	=	[par.op_vac2,0,"DXE_LIB_VAC2_OP.op_vac2()",ERO_VAC2,EL_VAC2,par.opPeriod_vac2,timeKeeper_vac2,initializations["VAC2"][1]]

				###
				###	Perform operations
				###
				for o in range(0,len(operations.keys())):
					curOp = operations.keys()[o]
					if (operations[operations.keys()[o]][0] == 1)&(operations[operations.keys()[o]][7] == 1):
						if ( (t.time()-operations[operations.keys()[o]][6]) < operations[operations.keys()[o]][5] ):
							operations[operations.keys()[o]][1] = 1
						if ( (t.time()-operations[operations.keys()[o]][6]) > operations[operations.keys()[o]][5] ):
							operations[operations.keys()[o]][6] = t.time()
							print "\top%d@t'=%f"%(o,(t.time()-timeKeeper_sc))
							maxAttempts = 5
							attempts = 0
							while (attempts < maxAttempts):

								try:
									exec(operations[operations.keys()[o]][2])

								except Exception as err:
									attempts = attempts + 1
									errBitStream = open("%s"%(operations[operations.keys()[o]][3].name),"r")
									errBit = errBitStream.read()
									errBitStream.close()
									errBit = errBit.strip(" ")
									errBit = errBit.strip("\n")
									errBit = errBit.strip(" ")
									errBit = errBit.strip("\n")
									if (errBit == ""):
										errBit = 0
									if (isinstance(errBit,basestring)):
										if (eval(errBit) == 1):
											errBit = 1
									if (errBit == 0):
										print "DAXSC:: ! ! Operation of %s failed [[ t=%d ]]\n %d remaining operation attempts of before reporting/logging error\nError: %s\n"%(curOp,t.time(),maxAttempts-attempts,err)
									if (attempts >= maxAttempts)&(errBit == 0):
										operations[operations.keys()[o]][3].close()
										operations[operations.keys()[o]][3] = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_%s.txt"%(path(),curOp),"w")
										errBit = 1
										operations[operations.keys()[o]][3].write("%d"%(errBit))
										operations[operations.keys()[o]][3].close()
										AudibleError()
										###
										### Email regarding initialization failure
										###
										subject = "Error"
										messageBody = " ! ! Operation of %s failed with error %s, INVESTIGATION SUGGESTED"%(curOp,err)
										com.email(subject,messageBody)
										print "DAXSC:: ! ! Error reported [[ t=%s ]]\n"%(t.strftime("%H:%M:%S")) + messageBody
										###
										### Log error
										###
										if (err != ""):
											logging.getLogger('').handlers = []
											logging.basicConfig(level=logging.ERROR, filename='%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRLOG_%s.txt'%(path(),curOp), filemode='w')
											logging.exception(" ! ! ! ! TERMINATING ERROR during OPERATION of %s at %s ! ! ! ! "%(curOp,t.strftime("%H:%M:%S %Y-%m-%d")))
									if (errBit == 0):
										t.sleep(3)
									if (errBit == 1):
										t.sleep(0.1)
									operations[operations.keys()[o]][1] = 0

								else:
									attempts = maxAttempts
									operations[operations.keys()[o]][1] = 1
									operations[operations.keys()[o]][3] = open("%s/DXE_OUTPUT/DXE_OUT_ERRLOG/DXE_OUT_ERRREP_O_%s.txt"%(path(),curOp),"w")
									operations[operations.keys()[o]][3].close()

				###
				###	Assess state of operations
				###
				###	NOTE: operation performed bit is set to 1 if operation was prompted but was not ready yet per opPeriod_* of sc.par
				###
				performedSum = 0
				for d in range(0,len(operations)):
					performedSum = performedSum + operations[operations.keys()[d]][1]

				###
				###	Perform actions based on state of Slow Control
				###
				if (initializedSum != opSum):
					db.db.close()
					fileClose()
					RS()
				if (performedSum != opSum):
					db.db.close()
					fileClose()
					RS()

		###
		### Refresh Slow Control parameters
		###
		t.sleep(1)
		par = reload(par)
