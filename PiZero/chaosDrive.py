#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 07:12:39 2019

@author: mike@tofet.net
"""


# Packages

import inotify.adapters
import argparse
import ConfigParser
import crypt
import os
import logging
import random
import string
import getpass
import subprocess
import signal


def configure_logging(console=False, level=logging.INFO):
    global logger
    logger = logging.getLogger('chaosdrive')
    logger.setLevel(logging.DEBUG)
    
    formatstr = '(%(asctime)s) %(levelname)s> %(message)s'
    datefmtstr = '%m/%d/%Y %H:%M:%S'
    
    handler = logging.FileHandler(global_logfile)
    handler.setLevel(level)
    formatter = logging.Formatter(fmt=formatstr, datefmt=datefmtstr)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    if (console):
        # Add a stream handler
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(fmt=formatstr, datefmt=datefmtstr)
        handler.setFormatter(formatter)
        logger.addHandler(handler)    
    
    return logger

def cfg_section_active(section):
    # This checks to see if the desired section and "active" option exists for the section
    # If the section or active option doesn't exist it returns False
    # If the section and active option does exist it returns the boolean value of the option
    result = False
    global config
    if (config.has_option(section, 'active')):
        result = config.getboolean(section, 'active')
    return result

def present_LUN(lun):
    # executes modprobe command to show LUN
    logger.debug("present_LUN({}) called".format(lun))
    f = subprocess.check_call(["modprobe","g_mass_storage","file={}".format(lun),"stall=0"])
    return

def close_LUN():
    logger.debug("close_LUN() called")
    f = subprocess.check_call(["modprobe","-r","g_mass_storage"])

def present_public_LUN():
    present_LUN(config.get('lun','publicLUN'))
    return

def present_secret_LUN():
    present_LUN(config.get('lun','secretLUN'))
    return

def mount_backing_file(backingFile, write=False, mount_point=False):
    # Mount -o loop,ro -t vfat /piusb.bin /mnt/loop
    logger.debug("mount_backing_file({}, {}) called".format(backingFile, write))
    dash_o = "loop,ro"
    if (write):
        dash_o = "loop"
    
    if (not mount_point):
        # No mount point was provided, default is in the config file
        mount_point = config.get('loop','loop')
        
    f = subprocess.check_call(["mount","-o",dash_o,"-t","vfat",backingFile,mount_point])
    return

def unmount(mount_point=False):
    # umount /mnt/loop
    logger.debug("unmount({}) called".format(mount_point))
    try:
        if (not mount_point):
            mount_point = config.get('loop','loop')
            
        f = subprocess.check_call(["umount",mount_point])
    except BaseException as badnews:
        # If umount fails, then the mount point is probably cleared already
        logger.warn("unmount() failed with {}".format(badnews))
        logger.warn("This is interpreted as the mount point already being cleared")
        
    return

def mount_public(write=False):
    mount_backing_file(config.get('lun','publicLUN'), write=write, mount_point=config.get('loop','loop'))
    return

def mount_secret(write=False):
    mount_backing_file(config.get('lun','secretLUN'), write=write, mount_point=config.get('loop','secret_loop'))
    return

def check_for_file(filename, auth=False):
    # Checks for filename at the root of LUN mount and verifies auth if True
    # returns true if filename exists and auth passes (if requested)
    # assumes backing file is already mounted
    logger.debug("check_for_file({}, {}) called".format(filename, auth))
    found = False
    filename = config.get('loop','loop')+"/"+filename
    try:
        if (os.path.isfile(filename)):
            logger.debug("{} found, checking if auth needed.".format(filename))
            f = open(filename, 'r')
            if (auth):
                # read the first line of the file for PLAINTEXT password
                key = f.readline().rstrip()
                passwd = config.get('auth','passwd')
                found = (crypt.crypt(key, passwd) == passwd)
                if (not found):
                    logger.warn("file {} found, but key '{}' did not match passwd in config file".format(filename, key))
            else:
                logger.debug("Auth not required for control file")
                found = True
            f.close()
        else:
            logger.debug("{} not found".format(filename))
    except IOError as badnews:
        logger.debug('check_for_file() IOError: {}'.format(badnews))
        found = False
    logger.debug("check_for_file: returning {}".format(found))
    return found

def delete_file(filename):
    # Just a wrapper for clarity sake
    # assumes backing file is already mounted
    logger.debug("delete_file({}) called".format(filename))
    filename = config.get('loop','loop')+"/"+filename
    os.remove(filename)
    return

def newconfig():
    """
    This needs to:
        - Copy newconfig.cfg to a working area
        - Go through the known sections
            - Check for each section
            - if active, check to make sure each required section is in place and 
            - specified files etc exist
            - if not, record errors in an error log and post to public and remount
    
    I still don't think this is a good idea.
    """
    return
    

def dupe():
    # Dupe function
    logger.debug("dupe() entered")
    wait = config.getboolean('dupe','wait_for_dupe')
    # mount the secret file
    mount_secret(write=True)
    src = config.get('loop','loop') + "/"
    dest = config.get('loop','secret_loop') + "/" + config.get('dupe','rsync_dest')
    rsync_opts = config.get('dupe','rsync_options')
    rsync_cmd = "rsync {} {} {}".format(rsync_opts, src, dest)
    logger.debug("dupe(): rsync command: {}".format(rsync_cmd))
        
    
    try:
        if (wait):
            logger.debug("Waiting for rsync to complete before LUN presentation")
            # Then we mount the public backing file and copy first
            mount_public()
            f = subprocess.check_call([rsync_cmd], shell=True)
            logger.info("dupe(): rsync complete")
            # When rsync returns, we unmount public and present it
            unmount()
            present_public_LUN()
            # then unmount secret
            unmount(config.get('loop','secret_loop'))
        else:
            logger.warn("Starting copy operation after presenting public LUN, this can cause instability")
            present_public_LUN()
            mount_public()
            f = subprocess.check_call([rsync_cmd], shell=True)
            logger.info("dupe(): rsync complete")
            # When rsync returns, we unmount public
            unmount()
            # then unmount secret
            unmount(config.get('loop','secret_loop'))
        logger.debug("dupe() complete")
    except BaseException as badnews:
        logger.error("dupe() failed with: {}".format(badnews))
        # ensure the public LUN is presented
        present_public_LUN()
        
    return

def alchemy():
    #alchemy function
    logger.info("alchemy() started")
    # mount the public and secret backing files and execute the script
    mount_public(write=True)
    mount_secret(write=True)
    
    cmd = '{} --publicLUN="{}" --secretLUN="{}"'.format(config.get('alchemy','script'), config.get('loop','loop'), config.get('loop','secret_loop'))
    logger.debug("alchemy(): script to call: {}".format(cmd))
    f = subprocess.check_call([cmd], shell=True)
    # unmount when complete (execute script in blocking mode!!)
    unmount()
    # then unmount secret
    unmount(config.get('loop','secret_loop'))
    return

def fickler():
    #fickler function
    logger.debug("fickler() entered")
    logger.info('fickler function started')
    count = increment_persistent_count(config.get('fickler','ficklerfile'))
    interval = config.getint('fickler','interval')
    logger.debug('fickler: count = {}, interval = {}'.format(count, interval))
    if ((count % interval) == 0):
        logger.info('fickler: presenting secret LUN on count {} and interval {}'.format(count, interval))
        present_secret_LUN()
        # exit
        os._exit(0)
    else:
        # Fickler isn't activated, should continue with chaos
        pass
    
    return

def squawk(force=False):
    # squawk function
    # Only confirmed working on PocketBeagle
    logger.debug("squawk({}) entered".format(force))
    activate = force
    
    mount_public()
    if (check_for_file(config.get('squawk', 'filename'), config.getboolean('squawk','auth'))):
        logger.info('Squawk control found, activating TTY')
        unmount()
        close_LUN()       
        activate = True
        mount_public(write=True)
        # delete the control file
        delete_file(config.get('squawk', 'filename'))
        # unmount the backing file
        unmount()
    else:
        logger.debug('Squawk control not found')
        unmount()
    
    if (activate):
        logger.info("Squawk activating")
        # activate g_Seral
        close_LUN()
        cmd = "modprobe g_serial"
        f = subprocess.check_call([cmd], shell=True)
        
        # ensure tty is enabled
        cmd = "systemctl enable serial-getty@ttyGS0.service"
        f = subprocess.check_call([cmd], shell=True)
        cmd = "systemctl restart serial-getty@ttyGS0.service"
        f = subprocess.check_call([cmd], shell=True)

    return activate

def reveal():
    # reveal function
    logger.debug("reveal() entered")
    
    # check for the reveal control file
    mount_public()
    reveal_complete = False
    if (check_for_file(config.get('reveal','filename'), config.getboolean('reveal','auth'))):
        logger.info('Reveal control found, switching LUN.')
        # unmount public backing file
        unmount()
        # Switch LUN presentation
        close_LUN()
        present_secret_LUN()
        # remount public backing file with write
        mount_public(write=True)
        # delete the control file
        delete_file(config.get('reveal','filename'))
        # unmount the backing file
        unmount()
        reveal_complete = True
    else:
        # Still need to unmount the drive
        unmount()
        
    return reveal_complete

def increment_persistent_count(filename):
    # opens the filename, reads the number in there, adds 1, stores the new number
    # and returns the new number
    number = 0
    if (os.path.isfile(filename)):
        f = open(filename, "r")
        number = int(f.readline().rstrip()) + 1
        f.close()
    else:
        number = 1
    
    with open(filename, "w") as counter:
        counter.write("{}\n".format(number))
    return number

def reset_counter(filename):
    with open(filename, "w") as counter:
        counter.write("0\n")
    return 

def failfail():
    # Escape valve.  If chaosdrive has 5 consecutive hard fails, activate squawk
    # check the count of fails
    # if = to or > 5, activate squawk
    try:
        numfails = increment_persistent_count(config.get('failfail', 'failfile'))
        if (numfails >= config.getint('failfail','maxfailcount')):
            logger.warn('Max failfail count reached.  Remember to reset the count after troubleshooting')
            squawk(force=True)
    except BaseException as badnews:
        logger.critical('Unhandled exception in failfail: {}'.format(badnews))
        squawk(force=True)
        
    return

def inotify_wait_for_modify(filename):
    # inotify can sometimes spam MODIFY notifications for single events
    # this is basically a low pass filter
    # Please note this is an infinite watch loop
    logger.debug("inotify_wait_for_modify(filename={}) called".format(filename))
    i = inotify.adapters.Inotify()

    i.add_watch(filename, mask=inotify.constants.IN_MODIFY)
    waitingForModify = True
    firstModFound = False
    
    while waitingForModify:
        events=i.event_gen(yield_nones=False, timeout_s=1)
        events = list(events)
        if len(events) > 0:
            firstModFound = True
        else:
            if firstModFound:
                waitingForModify = False
            

    logger.debug("inotify_wait_for_modify(): event seen")
    waitingForModify = True
    firstModFound = False
    return
                            
    
def monitor(action):
    """
    This is the meat of the chaos drive activity
    The rest is basically infrastructure..
    """
    logger.debug("monitor('{}') entered".format(action))
    try:
        
        if (action=="test"):
            logger.info("-------- Chaos Drive started in TEST mode ---------")
            test_clean()
        else:
            logger.info("-------- Chaos Drive started in daemon mode --------")
            
        global config
        # Power up - chaosDrive assumes only power comes from the host device, so it
        # boots fresh on every insert
        # First look for new config file - Note this file is only checked for on reboot
        # So needs to be placed and then the device cycled.
        # Easier to do with squawk mode, probably
        # Yeah, I don't like this..  Delays boot every time.  Think this update needs to
        # be done through squawk
#        mount_public()
#        if (check_for_file(config.get('auth','configFile'), config.get('auth','passwd'))):
#            logger.info('new config file found')
#        unmount()
            
        # First need to see if ghost copy is enabled
        if (cfg_section_active("dupe")):
            dupe()
                    
        # Then see if boggart is enabled, if so
        if (cfg_section_active("alchemy")):
            alchemy()
            
        # Then check fickler
        if (cfg_section_active("fickler")):
            fickler()
            
        # Present public LUN
        present_public_LUN()
        logger.info('public LUN presented from backing file: {}'.format(config.get('lun', 'publicLUN')))
        
        # Begin monitor mode IF monitoring functions enabled, otherwise 
        if (cfg_section_active("squawk") or cfg_section_active("reveal")):
            logger.info('Entering public_LUN monitoring loop')
            # inotify wait for write action on the public LUN file
            while True: 
                inotify_wait_for_modify(config.get('lun', 'publicLUN'))
                
                logger.debug('Write event detected on backing file')
                
                if (cfg_section_active("squawk")):
                    if (squawk()):
                        break
                
                if (cfg_section_active("reveal")):
                    if (reveal()):
                        # Once the secret LUN is presented, chaosDrive won't do anything else
                        break
                            
    except BaseException as badnews:
        logger.critical('monitor(): Unhandled exception received: {}'.format(badnews))
        failfail()       
        os._exit(-1)
    
    return

def write_pid(pid):
    global logger
    global global_pidfile
    logger.debug("write_pid()")
    try:
        f = open(global_pidfile, 'w')
        f.write("{}".format(pid)+"\n")
        f.close()
        logger.debug("Daemon pid is {}".format(pid))
    except IOError as badnews:
        logger.critical("Unable to write pid file because: {}".format(badnews))
        logger.critical("Is the daemon already running?")
        os._exit(-1)
    
    return

def read_pid():
    global logger
    global global_pidfile
    logger.debug("read_pid()")
    try:
        f = open(global_pidfile, 'r')
        pid_str = f.readline()
        f.close()
        pid = int(pid_str)
        logger.debug("Daemon pid is {}".format(pid))
        return pid
    except IOError as badnews:
        logger.critical("Unable to read pid file because: {}".format(badnews))
        logger.critical("ChaosDrive is unable to stop itself")        
        os._exit(-1)
        
def generate_password(pwd):
    salt = ''.join(random.SystemRandom().choice(string.letters + string.digits) for _ in range(8))
    entry = crypt.crypt(pwd, '$6$'+salt+'$')
    return entry

def getpwd():
    match = False
    while (not match):
        key = getpass.getpass("Password: ")
        key2 = getpass.getpass("Re-enter password: ")
        match = (key == key2)
        if (not match):
            print "Did not match!  Please try again."
    
    return key

def test_clean():
   # Need to start system in a clean state
   logger.debug('test_clean() called')
   close_LUN()
   unmount()
   unmount(config.get('loop','secret_loop'))
   return
   


# Set up args -----------------------------
description = 'ChaosDrive v0.1 Beta\n'
description += "Because USB drives are too trustworthy"

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("action", type=str, help="install - NOT IMPLEMENTED\ntest - run in console mode, acting as if fresh power up\nrun - run in daemon mode\nstop - stop the daemon\npassword - generate password entry", choices=['install', 'test', 'run', 'stop', 'password'])
parser.add_argument("-c", "--configfile", type=str, help="Use a specific config file, default is /etc/chaos/config/chaosdrive.cfg", default="/etc/chaos/config/chaosdrive.cfg")
parser.add_argument("-l", "--logfile", type=str, help="Log to a specific log file, default is /etc/chaos/logs/chaosdrive.log", default="/etc/chaos/logs/chaosdrive.log")
parser.add_argument("-p", "--pidfile", type=str, help="PID file that holds the daemon PID, default is /etc/chaos/logs/chaosdrive.pid", default="/etc/chaos/logs/chaosdrive.pid")
parser.add_argument('-d', "--debug", action='store_true', help='Enable all debugging log messages')
# And GO!

args = parser.parse_args()

# set the file locations
global_cfgfile = args.configfile
global_logfile = args.logfile
global_pidfile = args.pidfile

# logging level
global logger
log_level = logging.INFO
if (args.debug):
    log_level=logging.DEBUG

# Parse the config file
global config
config = ConfigParser.ConfigParser()
config.read(global_cfgfile)

# parse the action
if (args.action == 'install'):
    configure_logging(console=True, level=log_level)
    logger.error("Install action not implemented!  Please see XXXX for more info")
    os._exit(-1)
elif (args.action == 'test'):
    # Runs the chaosDrive in blocking mode
    configure_logging(console=True, level=log_level)
    monitor(args.action)    
elif (args.action == 'run'):
    # Runs chaosDrive in daemon (i.e. production mode)
    configure_logging(console=False, level=log_level)
    newpid = os.fork()
    if (newpid==0):
        # I'm the child process
        # write my pid to assist with stopping
        write_pid(os.getpid())
        # begin monitoring
        logger.debug("I'm the child and I'm starting the daemon")
        monitor(args.action)
    else:
        # I'm the parent
        logger.debug("I'm the parent and need to exit")
        os._exit(0)
elif (args.action == 'stop'):
    # Stops the chaosdrive daemon
    # Read the pid
    configure_logging(console=True, level=log_level)
    chaospid = read_pid()
    logger.info("stop action received")
    os.kill(chaospid, signal.SIGKILL)
    os._exit(0)
elif (args.action == 'password'):
    configure_logging(console=True, level=log_level)
    print "Use this to generate a passwd entry for the drive config file."
    pwd = getpwd()
    print "Entry: passwd = {}".format(generate_password(pwd))
    
logger.info('chaosDrive complete')   
