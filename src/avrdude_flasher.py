#!/usr/bin/env python

import os, sys, time
from subprocess import call
from subprocess import Popen, PIPE
import subprocess
import re

chip = "attiny2313" #Defualt chip can overwritten by filename _<projectname>_chip_.hex
programmer = "usbasp"
path_to_watch = "./GccApplication3/GccApplication3/Debug"


def files_to_timestamp(path):
    files = [os.path.join(path, f) for f in os.listdir(path)]
    return dict ([(f, os.path.getmtime(f)) for f in files])


def compile(_file):
    #run avr-gcc
    #build dir is smae folder
    #main.cpp nicht löschen

def flash(hex_file, eep_file):
    enable_flash_writing = True
    enable_eeprom_writing = False
    
   # print("- USING attiny2313 -- USBASP ---")

    #BURN FLASH
    if hex_file and enable_flash_writing:
        abs_path_hex = os.path.abspath(hex_file)
        if not re.match(".*.hex$",abs_path_hex):
            print "--- ERROR .hex not Found---"
        else:
            sp = str(abs_path_hex).split("_")
            _len = len(sp)
            if _len >= 3:
                chip_name = sp[_len-2].lower()
            else:
                chip_name = chip
                print("--- USING DEFUALT CHIP "+ chip_name + " -----")

            print subprocess.Popen("avrdude -c "+programmer+" -p "+chip_name+"  -U flash:w:" + str(abs_path_hex), shell=True, stdout=subprocess.PIPE).stdout.read()
            os.remove(abs_path_hex)

    #WRITE EEPROM
    if eep_file and enable_eeprom_writing:
        print("-- PROGRAMMING EEP FILE")
        abs_path_eep = os.path.abspath(eep_file)
        if not re.match(".*.eep$",abs_path_eep):
            print "--- ERROR .eep not Found---"
        else:
            sp = str(abs_path_eep).split("_")
            _len = len(sp)
            if _len >= 3:
                chip_name = sp[_len-2].lower()  
            else:
                chip_name = chip
                print("--- USING DEFUALT CHIP "+ chip_name + " -----")
            print subprocess.Popen("avrdude -c "+programmer+" -p "+chip_name+" -B 1  -U eeprom:w:" + str(abs_path_eep), shell=True, stdout=subprocess.PIPE).stdout.read()
            os.remove(abs_path_eep)




if __name__ == "__main__":

   


    print "Watching ", path_to_watch

    before = files_to_timestamp(path_to_watch)

    while 1:
        time.sleep (2)
        after = files_to_timestamp(path_to_watch)

        added = [f for f in after.keys() if not f in before.keys()]
        removed = [f for f in before.keys() if not f in after.keys()]
        modified = []

        for f in before.keys():
            if not f in removed:
                if os.path.getmtime(f) != before.get(f):
                    modified.append(f)

        if added: 
            print "Added: ", ", ".join(added)
            for td in added:
                if re.match(".*.hex$",td):
                    flash(td,None)
                if re.match(".*.eep$",td):
                    flash(None,td)
                if re.match(".*.cpp$",td):
                    compile(td) 

        if removed: print "Removed: ", ", ".join(removed)

        if modified: 
            print modified
            for td in modified:
                if re.match(".*.hex$",td):
                    flash(td,None)       
                if re.match(".*.eep$",td):
                    flash(None,td) 
                if re.match(".*.cpp$",td):
                    compile(td) 
        before = after
