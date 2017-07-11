###
### DXE SERIAL MULTIPLEXER, INITIALIZATION (sm INI) [Device: Startech ICUSB2321fF Serial Multiplexer]
###

###	Import necessary packages and scripts ###
import serial as ser

### Assign all serial ports of serial multiplexer an addressed name ###
### Note: Interpret sm[NUMBER] as communication with serial multiplexer on port [NUMBER]
for i in range(1,17):
    exec("sm%d = ser.Serial('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_ST1832%d-if00-port0')"%(i,i+48))