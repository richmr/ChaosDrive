#!/bin/sh

# Use to mount backing files for chaos drive
# backing files may have variable offsets, this is used to assist with that
# assumes type is vfat
# bfmount [-o mount_options] backing_file mount_point


usage() 
{
    echo "Use to mount backing files for chaos drive"
    echo "Backing files may have variable offsets, this is used to deal with that issue"
    echo "Curently optimized for BusyBox running on PocketBeagle"
    echo "(c) 2019 Michael Rich @miketofet"
    echo
    echo "usage $0 [-o o] [-p p] [-f f] [-l l] backing_file mount_point"
    echo "  -o mount options [default is rw]"
    echo "  -p partition number [default is 1 (first)]"
    echo "  -f fdisk -l partition start field (default is 4 (busybox))"
    echo "  -l loopback device number [default is 0]"

    echo  
    echo "  By default, bfmount will mount as partition 1 as rw"
}


### Constants

BLOCK_SIZE=512

### Initialized variables

partition=1
mnt_options="rw"
fdisk_field=4
loop_dev=0

### Process opts
while getopts ":o:p:f:l:h" opt; do
    case ${opt} in
        o )
            mnt_options=$OPTARG
            ;;
        h )
            usage
            exit 0
            ;;
        p )
            partition=$OPTARG
            ;;
        f )
            fdisk_field=$OPTARG
            ;;
        l )
            loop_dev=$OPTARG
            ;;
        \? )
            echo "Invalid Option: -$OPTARG" 1>&2
            echo
            usage
            exit 1
            ;;
        : )
            echo "Invalid option: -$OPTARG requires an argument" 1>&2
            echo
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND -1))

# Grab the positionals
backing_file=$1
mount_point=$2

if [ -z "$backing_file" ]
then
      echo "Please specify the backing file to mount"
      usage
      exit 1
fi

if [ -z "$mount_point" ]
then
      echo "Please specify the mount point"
      usage
      exit 1
fi

# Get the offset for the given partition number
offset_sector=$(fdisk -l $backing_file | grep $backing_file$partition | awk "{print \$$fdisk_field}")

# error check
if [ -z "$offset_sector" ]
then
    echo "Unable to find offset for desired partition number.  Check -n or -f"
    exit 1
fi

# translate to byte offset
offset_byte=$(($offset_sector*$BLOCK_SIZE))

# set up loopback
if [ -z "$loop_dev" ]
then
    # This didn't work correctly because then I didn't know loop device to use for mount
    # Differences in busybox vs debian in losetup make fixing this not worth it
    # just track your loop devices!
    losetup -f -o$offset_byte $backing_file
else
    losetup -o$offset_byte /dev/loop$loop_dev $backing_file
fi

# mount it
mount -o $mnt_options -t vfat /dev/loop$loop_dev $mount_point
exit 0
