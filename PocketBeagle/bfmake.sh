#!/bin/sh

# Use to make backing files for chaos drive
# Follows recipe at http://linux-sunxi.org/USB_Gadget/Mass_storage


usage() 
{
    echo "Use to make sparse backing files for chaos drive"
    echo "Only makes VFAT partitioned systems"
    echo "Curently optimized for BusyBox running on PocketBeagle"
    echo "(c) 2019 Michael Rich @miketofet"
    echo
    echo "usage $0 [-s s] [-l l] backing_file_name"
    echo "  -s size of backing file in MB [default is 1024]"
    echo "  -l loopback device [default is 0]"

    echo  
    echo "  By default, will make a 1 Gb sparse backing file"
}


### Constants

BLOCK_SIZE=512

### Initialized variables

drive_size=1024
loop_dev=0

### Process opts
while getopts ":s:l:h" opt; do
    case ${opt} in
        s )
            drive_size=$OPTARG
            ;;
        h )
            usage
            exit 0
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

# Grab the positional
backing_file_name=$1

if [ -z "$backing_file_name" ]
then
      echo "Please specify the backing file to make" 1>&2
      usage
      exit 1
fi

# create the sparse file
dd if=/dev/zero of=$backing_file_name bs=1M seek=$drive_size count=0

# create the partition in the file
# buildroot doesnt have sfdisk and I'm not interested in learning parted today
# So.. Ugly non-interactive fdisk hack starts..  here..
printf "n\np\n1\n2048\n\nt\nc\nw\n" | fdisk -u $backing_file_name

# setup to loopback
# Since we just made the thing, the offset is always 512*2048
losetup -o1048576 /dev/loop$loop_dev $backing_file_name

# make the filesystem
mkdosfs /dev/loop$loop_dev

# tear down the loop
losetup -d /dev/loop$loop_dev
