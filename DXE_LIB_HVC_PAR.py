###
### DXE HVC, PARAMETERS (PAR) [Device: SPS PS365m Power Supply + other(s) similar]
###

###
###	SET PARAMETERS
###
###	NOTE: onPos and onNeg are bits determining if the corresponding positive or negative unit's code is executed
###

###	Positive Unit ###
onPos = 0
hvcPos_vSet = 1337.0
hvcPos_vLimit = 4500.0
hvcPos_iLimit = 0.0007

###	Negative Unit ###
onNeg = 1
hvcNeg_vSet = -1337.0
hvcNeg_vLimit = -6000.0
hvcNeg_iLimit = -0.0005
