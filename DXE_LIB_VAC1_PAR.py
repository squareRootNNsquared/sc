###
### DXE VACUUM MEASUREMENT 001, PARAMETERS (vac1 PAR) [Device: MKS 972B DualMag Transducer]
###

###
### Define interaction with device
### 

### Define RS485 command-coupled address ###
RS485Address = 253

###
### Define ineraction type and details, Format interaction type and details
###
### Note: Each sublist contains following ordered list: ["interactionType","interaction","interactionAttribute"]
###		interactionType: "!": command or "?": query
###		interaction: command or query symbol, see documentation, 
###		interactionAttribute: specification relevant to commands, not applicable in a query
###
interactionSpecification = [["!","GT","AIR"],["!","UT","VAC1"],["!","RSD","ON"],["?","PR4",""],["!","RSD","OFF"]]
###									0 				1					2 				3 				4 
for i in range(0, len(interactionSpecification)):
    if interactionSpecification[i][0] == "?":
        interactionSpecification[i][2] = ""
    
###
### Short List of Commands::
###
### PR1 - PR5 : Pressure readings, 4 = combined sensors 4 sigfig
###