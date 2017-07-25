NOTE_08JE2016:
May need to execute
chmod +x ../DXE_SC.py
in terminal in order to allow Slow Control (SC) script to perform an os function.

Davis Xenon Characterization Project Slow Control Program
Author(s):	Nathaniel Nunez
Intended Platform:	Ubuntu 14.04 LTS
Programming Language:	python 2.7 (written in 2.7.9)
Required python packages:	pyserial, matplotlib, pylab, numpy, python-mysqldb

DXE_SC.py is the center of this Slow Control program that references library files in the program's root folder. The program is intended to be continuously ran, and while doing so continuously collects data pertaining to the instruments involved.

DXE_PLT.py is a program that generates plots of the data collected by DXE_SC.py. Files beginning with DXE_LIB are not intended to be executed directly.

Per device to be operated and monitored, three library (LIB) files are implemented. An initialization file ending in the abbreviation INI, an operation file ending in the abbreviation OP, and a parameter file ending in the abbreviation PAR. Initialization is typically only ran once (infrequently updated), to store device relevant information in memory. Operation is ran continuously in conjunction with the Slow Contol center script. A parameter library file contains user adjustable parameters pertaining to a device (Frequently updated). For the High Voltage Control (HVC) devices, their voltage settings (parameters), for example, will be in the library file entitled according to the name of the devices (HVC), with parameter (PAR) appended to the file name. All files pertaining to the experiment are prepended with the abbreviation DXE (Davis Xenon). The parameter file for High Voltage Control is thus entitled DXE_LIB_HVC_PAR.py. Some instruments may be implemented with a greater or lesser amount of associated files, three are utilized for the high voltage control in specific.

A note on nomenclature:
Subspecifiers (such as cat in animal_cat) will not be included in parameter names when current context indicates subspecification. For example, in a set of library files corresponding to a given device, this correspondence is the only one necessary and the given device's name will not be rereferenced in a parameter.
