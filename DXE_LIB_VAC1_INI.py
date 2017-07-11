###
### DXE VACUUM MEASUREMENT 001, INITIALIZATION (vac1 INI) [Device: MKS 972B DualMag Transducer]
###
### NOTE: Max operational frequency for data fetching is ~25Hz (with RSD = "ON"), timeout need be set to the trippled reciprocal of this
###

### Import necessary packages and scripts ###
import DXE_SC as sc
import serial as ser
import time as t
import re

### Assign communication with device a port on serial multiplexer (sm) ###
com_vac1 = ser.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0', 9600, timeout=0.12)
#com_vac1 = sc.com_sm.sm5

### Define Sub-Operation function, input is a number corresponding to sublist of interactionSpecification ###
def subOp(I):

    ### Format interaction ###
    interactionType = sc.par.vac1.interactionSpecification[I][0]
    interaction = sc.par.vac1.interactionSpecification[I][1]
    interactionAttribute = sc.par.vac1.interactionSpecification[I][2]
    interactionFormatted_1 = "@" + "%s"%(sc.par.vac1.RS485Address) + interaction + interactionType + interactionAttribute + ";"
    interactionFormatted_2 = interactionFormatted_1 + "FF" ### + checksum(interactionFormatted_1) ### mfc1 requires checksum, vac1 does not
    interactionFormatted_3 = interactionFormatted_2 ### "@@" + ... removed; mfc1 uses three "@" symbols

    ### Interact ###
    com_vac1.write('%s'%(interactionFormatted_3))
    if interactionType == "?":
        output = com_vac1.readline()
        t.sleep(sc.par.holdTime)
        output_original = output
    if interactionType == "!":
        ignore1 = com_vac1.readline() ### NOTE: Ignore responses if not from query
        output = "COMMAND"
        output_original = output
    if ("!" in interactionType) == False:
        if ("?" in interactionType) == False:
            ignore2 = com_vac1.readline() ### NOTE: Ignore responses if not from query or command
            output = "Interaction type improperly specified."
            output_original = output
    com_vac1.flushInput()
    com_vac1.flushOutput()
    com_vac1.flush()

    ### Check for Error (NAK) or Acknowledgement (ACK) ###
    ### Note: Command responses are ignored
    if ("ACK" in output) == False:
        if ("NAK" in output) == False:
            if output != "COMMAND":
                output = "Fatal error, check commuication interface."

    ### Process and store reply in "output", Flush buffer (ACK) ###
    if ("ACK" in output) == True:
        output = output.split(';')  
        output = output[0]
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

    ### Process and store reply in "output", Flush buffer (NAK) ###
    if ("NAK" in output_original) == True:
        output = output.split(';')
        output = output[0]
        output = output.strip("@") ### Note: "strip" => string must be at beginning or end to be removed
        output = output.strip("@")
        output = output.strip("@")
        output = output[3:]
        output = output.replace("NAK","")
        output = str(output)
        output = "Error Code Generated: " + output

    return output

### VAC1 initialization module ###
def ini_vac1():
	
    subOp(0)
    t.sleep(sc.par.holdTime)
    subOp(1)
    t.sleep(sc.par.holdTime)
    subOp(2)
    t.sleep(sc.par.holdTime)