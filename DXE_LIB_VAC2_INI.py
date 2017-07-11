###
### DXE VAC2, INITIALIZE (INI) [Devices: Omega CN16DPT-305-C24-EIP Temperature and Process Controller, Omega MMA100V10P5C2T3A5CE Pressure Gauge]  
###

### Import necessary packages and scripts
import DXE_SC as sc
import socket

###
### Initialize connectivity to device
###

### Define "socket" instance with appropriate parameters
com_vac2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
### Establish connection to device; ("address", "Local Port" setting via "Serial" tab)
com_vac2.connect(("dax-vac2.physics.ucdavis.edu",2001))

###
### Create table in database for device
###

### Define Columns in table:
### 1   Time[s]         Time in seconds
### -   -               -
### 2   Pressure2[kpa]	On the order of atmospheric pressure reading provided by VAC2
VAC2 = sc.db.Table("VAC2","TimeUNITs DOUBLE,Pressure2UNITkpa DOUBLE")

### VAC2 Initialization module
def ini_vac2():
	lambda null:none