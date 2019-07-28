#!/bin/sh

# Use to "steal" the time from a directory and set the system clock.
# Chaos Drive has no way to keep the current time, or get it by normal methods
# this is not a problem when saving and modifying files using the host
# but if the Chaos Drive does it itself (i.e. alchemy mode) it will
# leave highly suspicious dates behind that are mere seconds after the
# Unix epoch.

# This hack simply checks the directory it has been handed, picks the latest
# file in there, and sets the system clock to match.

# I use the atime, since that tends to be closer to the actual day
# but I use the hour and minutes from ctime to apply a little randomness
# to the hour that is set.  BusyBox reads FAT as atime always set to 00:00:00

# You go to hack with the time you've got, not the time you want

usage()
{
    echo "Use to steal approximate system time for Chaos Drive"
    echo "Curently optimized for BusyBox running on PocketBeagle"
    echo "(c) 2019 Michael Rich @miketofet"
    echo
    echo "usage $0 [-f] [directory]"
    echo "  -f Force (don't check for existing time)"
}

###

force=""

### Process opts
while getopts "hf" opt; do
    case ${opt} in
        h )
            usage
            exit 0
            ;;
        f )
            force=1
            ;;
        \? )
            echo "Invalid Option: -$OPTARG" 1>&2
            echo
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND -1))

# Grab the positionals
directory=$1

if [ -z "$directory" ]
then
      directory="."
fi

# neither of the following tests exits with anything other than 0 to prevent
# throwing exceptions in Chaos Drive

# First test, has time already been set?
# This rashly assumes any time after 2000 means the clock has already been set, let's return quick
# Will only make this check if -f has not been set
if [ -z "$force"]
then
  if test $(date -I | awk -F"-" '{print $1}') \> 2000
  then
      # for test only: echo "Date is already after 2000 time probably set?"
      exit 0
  fi
fi

# Next, check to see if there are files in the target directory
# If so, continue, if not exit gracefully
if test $(ls -l $directory | wc -l) = 1
then
    # for test only: echo "No files in target directory.  Better luck next time"
    exit 0
fi

# Good to go

# Set the system time
setday=$(ls -ltu --full-time $directory | head -n 2 | tail -n 1 | awk '{print $6}')
sethour=$(ls -lt --full-time $directory | head -n 2 | tail -n 1 | awk '{print $7}')

date -s "$setday $sethour"
exit 0
