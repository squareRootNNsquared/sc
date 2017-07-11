###
### DXE HVC, INITIALIZE (INI) [Device: SPS PS365m Power Supply + other(s) similar]
###

###	Import necessary packages and scripts ###
import DXE_SC as sc
import time
import serial as ser

### Assign communication with power supplies a port on serial multiplexer (sm) ###
if (sc.par.hvc.onPos == 1):
	com_hvcPos = sc.com_sm.sm5
	com_hvcPos.timeout	=	sc.par.tO_hvc
if (sc.par.hvc.onNeg == 1):
	com_hvcNeg = sc.com_sm.sm7
	com_hvcNeg.timeout	=	sc.par.tO_hvc

### HVC initialization module ###
def ini_hvc():

	###	Initialize Positive unit ###
	if (sc.par.hvc.onPos == 1):
		com_hvcPos.write("SMOD 0 %s"%(ser.CR)) ### Enable rear panel control, NOTE: value=0 is needed due to a bug (?)
		com_hvcPos.write("HVON %s" %(ser.CR)) ### High Voltage ON
		com_hvcPos.write("TMOD 1 %s" %(ser.CR)) ### Set Trip Mode to automatic clear setting (manual unclear, may reqire 0)

	###	Initialize Negative unit ###
	if (sc.par.hvc.onNeg == 1):
		com_hvcNeg.write("SMOD 0 %s"%(ser.CR)) ### Enable rear panel control, NOTE: value=0 is needed due to a bug (?) 
		com_hvcNeg.write("HVON %s" %(ser.CR)) ### High Voltage ON
		com_hvcNeg.write("TMOD 1 %s" %(ser.CR)) ### Set Trip Mode to automatic clear setting (manual unclear, may reqire 0)
	