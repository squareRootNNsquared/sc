###
### DXE VAC2, OPERATION (OP) [Devices: Omega CN16DPT-305-C24-EIP Temperature and Process Controller, Omega MMA100V10P5C2T3A5CE Pressure Gauge]  
###

### Import necessary packages and scripts
import DXE_SC as sc
import socket
import DXE_LIB_VAC2_INI as ini
import time as t

### VAC2 Operation module
def op_vac2():

	###
	### Colect Data
	###
	ini.com_vac2.send("*X01\r")
	vac2 = ini.com_vac2.recv(16)

	###
	### Process Data
	###
	vac2 = eval(vac2)

	###
	### Output to database
	###
	ini.VAC2.addData('''%f,%f'''%(t.time(),vac2))