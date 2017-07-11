###
### DXE CAPACITANCE MEASUREMENT, OPERATION (cap1 OP) [Device: Smartec Universal Transducer Interface Multifunction]
###

### Import necessary packages and scripts ###
import DXE_SC as sc
import DXE_LIB_CAP1_INI as ini
import serial as ser
import time as t

### CAP1 Operation module ###
def op_cap1():


	###
	###	Create table in database for device
	###
	###	Define Columns in table:
	###	1	Time[s]				Time in seconds
	###	-	-					-
	###	2	Capacitance[pF]		Measured capacitance
	CAP1 = sc.db.Table("CAP1","TimeUNITs DOUBLE,CapacitanceUNITpf DOUBLE")

	### Collect and Organize Data ###
	ini.com_cap1.write("m %s"%(ser.CR)) ### Single measurement
	t.sleep(sc.par.holdTime)
	allOutput = ini.com_cap1.readline() ### Single measurement output
	outputList = allOutput.split()
	outputList[0] = float(int(outputList[0],16))
	T_BA = outputList[0]
	outputList[1] = float(int(outputList[1],16))
	T_CA = outputList[1]
	outputList[2] = float(int(outputList[2],16))
	T_DA = outputList[2]

	### Reference Capacitor Value ###
	capRef = 2.0#pF

	### Calculate
	C_CA__divBy__C_DA = float((T_CA-T_BA)/(T_DA-T_BA)) ### Compute Ratio of C and D connections
	cap1UTI = C_CA__divBy__C_DA*capRef ### cap1 (C_CA) per UTI measurement =~ T_CA/T_DA = C_CA/C_DA, (C_CA/C_DA) * capRef = C_CA 
	cap1 = cap1UTI

	###
	### Output to database
	###
	CAP1.addData("%f,%f"%(t.time(),cap1))
	###
	###	Columns in table:
	###	1	Time[s]				Time in seconds
	###	-	-					-
	###	2	Capacitance[pF]		Measured capacitance