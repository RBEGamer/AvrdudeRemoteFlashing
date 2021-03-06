# AvrdudeRemoveFlashing

A simple script to monitor `.hex`, `.eep` files and program it to the avr chip
![GitHub Logo](/documentation/ch.png)

# FEATURES
* `.hex` and `.eep` flashing
* file system monitoring (Build directory) for instant flash to the chip
* works on RPI/Linux


# NEEDED HARDWARE
* A avrdude compatible programmer like the cheap USBASP

# USAGE
modify the following lines to setup the system in `avrdude_flasher.py`:

* `9 chip = "attiny2313"` define here the default chip if it not in the filename. See avrdude docu `-p` flag
* `programmer = "usbasp"` define here your programming device. See avrdude docu for the `-c` flag
* `path_to_watch = "./GccApplication3/GccApplication3/Debug"` define the path to watch for `.hex` files

See at function flash for more configration flags.

# SETUP
Any linux system with `python2` and `avrdude` installed.
I used a RPI Zero W with an USBASP connected.

I setup a smb share and setup the `path_to_watch` path to it, so if AtmelStudio generates a new build and the pythonscript flashes the new file to the chip on an other Computer.

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

## RUNNING MONITOR ON SMB SHARE
If you want to watch `*.hex` files on smb shares you have to mount it on ubuntu into the filesystem.
The normal Files-Application dont do that.
So first you have to install `cifs-utils`
* `sudo apt-get install cifs-utils`
Create a local mounting folder
* `sudo mkdir /mnt/tmp_dev_share`
And mount the SMB Server to it (Here the smb share is on `192.168.1.23` and we want to mount the `/home/tmp` folder)
* `sudo mount -t cifs //192.168.1.23/home/tmp /mnt/tmp_dev_share`

The last step is to edit the `path_to_watch` Variable to `/mnt/tmp_dev_share`
