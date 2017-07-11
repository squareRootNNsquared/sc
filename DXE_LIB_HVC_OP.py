###
### DXE HVC, OPERATION (OP) [Device: SPS PS365m Power Supply + other(s) similar]
###

###	Import necessary packages and scripts ###
import DXE_SC as sc
import DXE_LIB_HVC_INI as ini
import time as t
import os
import sys
import serial as ser

def path():	###	Returns current directory in string format
	return os.path.dirname(os.path.realpath(sys.argv[0]))

### DXE_HVC operation module ###
def op_hvc():

	###
	###	Create table in database for device
	###
	###	Define Columns in table:
	###	1	Time[s]				Time in seconds
	###	-	-					-
	###	2	Pos_Error[]			Positive unit Error Log
	###	3	Pos_vOut[V]			Positive unit voltage output, volts
	###	4	Pos_vSet[V]			Positive unit voltage set point, volts
	###	5	Pos_vLimit[V]		Positive unit voltage limit, volts
	###	6	Pos_iOut[A]			Positive unit current output, amps*10^6
	###	7	Pos_iLimit[A]		Positive unit current limit, amps*10^6
	###	-	-					-
	###	8	Neg_Error[]			Negative unit Error Log
	###	9	Neg_vOut[V]			Negative unit voltage output, volts
	###	10	Neg_vSet[V]			Negative unit voltage set point, volts
	###	11	Neg_vLimit[V]		Negative unit voltage limit, volts
	###	12	Neg_iOut[A]			Negative unit current output, amps*10^6
	###	13	Neg_iLimit[A]		Negative unit current limit, amps*10^6
	HVC = sc.db.Table("HVC","TimeUNITs DOUBLE,Pos_ErrorUNIT VARCHAR(45),Pos_vOutUNITv DOUBLE,Pos_vSetUNITv DOUBLE,Pos_vLimitUNITv DOUBLE,Pos_iOutUNITa DOUBLE,Pos_iLimitUNITa DOUBLE,Neg_ErrorUNIT VARCHAR(45),Neg_vOutUNITv DOUBLE,Neg_vSetUNITv DOUBLE,Neg_vLimitUNITv DOUBLE,Neg_iOutUNITa DOUBLE,Neg_iLimitUNITa DOUBLE")

	###
	###	Initialize all values to be input into database to null
	###
	pos_err = "0"
	pos_vOut = 0
	pos_vSet = 0
	pos_vLimit = 0
	pos_iOut = 0
	pos_iLimit = 0
	neg_err = "0"
	neg_vOut = 0
	neg_vSet = 0
	neg_vLimit = 0
	neg_iOut = 0
	neg_iLimit = 0

	###
	###	Positive Unit High Voltage Power Supply Operation SubModule
	###
	if (sc.par.hvc.onPos == 1):

		### Apply current and voltage settings ###
		ini.com_hvcPos.write("VSET %f %s" %(sc.par.hvc.hvcPos_vSet,ser.CR)) ### Apply voltate setting
		ini.com_hvcPos.write("VLIM %f %s" %(sc.par.hvc.hvcPos_vLimit,ser.CR)) ### Apply voltage limit
		ini.com_hvcPos.write("ILIM %f %s" %(sc.par.hvc.hvcPos_iLimit,ser.CR)) ### Apply current limit
		pos_vSet = sc.par.hvc.hvcPos_vSet
		pos_vLimit = sc.par.hvc.hvcPos_vLimit
		pos_iLimit = sc.par.hvc.hvcPos_iLimit
		pos_vSet = 0
		pos_vLimit = 0
		pos_iLimit = 0

		###	Label HVC unit currently operating
		hvc_unitType = "Positive"

		### Read device for an error message, log, clear, continue ###
		ini.com_hvcPos.write("LERR? %s" %(ser.CR))
		t.sleep(sc.par.holdTime)
		hvc_errorMessage = ini.com_hvcPos.readline()	### zero by default, in a no-error state
		hvc_errorMessage = float(hvc_errorMessage)
		pos_err = ""
		if (hvc_errorMessage > 0) :
			pos_err = "Error Code: %f\t%s\tUnit: %s\n" %(hvc_errorMessage,t.strftime('%Y-%m-%d:%H:%M:%S'),hvc_unitType)
			ini.com_hvcPos.write("*CLS %s" %(ser.CR))
			hvc_errorMessage = 0
			t.sleep(sc.par.holdTime)
		pos_err = "0"

		###	READ parameters	###
		ini.com_hvcPos.write("VOUT? %s" %(ser.CR) )			###	Request parameter over bus
		t.sleep(sc.par.holdTime)							###	Wait for device to operate
		pos_vOut = ini.com_hvcPos.readline()				###	Read device response
		pos_vOut = eval(pos_vOut.replace("E","*10**"))		###	Convert: %s->%f
		ini.com_hvcPos.write("IOUT? %s" %(ser.CR) )
		t.sleep(sc.par.holdTime)
		pos_iOut = ini.com_hvcPos.readline()
		pos_iOut = eval(pos_iOut.replace("E","*10**"))
		pos_vOut = 0
		pos_iOut = 0

	###
	###	Negative Unit High Voltage Power Supply Operation SubModule
	###
	if (sc.par.hvc.onNeg == 1):

		### Apply current and voltage settings ###
		ini.com_hvcNeg.write("VSET %f %s" %(sc.par.hvc.hvcNeg_vSet,ser.CR)) ### Apply voltate setting
		ini.com_hvcNeg.write("VLIM %f %s" %(sc.par.hvc.hvcNeg_vLimit,ser.CR)) ### Apply voltage limit
		ini.com_hvcNeg.write("ILIM %f %s" %(sc.par.hvc.hvcNeg_iLimit,ser.CR)) ### Apply current limit
		neg_vSet = sc.par.hvc.hvcNeg_vSet
		neg_vLimit = sc.par.hvc.hvcNeg_vLimit
		neg_iLimit = sc.par.hvc.hvcNeg_iLimit

		###	Label HVC unit currently operating
		hvc_unitType = "Negative"

		### Read device for an error message, log, clear, continue ###
		ini.com_hvcNeg.write("LERR? %s" %(ser.CR))
		t.sleep(sc.par.holdTime)
		hvc_errorMessage = ini.com_hvcNeg.readline()	### zero by default, in a no-error state
		hvc_errorMessage = float(hvc_errorMessage)
		neg_err = ""
		if (hvc_errorMessage > 0) :
			neg_err = "Error Code: %f\t%s\tUnit: %s\n" %(hvc_errorMessage,t.strftime('%Y-%m-%d:%H:%M:%S'),hvc_unitType)
			ini.com_hvcNeg.write("*CLS %s" %(ser.CR))
			hvc_errorMessage = 0
			t.sleep(sc.par.holdTime)

		###	READ parameters	###
		ini.com_hvcNeg.write("VOUT? %s" %(ser.CR) )			###	Request parameter over bus
		t.sleep(sc.par.holdTime)							###	Wait for device to operate
		neg_vOut = ini.com_hvcNeg.readline()				###	Read device response
		neg_vOut = eval(neg_vOut.replace("E","*10**"))		###	Convert: %s->%f
		neg_vOut = float(neg_vOut)
		ini.com_hvcNeg.write("IOUT? %s" %(ser.CR) )
		t.sleep(sc.par.holdTime)
		neg_iOut = ini.com_hvcNeg.readline()
		neg_iOut = eval(neg_iOut.replace("E","*10**"))

	###
	### Output to database
	###
	HVC.addData('''%f,"%s",%f,%f,%f,%f,%f,"%s",%f,%f,%f,%f,%f'''%(t.time(),pos_err,pos_vOut,pos_vSet,pos_vLimit,pos_iOut*10**6,pos_iLimit*10**6,neg_err,neg_vOut,neg_vSet,neg_vLimit,neg_iOut*10**6,neg_iLimit*10**6))
	###
	###	Columns in table:
	###	1	Time[s]				Time in seconds
	###	-	-					-
	###	2	Pos_Error[]			Positive unit Error Log
	###	3	Pos_vOut[V]			Positive unit voltage output, volts
	###	4	Pos_vSet[V]			Positive unit voltage set point, volts
	###	5	Pos_vLimit[V]		Positive unit voltage limit, volts
	###	6	Pos_iOut[A]			Positive unit current output, amps*10^6
	###	7	Pos_iLimit[A]		Positive unit current limit, amps*10^6
	###	-	-					-
	###	8	Neg_Error[]			Negative unit Error Log
	###	9	Neg_vOut[V]			Negative unit voltage output, volts
	###	10	Neg_vSet[V]			Negative unit voltage set point, volts
	###	11	Neg_vLimit[V]		Negative unit voltage limit, volts
	###	12	Neg_iOut[A]			Negative unit current output, amps*10^6
	###	13	Neg_iLimit[A]		Negative unit current limit, amps*10^6