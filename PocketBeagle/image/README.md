# Pre-built Chaos Drive Image
Follow these steps to use this image:
- Download and extract the sdcard.img file from chaosdriveimage.tar.gz
- Mount an appropriate micro SD card on your host.  Testing can be done with something as small as 3 GB
- Burn the image to the SD card.  I like using [BalenaEtcher](https://www.balena.io/etcher/)
- Increase the size of the root file system.  You can make it as big as the SD card will let you, but make it at least 3 GB
- Insert the SD card in to the PocketBeagle and boot via OTG adapter or OTG cable
- After 10 seconds or so your host should register a new serial device.  
    * On a Linux system (or Mac OS) I like to run `ls -lt /dev/tty* | head`.  This will give you a time-ordered list of available tty devices.  If you aren't sure which one is the Chaos Drive, disconnect the Chaos Drive and look to see which one disappeared.  
    * On a Windows host, check the Device Manager for new serial devices.  It's usually COM3 or COM4 it seems.
- Connect to the terminal
    * On Linux/Mac OS, use `sudo screen \dev\ttydevice 115200` where "ttydevice" is the actual name of your device
    * On Windows use a client such as PuTTY
- You may see a login prompt or you may not.  If not, hit "Enter"
- Username is root and there is no password
    * WHAT?!  NO PASSWORD?! Yes. This is an embedded Linux device with no network access and after you follow the remainder of the instructions, the serial device will not present itself automatically again
- Follow the directions in /root/readme.txt to complete the set up. ([Also visible here](../readme.txt))

## Enjoy!
