# Chaos Drive on the RPi Zero

I started building the drive on the RPi Zero but was unhappy with the boot times (> 40 seconds to present a LUN).  I was also unable to get Buildroot to work on the Zero despite multiple attempts.  After I shifted to the PocketBeagle and Buildroot, the code base diverged significantly.  These instructions and the code here are the last known working version of Chaos Drive on a RPi Zero

## RPi Zero (Raspbian) Instructions

Working from a sudo user

Set up file structure:
- `mkdir /etc/chaos`
- `mkdir /etc/chaos/backing`
- `mkdir /etc/chaos/config`
- `mkdir /etc/chaos/logs`

Make the mount points.  These need to match your config file settings
- `mkdir /mnt/chaos`
- `mkdir /mnt/secret`

Make public and secret backing files in the backing directory
(instructions taken from https://gist.github.com/gbaman/50b6cca61dd1c3f88f41)
- Calculate block count required for desired backing file size: file_size_in_bytes/512
- For example: 8 GB -> 8000000000/512 = 15625000
- `sudo dd if=/dev/zero of=/etc/chaos/backing/public.bin bs=512 count=15625000`
- `sudo mkdosfs /etc/chaos/backing/public.bin`
- `sudo dd if=/dev/zero of=/etc/chaos/backing/secret.bin bs=512 count=15625000`
- `sudo mkdosfs /etc/chaos/backing/secret.bin`

NOTE: I discovered later in the PocketBeagle build that the backing files made like this do not contain a valid partition table and will not present correctly to a Windows host.  OR, if you DO add a proper partition table the backing files may not mount correctly as a loopback device.  I eventually wrote "automagical" [create](PocketBeagle/bfmake.sh) and [mount](PocketBeagle/bfmount.sh) scripts to help with this, but they are designed to work on BusyBox and not Debian.  Refer to those scripts for the recipes I used to solve these problems.

Python dependencies
- Install pip: `sudo apt-get install python-pip`
- Install inotify: `sudo pip install inotify`

Install files:
- Copy chaosDrive.py to /etc/chaos
- `chmod a+x /etc/chaos/chaosDrive.py`
- Copy chaosdrive.cfg to /etc/chaos/config

At this point you can experiment with chaosDrive by entering /etc/chaos and running `./chaosDrive.py -d test`

You CAN make the drive start at boot, but on the RPi Zero you are probably better off just experimenting with it.

Set up chaosDrive to start at boot:
- Copy chaosdrive.sh to /etc/init.d
- `chmod a+x /etc/init.d/chaosdrive.sh`
- `cd /etc/init.d`
- `update-rc.d chaosdrive.sh defaults`
