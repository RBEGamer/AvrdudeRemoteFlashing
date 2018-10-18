# AvrdudeRemoveFlashing
![GitHub Logo](/documentation/ch.png)
A simple script to monitor `.hex`, `.eep` files and program it to the avr chip

# FEATURES
* `.hex` and `.eep` flashing
* file system monitoring (Build directory) for instant flahsh
* works on RPI


# NEEDED HARDWARE
* A avrdude compatible programmer like the cheap USBASP

# USAGE
modify the following lines to setup the system in `avrdude_flasher.py`:

* `9 chip = "attiny2313"` define here the default chip if it not in the filename. See avrdude docu -p flag
* `programmer = "usbasp"` define here your programming device. See avrdude docu for the -c flag
* `path_to_watch = "./GccApplication3/GccApplication3/Debug"` define the path to watch for .hex files

See at function flash for more configration flags.

# SETUP
Any linux system with `python2` and `avrdude` installed.
I used a RPI Zero with an USBASP connected.

I setup a smb share and setup the `path_to_watch` path to it, so if AVRStudio generates a new build the pythonscript flashes the new file to the chip.

After setup simply run `avrdude_flasher.py`

# BUILD FILESNAMES
A feature is that the chip to programm can be determand in the filename, so you dont need to change the script.
The filename for `.hex` and `.eep` need the following pattern:
`_<projectname>_<chipname>_.hex` and `_<projectname>_<chipname>_.eep`
So a valid build file for an Attiny2313 is:
* HEX:`~/build/_ledblink_attiny2313_.hex` 
* EEP:`~/build/_ledblink_attiny2313_.eep` 


# AtmelStudioSetup
A AtmelStudioProject runs not very well on a FileShare i have noticed.
So i added a PostBuildRule to copy the build files to the share via a windows copy command:


* hardcoded chip name: `copy $(MSBuildProjectDirectory)\Debug\$(AssemblyName).hex  C:\Users\root\Dropbox\testproj\Debug\_$(AssemblyName)_attiny2313_.hex`

## OR:

* with atmel studio macro: `copy $(MSBuildProjectDirectory)\Debug\$(AssemblyName).hex  C:\Users\root\Dropbox\testproj\Debug\_$(AssemblyName)_$(avrdevice)_.hex`
