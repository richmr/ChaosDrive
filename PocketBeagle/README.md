# Chaos Drive on the PocketBeagle

The PocketBeagle is an amazing board.  I suggest you get one.

Though I originally started working with the production PocketBeagle image provided by BeagleBoard I was not satisfied with how long it took to present a LUN (on the production image the kernel alone takes over 18 seconds to load).  So I built a custom [Buildroot](https://buildroot.org/) image and got the initial LUN presentation time down to about 10 seconds.

All of the code here is written to work in the BusyBox environment that Buildroot creates.  There are many differences between both the options and the output of the Debian and BusyBox versions of standard commands; I would not expect my scripts to work on the production PocketBeagle images (or any Debian environment).

The REALLY good news is my POC image is around a 20 MB download and it is very straightforward to use it on a PocketBeagle.  Follow [these instructions](image/) and you can have a working Chaos Drive in just a few minutes.

## Build Your Own Image
I've done my best to document how I configured Buildroot, from scratch, to create my image.

I owe a significant debt to [E-ALE](https://e-ale.org/) and the resources they provide online and in their repo.  Without their scripts and documentation I doubt I would have gotten this build to work.  I have copied their publicly-available files to the proper locations in my repo and have tried to give credit as correctly as possible.

Follow the build instructions [here](buildroot).

## Experimenting with Chaos Drive on a "vanilla" PocketBeagle
The [instructions and code for the RPi Zero](../PiZero) should work on a PocketBeagle running the production Debian image.

You should do these additional steps to prep first
- Get your board access to the internet: https://www.hackster.io/hologram/sharing-internet-with-the-pocketbeagle-on-osx-cd62b2
- sudo apt-get update
- sudo apt-get install inotify-tools

NOTE: I haven't tested these steps in a while.  I highly recommend jumping in to the Buildroot image.

## Configuring the Chaos Drive

The [chaosdrive.cfg](./chaosdrive.cfg) controls the Chaos Drive function and is fully commented

Also check options with `./chaosDrive_pb.py -h`

## The bf*.sh scripts
Working with backing files turned out to be a little tricky.  To help with that, I wrote some scripts.

Basically they automate the activation and tearing down of loop devices on the Linux system for creation and modification purposes.  The scripts are reasonably well commented and you can see the overall "recipe" I was automating at this link: http://linux-sunxi.org/USB_Gadget/Mass_storage

## The fakentp.sh script
The Chaos Drive has no way to keep the proper time, or get it.  This script "steals" the time from the files present on the public LUN to help get the device closer to the correct time.  In general, the time metadata for a file is created by the host.  However, if the drive itself creates or modifies any files (ex. while using Alchemy mode), it will set the time to the current system time.  If we don't "steal" some sort of reasonable time, then every new file will be created mere seconds after 00:00, Jan 1, 1970.
