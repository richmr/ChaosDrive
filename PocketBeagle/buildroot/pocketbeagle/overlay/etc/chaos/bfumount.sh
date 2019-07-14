#!/bin/sh

# Use to unmount backing files for chaos drive
# backing files are loaded as looped devices, so this tears the loop device down too
# bfumount mount_point


usage() 
{
    echo "Use to unmount looped backing devices for Chaos Drive"
    echo "Curently optimized for BusyBox running on PocketBeagle"
    echo "(c) 2019 Michael Rich @miketofet"
    echo
    echo "usage $0 mount_point"
}


# Grab the positionals
mount_point=$1

if [ -z "$mount_point" ]
then
      echo "Please specify the mount point"
      usage
      exit 1
fi


# First find the loop device
loop_dev=$(mount | grep $mount_point| awk '{print $1}')

# Error check
if [ -z "$loop_dev" ]
then
      echo "Unable to find loopback device.  Please check mount file for your mount point."
      usage
      exit 1
fi

#unmount it
umount $mount_point

# pull down the loopback device
losetup -d $loop_dev