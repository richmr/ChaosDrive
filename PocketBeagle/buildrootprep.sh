#!/bin/sh

# Simply copies files from this root directory to proper place in
# buildroot file structure.  I do this before every image build

# ensure the proper scripts are executable
chmod a+x *.sh
chmod a+x *.py

# First the main script
cp -f chaosDrive_pb.py buildroot/pocketbeagle/overlay/etc/chaos/

# And the alchemy test script
cp -f alchemyTest.py buildroot/pocketbeagle/overlay/etc/chaos/

# Now the backing file scripts and fakentp
cp -f bf*.sh buildroot/pocketbeagle/overlay/etc/chaos/
cp -f fakentp.sh buildroot/pocketbeagle/overlay/etc/chaos/

# Config file
cp -f chaosdrive.cfg buildroot/pocketbeagle/overlay/etc/chaos/config/

# Put the startup script in place
cp -f S50chaosdrive_initial.sh buildroot/pocketbeagle/overlay/etc/init.d/

# Copy the run script (to be moved by user after first boot)
cp -f S60chaosdrive_run.sh buildroot/pocketbeagle/overlay/etc/chaos/

# put the readme in the root folder, since that is landing after serial tty
cp -f readme.txt buildroot/pocketbeagle/overlay/root/

# make important directories
mkdir -p buildroot/pocketbeagle/overlay/mnt/chaos
mkdir -p buildroot/pocketbeagle/overlay/mnt/secret
mkdir -p buildroot/pocketbeagle/overlay/etc/chaos/backing
mkdir -p buildroot/pocketbeagle/overlay/etc/chaos/logs

# Now copy the overlay directory to your buildroot board directory
