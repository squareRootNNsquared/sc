###
### DXE STR, INITIALIZE (INI) [Devices: Omega DPiS8 Strain Gauge Monitor x 2, Omega LCM101-50 Strain Gauge x 2]  
###

### Import necessary packages and scripts
import DXE_SC as sc
import socket

###
### Initialize connectivity to devices
###

### str1
### Define "socket" instance with appropriate parameters
com_str1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#### Establish connection to device; ("address", "Local Port" setting via "Serial" tab)
com_str1.connect(("",1))

### str2
### Define "socket" instance with appropriate parameters
com_str2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
### Establish connection to device; ("address", "Local Port" setting via "Serial" tab)
com_str2.connect(("1",2))

###
### Create table in database for device
###

### Define Columns in table:
### 1   Time[s]         Time in seconds
### -   -               -
### 2   Strain1[kg]		Strain on strain gauge 1, STR1
### 3   Strain2[kg]		Strain on strain gauge 2, STR2
STR = sc.db.Table("STR","TimeUNITs DOUBLE,Strain1UNITkg DOUBLE,Strain2UNITkg DOUBLE")

### STR Initialization module
def ini_str():
	lambda null:none
