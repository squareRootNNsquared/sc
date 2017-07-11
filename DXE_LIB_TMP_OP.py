###
### DXE TMP, OPERATION (OP) [Devices: Omega CN16DPT-305-C24-EIP Temperature and Process Controller, Omega MMA100V10P5C2T3A5CE Pressure Gauge]  
###

### Import necessary packages and scripts
import DXE_SC as sc
import socket
import DXE_LIB_TMP_INI as ini
import time as t

### TMP Operation module
def op_tmp():

	###
	### Colect Data
	###
	ini.com_tmp.send("input? A\n")
	tmpA = ini.com_tmp.recv(16)
	t.sleep(0.1)
	#ini.com_tmp.send("input? B\n")		### No thermistor connected at the moment!
	#tmpB = ini.com_tmp.recv(16)
	tmpB = "69"

	###
	### Process Data
	###
	tmpA = eval(tmpA)
	tmpB = eval(tmpB)

	###
	### Output to database
	###
	ini.TMP.addData('''%f,%f,%f'''%(t.time(),tmpA,tmpB))