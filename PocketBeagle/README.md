# Chaos Drive on the PocketBeagle

The PocketBeagle is an amazing board.  I suggest you get one.

Though I originally started working with the production PocketBeagle images provided by BeagleBoard I was not satisfied with how long it took to present a LUN (on the production image the kernel alone takes over 18 seconds to load).  So I built a custom [Buildroot](https://buildroot.org/) image and got the initial LUN presentation time down to about 10 seconds.

All of the code here is written to work in the BusyBox environment that Buildroot creates.  There are many differences between both the options and the output of the Debian and BusyBox versions of standard commands and I would not expect my scripts to work on the production PocketBeagle images (or any Debian environment).

The REALLY good news is my POC image is around a 20 MB download and it is very straightforward to use it on a PocketBeagle.  Follow [these instructions](image/) and you can have a working Chaos Drive in just a few minutes.

## Build Your Own Image
I've done my best to document how I configured Buildroot, from scratch, to create my image.

I owe a significant debt to [E-ALE](https://e-ale.org/) and the resources they provide on line and in their repo.  Without their scripts and documentation I doubt I would have gotten this build to work.  I have copied their publicly-available files to the proper locations in my repo and have tried to give credit as correctly as possible.

Follow the build instructions [here](buildroot).

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
