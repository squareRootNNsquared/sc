###
### DXE VACUUM MEASUREMENT 001, OPERATION (vac1 OP) [Device: MKS 972B DualMag Transducer]
###

### Import necessary packages and scripts ###
import DXE_SC as sc
import serial as ser
import time as t
import re

### VAC1 Operation module ###
def op_vac1():

    ###
    ### Create table in database for device
    ###
    ### Define Columns in table:
    ### 1   Time[s]         Time in seconds
    ### -   -               -
    ### 2   Error[]         Error message
    ### 3   Pressure1[Torr] On the order of vacuum pressure reading provided by VAC1
    VAC1 = sc.db.Table("VAC1","TimeUNITs DOUBLE,ErrorUNIT VARCHAR(45),PressureUNITtorr DOUBLE")

    ###
    ### Output to database
    ###
    ### Store device output as error or data accordingly
    ###
    ### IMPORTANT NOTE: There is currently a bug that requires the pressure to be querried twice
    ###                 It is likely that a smiliar issue will be had with the MFC
    ###
    import DXE_LIB_VAC1_INI as ini
    ignore = ini.subOp(3) ### This is the ignorance aforementioned
    press = ini.subOp(3)
    if isinstance(press, basestring):
        err = press
        press = 0
    else:
        err = ""
    VAC1.addData('''%f,"%s",%f'''%(t.time(),err,press))