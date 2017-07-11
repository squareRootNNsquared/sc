###
### DXE CAPACITANCE MEASUREMENT, INITIALIZATION (cap1 INI) [Device: Smartec Universal Transducer Interface Multifunction]
###

### Import necessary packages and scripts ###
import DXE_SC as sc
import serial as ser
import time as t

### Assign communication address to device, communicates via USB ###
com_cap1 = ser.Serial('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1001DAs-if00-port0')

### CAP1 Initialization module ###
def ini_cap1():

	com_cap1.write("@ %s"%(ser.CR)) ### Initialize communication with device
	t.sleep(sc.par.holdTime)
	com_cap1.write("1 %s"%(ser.CR)) ### Fast/Slow mode
	t.sleep(sc.par.holdTime)