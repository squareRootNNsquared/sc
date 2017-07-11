###
### DXE STR, OPERATION (OP) [Devices: Omega DPiS8 Strain Gauge Monitor, Omega LCM101-50 Strain Gauge]  
###

### Import necessary packages and scripts
import DXE_SC as sc
import socket
import DXE_LIB_STR_INI as ini
import time as t

### STR Operation module
def op_str():

	###
	### Colect Data
	###
	ini.com_str1.send("*X01\r")
	str1 = ini.com_str1.recv(16)
	ini.com_str2.send("*X01\r")
	str2 = ini.com_str2.recv(16)

	###
	### Process Data
	###
	str1 = eval(str1)
	str2 = eval(str2)

	###
	### Output to database
	###
	ini.STR.addData('''%f,%f,%f'''%(t.time(),str1,str2))