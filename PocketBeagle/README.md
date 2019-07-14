# Loki

RPi Zero (Raspbian) Instructions

Working from a sudo user

Set up file structure:
- mkdir /etc/chaos
- mkdir /etc/chaos/backing
- mkdir /etc/chaos/config
- mkdir /etc/chaos/logs

Make the mount points.  These need to match your config file settings
- mkdir /mnt/chaos
- mkdir /mnt/secret

Make public and secret backing files in the backing directory
(instructions taken from https://gist.github.com/gbaman/50b6cca61dd1c3f88f41)
- Calculate block count required for desired backing file size: file_size_in_bytes/512
- For example: 8 GB -> 8000000000/512 = 15625000
- sudo dd if=/dev/zero of=/etc/chaos/backing/public.bin bs=512 count=15625000
- sudo mkdosfs /etc/chaos/backing/public.bin
- sudo dd if=/dev/zero of=/etc/chaos/backing/secret.bin bs=512 count=15625000
- sudo mkdosfs /etc/chaos/backing/secret.bin

Python dependencies
- Install pip: sudo apt-get install python-pip
- Install inotify: sudo pip install inotify
- Install mtools: sudo apt-get install mtools
- Install fatattr: sudo apt-get install fatattr

PocketBeagle prep
- Get your board access to the internet: https://www.hackster.io/hologram/sharing-internet-with-the-pocketbeagle-on-osx-cd62b2
- sudo apt-get update
- sudo apt-get install inotify-tools

Install files:
- Copy chaosDrive.py to /etc/chaos
- chmod a+x /etc/chaos/chaosDrive.py 
- Copy chaosdrive.cfg to /etc/chaos/config
- Copy chaosdrive.sh to /etc/init.d
- chmod a+x /etc/init.d/chaosdrive.sh
- Copy chaosBoot.sh to /opt/scripts/boot
- chmod a+x /opt/scripts/boot/chaosBoot.sh

Set up chaosDrive to start at boot (as root):
- cd /etc/init.d
- update-rc.d chaosdrive.sh defaults

Modify the default PocketBeagle start up script:
-  Replace "am335x_evm.sh" with "chaosBoot.sh" on line 105 of /opt/scripts/boot/generic-startup.sh



