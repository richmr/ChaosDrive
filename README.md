# Chaos Drive

Chaos Drive is a POC of a USB Flash drive that can do funny things with presented storage.
In USB Gadget parlance, the storage that is presented when a drive is plugged in is called a LUN.

The drive has two LUNs, public and secret.  The public LUN is presented at every boot, and the secret LUN can be summoned by specific commands

## Main Chaotic functions of the drive:

Because the drive is actually a fully functioning Linux device, it can interact with the LUNs in interesting ways
### Chaotic Good:

- Reveal - Present the secret LUN in response to a specific file being written at a specific place.  I consider this Chaotic Good because it can be a good way to hide something from casual inspection

### Chaotic Neutral:

- Squawk - Activate a serial TTY on the drive so you can log in and make changes
- FailFail - Activate a serial TTY if the drive keeps having problems running correctly

### Chaotic Evil

- Alchemy - Run a script to modify contents of a LUN before it is presented to the user
- Dupe - Copy the contents of the public LUN to the secret LUN surreptitiously
- Fickler - Present a different LUN depending on how many times the drive has been used
    - Intended use is to present files that get virus scanned, and then present a different set the next time the drive is used

## Quick Start:

The easiest way to get started is to [download](PocketBeagle/image) and flash the completed image, slap it in a PocketBeagle, boot up, and follow the instructions in [readme.txt](PocketBeagle/readme.txt)

Otherwise build your own PocketBeagle image by following these [directions](PocketBeagle/buildroot)

## Compatible boards
In theory, Chaos Drive can be made to work on any OTG-capable Linux system.  But I have only worked on the PocketBeagle and the RPi Zero.  Very early on I switched over to the PocketBeagle and my most up-to-date code is all for the PocketBeagle.  The RPi Zero is best used for casual experimentation.  I do not update the RPi Zero code.   
