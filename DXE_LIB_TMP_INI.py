###
### DXE TMP, INITIALIZE (INI) [Device: Cryogenic Control Systems Model Crycon 26 Temperature Controller]  
###

### Import necessary packages and scripts
import DXE_SC as sc
import socket

###
### Initialize connectivity to device
###
### Define "socket" instance with appropriate parameters
com_tmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
### Establish connection to device; ("address", "Local Port" setting via "Serial" tab)
com_tmp.connect(("169.237.42.6",5000))

###
### Create table in database for device
###

### Define Columns in table:
### 1   Time[s]         	Time in seconds
### -   -               	-
### 2   TemperatureA[K]		Cryocon 26 temperature measurement of Input A
### 3   TemperatureB[K]		Cryocon 26 temperature measurement of Input B
TMP = sc.db.Table("TMP","TimeUNITs DOUBLE,TemperatureAUNITK DOUBLE,TemperatureBUNITK DOUBLE")

### TMP Initialization module
def ini_tmp():
	lambda null:none