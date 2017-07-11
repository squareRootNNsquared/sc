###
### DXE MASS FLOW CONTROLLER 001, OPERATION (mfc1 OP) [Device: MKS GM50A Mass Flow Controller]
###

### Import necessary packages and scripts ###
import DXE_SC as sc
import DXE_LIB_MFC1_INI as ini
import re
import time as t

### MFC1 Operation module ###
def op_mfc1():

    ###
    ### Create table in database for device
    ###
    ### Define Columns in table:
    ### 1   Time[s]         Time in seconds
    ### -   -               -
    ### 2   Error[]         Error message
    ### 3    
    MFC1 = sc.db.Table("MFC1","TimeUNITs DOUBLE,ErrorUNIT VARCHAR(45),StatusUNIT VARCHAR(45),SetFlowUNITsccm DOUBLE,FlowUNITsccm DOUBLE")

    ### Gather various data and store in variables, overwriting error with last error message derived from interaction with device
    err = ""

    flow =  ini.subOp(7)
    if isinstance(flow, basestring):
        err = flow
        flow = 0
  

    flowSet =  ini.subOp(6)
    if isinstance(flowSet, basestring):
        err = flowSet
        flowSet = 0

    status = ini.subOp(8)
    if status != "O":
        ini.subOp(9)

    ###
    ### Output to database
    ###
    MFC1.addData('''%f,"%s","%s",%f,%f'''%(t.time(),err,status,flowSet,flow))