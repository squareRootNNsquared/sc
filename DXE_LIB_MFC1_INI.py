###
### DXE MASS FLOW CONTROLLER 001, INITIALIZATION (mfc1 INI) [Device: MKS GM50A Mass Flow Controller]
###
### NOTE1: Device requires THIRTY MINUTES of "warm-up" prior to operation.
###
### NOTE2: "For optimum control performance, the user can (should) specify the inlet pressure
### to the device through the Ethernet User Interface"
###
### NOTE3: Max operational frequency for data fetching is ~250Hz, timeout set to the trippled reciprocal of the max of vac1
###
### NOTE4: Timeout need be set to roughly triple that required for repeated commands to be successfully interpreted via probook 4320s/ubuntu/ipy notebook, =0.12s
###
### NOTE5: If available, RSD setting may help the receiving of data if information received appears incomplete
###
### NOTE6: User Range of flow is 20000 sccm
###

### Import necessary packages and scripts ###
import DXE_SC as sc
import serial as ser
import time as t
import re

### Assign communication with device a port on serial multiplexer (sm) ###
com_mfc1 = ser.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0', 9600, timeout=0.2)

### Define checksum calculating function ###
def checksum(inputString):
    stringSumDec = 0
    for i in range(0,len(inputString)):
        stringSumDec += ord("%s"%(inputString[i]))
    stringSumHex = hex(stringSumDec)
    checkSum = str(stringSumHex)
    checkSum = checkSum[-2:]
    checkSum = checkSum.upper()
    return checkSum

### Define Sub-Operation function, input is a number corresponding to sublist of interactionSpecification ###
def subOp(I):

    ### Format interaction ###
    interactionType = sc.par.mfc1.interactionSpecification[I][0]
    interaction = sc.par.mfc1.interactionSpecification[I][1]
    interactionAttribute = sc.par.mfc1.interactionSpecification[I][2]
    interactionFormatted_1 = "@" + "%s"%(sc.par.mfc1.RS485Address) + interaction + interactionType + interactionAttribute + ";"
    interactionFormatted_2 = interactionFormatted_1 + checksum(interactionFormatted_1)
    interactionFormatted_3 = "@@" + interactionFormatted_2

    ### Interact ###
    com_mfc1.write('%s'%(interactionFormatted_3))
    if interactionType == "?":
        output = com_mfc1.readline()
        t.sleep(sc.par.holdTime)
        output_original = output
    if interactionType == "!":
        output = "COMMAND"
        output_original = output
    if ("!" in interactionType) == False:
        if ("?" in interactionType) == False:
            output = "Interaction type improperly specified."
            output_original = output

    ### Check for Error (NAK) or Acknowledgement (ACK) ###
    ### Note: Command responses are ignored
    if ("ACK" in output) == False:
        if ("NAK" in output) == False:
            if output != "COMMAND":
                output = "Fatal error, check commuication interface."
                output_original = output
                com_mfc1.flushInput()
            
    ### Process and store reply in "output", Flush buffer (ACK) ###
    if ("ACK" in output) == True:
        output = output.split(';')
        output = output[0]
        output = output[2:]
        output = output.strip("@") ### Note: "strip" => string must be at beginning or end to be removed
        output = output.strip("@")
        output = output.strip("@")
        output = output[3:]
        output = output.replace("ACK","")
        if output.find("E") != -1: ### If there's an E:
            if not re.search('[a-zA-Z]', output.replace("E","")): ### If there are no letters with E removed
                output = output.replace("E","*10**")
        if not re.search('[a-zA-Z]', output): ### If there are no letters
            if ("." in output) == True: ### If value is decimal (output is a manipulatable number) Note: requires S/N has no "."
                output = eval(output)
        com_mfc1.flushInput()

    ### Process and store reply in "output", Flush buffer (NAK) ###
    if ("NAK" in output_original) == True:
        output = output.split(';')
        output = output[0]
        output = output[2:]
        output = output.strip("@") ### Note: "strip" => string must be at beginning or end to be removed
        output = output.strip("@")
        output = output.strip("@")
        output = output[3:]
        output = output.replace("NAK","")
        output = str(output)
        output = "Error Code Generated: " + output
        com_mfc1.flushInput()
    
    return output

### MFC1 Initialization module ###
def ini_mfc1():

    subOp(0)    #   Wink on
    t.sleep(1)
    subOp(1)    #   Wink off
    t.sleep(0.1)
    subOp(3)    #   Calibration mode
    t.sleep(0.1)
    subOp(4)    #   Set gas to Xe
    t.sleep(0.1)
    subOp(2)    #   Run Mode
    t.sleep(0.1)
