###
### DXE SC PARAMETERS (PAR)
###
### NOTE1: The entities of DXE_LIB_SC_PAR (or that with "sc" in name referenced from outside of this file) are Slow Control program global and as such may be used in many locations
###
### NOTE2: All devices are listed in any area where device references are present. Where a device has no code pertaining to such an area, a placeholder is. Devices are alphabetized by SC short name.
###

###	Import necessary packages and scripts ###
import time

### Import library parameter files associated with each computer-interfaced device ###
import DXE_LIB_CAP1_PAR	as	cap1
import DXE_LIB_HVC_PAR 	as	hvc
import DXE_LIB_MFC1_PAR	as	mfc1
#							sm
#							str
#							tmp
import DXE_LIB_VAC1_PAR	as	vac1
#							vac2

###
### ENABLE/DISABLE SLOW CONTROL ROUTINE
###
### NOTE: 1 enables, 0 disables; Must stop program in order to turn a devices interfacing on
###
run = 1

###
### ENABLE/DISABLE INTERFACING OF DEVICES/FEATURES
###
### NOTE: 1 enables, 0 disables; Must stop program in order to turn a devices interfacing on
###

### Devices ###
op_cap1	= 1
op_hvc	= 1
op_mfc1	= 0
op_sm	= 1
op_str  = 0
op_tmp  = 0
op_vac1	= 0
op_vac2 = 0

### Features ###
op_plt = 1

###
###	SET PARAMETERS
###

###
### Program Upon-Fault Mailing List
###
###	Text messages may be sent via email. To do so,
###	in place of the recipient, store the number 
###	with _L appended such that "L" is the letter
###	designated by this program to correspond to
### the format of the SMS Gateway of the provider.
###
###	Example: recipient = "7894561230_A"
###
###	Note: SMS Gateway numbers are 10 digits, negl-
###			ecting the common prepended "1", "+1"
###
###	AT&T: 		A [[Gateway confirmed, format OK]]
###	Metro PCS:	M [[UNTESTED]]
###	Sprint:		S [[UNTESTED]]
###	T-Mobile:	T [[UNTESTED]]
### Verizon:	V [[Gateway confirmed, potential format issues]]
###	Virgin:		I [[Gateway confirmed, format OK]]
###
emailList = []

###
###	Universal Parameters
###
### UNIVERSAL HOLD TIME [SECONDS]
holdTime		= 0.01
### UNIVERSAL OPERAION FREQUENCY [Hz]
frequency	= holdTime**-1
### MINIMUM SLOW CONTROL ROUTINE TIME [SECONDS] (If routine is finished early, program will do nothing until this value of time has elapsed)
routineTime = 2

###
###	Plot parameters
###
### Plot time start ( [HOURS] prior to current time)
plotTimeStart	= 0.05
### Plot time end ( [HOURS] prior to current time)
plotTimeEnd		= 0
### Plot period ( [MINUTES]  between generation/refresh of plot)
opPeriod_plt		= 0.125
### Plot time window (plot time width) ( [SECONDS]  time range during which plot switching occurs)###
plotTimeWidth = 5

###
### Device Interaction Frequency Parameters ( [SECONDS] of MINIMUM time between operations)
###
opPeriod_cap1 = 0.35
opPeriod_hvc  = 0.4
opPeriod_mfc1 = 0.2
#		 sm
opPeriod_str  = 3
opPeriod_tmp  = 1
opPeriod_vac1 = 0.2
opPeriod_vac2 = 3

###
###	Device Serial Port Timeout Parameters
###
#  cap1
tO_hvc  = 1
tO_mfc1 = 1
#  sm
#  str
#  tmp
tO_vac1 = 1
#  vac2

###
### Perform time conversion calculations
###
plotTimeStart = (time.time())-(plotTimeStart*60*60)
plotTimeEnd = (time.time())-(plotTimeEnd*60*60)
opPeriod_plt = opPeriod_plt*60
if routineTime <= 1:	### Adjust routineTime value to minimum if is at or below.
	routineTime = 1.00001 

### Refresh parameters stored in interfaced-device specific files ###
cap1	= reload(cap1)
hvc		= reload(hvc)
mfc1	= reload(mfc1)
#				 sm
#				 str
#				 tmp
vac1	= reload(vac1)
#				 vac2
