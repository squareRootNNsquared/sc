###
### DXE MASS FLOW CONTROLLER 001, PARAMETERS (mfc1 PAR) [Device: MKS GM50A Mass Flow Controller]
###

###
### Define interaction with device
### 

### Define RS485 command-coupled address ###
RS485Address = 252

###
### Define ineraction type and details, Format interaction type and details
###
### Note: Each sublist contains following ordered list: ["interactionType","interaction","interactionAttribute"]
###		interactionType: "!": command or "?": query
###		interaction: command or query symbol, see documentation, 
###		interactionAttribute: specification relevant to commands, not applicable in a query
###

###
### Set flow rate
###
### NOTE: Range per documentation [28000,6001]
###
flowSet = 6500

interactionSpecification = [["!","WK","ON"],["!","WK","OFF"],["!","OM","RUN_MODE"],["!","OM","CAL_MODE"],["!","PG","6"],["!","S","%f"%(flowSet)],["?","S",""],["?","FX",""],["?","T",""],["!","SR",""]]
for i in range(0, len(interactionSpecification)):
    if interactionSpecification[i][0] == "?":
        interactionSpecification[i][2] = ""