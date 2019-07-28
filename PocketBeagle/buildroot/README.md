# Building the Chaos Drive Image
The Chaos Drive image is a customized [Buildroot](https://buildroot.org/) image.  The following instructions are my best attempt to describe how I configured Buildroot to work.

### Hacker Beware!
Having unknowingly borked my own development environment repeatedly, I can only state that Buildroot dev environments are brittle.  Here are some lessons that were inflicted upon me; may they provide some wisdom for you
- Only use the built-in configuration tools from the root of your Buildroot dev environment; for example, do not go to the Linux folder and run the configuration tool there.  From the root of my envrionment I used:
    - `make menuconfig` - Core Buildroot configurations
    - `make linux-menuconfig` - Direct configuration of linux
    - `make busybox-menuconfig` - A few details needed from here
- Take full advantage of the magical "/". Typing "/" while using the configuration tool will allow you to search for the option you are looking for.  It's SUPER useful
- Don't accidentally build as root; it will totally bork the permissions in your dev environment
- Consider running Buildroot from a VM.  Two updates to my OS broke my dev environment in complicated ways; a virtualized environment might help insulate from this problems

Lastly, I can't guarantee these instructions will work without some tweaking on your part.  As I stated, the Buildroot environment is brittle.  Changes to Buildroot, busybox, Linux kernels, or any packages may break your build.  Google and persistence got me through.  Good luck!

### Acknowledgements
I probably would not have been able to successfully use Buildroot on the PocketBeagle without these resources:
- [The Embedded-Apprentice Linux Engineer](https://e-ale.org/)
    - Their [GitHub repo](https://github.com/e-ale/Code/tree/master/RESOURCES/buildroot) provided the files used in my build
    - The walk-through by Thomas Petazzoni located [here](https://bootlin.com/pub/conferences/2018/elc/petazzoni-e-ale-buildroot-tutorial/petazzoni-buildroot-tutorial-lab.pdf) was absolutely critical to getting my build to work.
- Robert C. Nelson’s PocketBeagle work
    - The Linux config files on his [repo](https://github.com/RobertCNelson/Supercon-2017-PocketBeagle) allowed me to compare my settings and see what was wrong
    - Also the startup scripts for the production Beagle boards were a great resource

# Let's Build That Image
I am going to assume your buildroot environment is at: `~/buildroot` and your ChaosDrive repo is at `~/ChaosDrive`.  Adjust commands below as necessary.

## Download buildroot
Clone the Buildroot official Repo:

`git clone git://git.busybox.net/buildroot`

## Add Pocketbeagle board to buildroot folder structure
Clone my repo:

`git clone https://github.com/richmr/ChaosDrive.git`

After cloning my repository:

```
cd ~/ChaosDrive/PocketBeagle
./buildrootprep.sh
```

This will ensure the most recent files are in place in `~/ChaosDrive/PocketBeagle/buildroot/pocketbeagle` as well as ensure the proper overlay structure is in place.

Then copy the ChaosDrive pocketbeagle files to buildroot.  Be sure to copy over everything:

`cp -rf ~/ChaosDrive/PocketBeagle/buildroot/pocketbeagle/ ~/buildroot/board/`

## Initial buildroot set up

`cd ~/buildroot`

Mr. Petazzoni bases his work on a stable release (to help prevent that brittle effect I mentioned above).  So I did the same:

`git checkout -b ChaosDrive 2018.02`

Start basic configuration:

`make menuconfig`

**Note:** The following is a cut and paste from Thomas Petazzoni's [walk through](https://bootlin.com/pub/conferences/2018/elc/petazzoni-e-ale-buildroot-tutorial/petazzoni-buildroot-tutorial-lab.pdf) with light editing in **bold**.  I have also removed some text for conciseness indicated with *(...)*

> - In *Target options*
    - Change *Target architecture* to *ARM (little endian)*
    - Change *Target architecture* variant to *Cortex-A8*
- In *Build options*, set *global patch directories* to **board/pocketbeagle/patches/**. *(...)*
- In *Toolchain*
    - Change *Toolchain type* to *External toolchain*. *(...)*
- In *System configuration*, you can customize the *System host name* and *System banner* if you wish. Keep the default values for the rest.
- In *Kernel*
    - Enable the *Linux kernel*, obviously!
    - Choose *Custom version* as the *Kernel version*
    - Choose *4.14.24* as *Kernel version*
    - Patches will already be applied to the kernel, thanks to us having defined a *global patch directory above*.
    - Choose `omap2plus` as the *Defconfig name*
    - We’ll need the Device Tree of the PocketBeagle, so enable *Build a Device Tree Blob (DTB)*
    - And use `am335x-pocketbeagle` as the *Device Tree Source file names*
- In *Target packages*, we’ll keep just Busybox enabled for now. In the next sections, we’ll enable more packages.
- In *Filesystem images*, enable *ext2/3/4 root filesystem*, select the *ext4* variant. You can also disable the *tar* filesystem image, which we won’t need.
- In *Bootloaders*, enable *U-Boot*, and in *U-Boot*:
    - Switch the *Build system* option to *Kconfig*: we are going to use a modern U-Boot, so let’s take advantage of its modern build system!
    - Use a *Custom version* of value *2018.01*. You’ll notice that the current default is already 2018.01. However, Buildroot upstream is regularly updating this to the latest U-Boot version. However, to have a reproducible setup, we really want to use a fixed version.
    - Use `am335x_pocketbeagle` as the *Board defconfig*
    - The *U-Boot binary format* should be changed from `u-boot.bin` to `u-boot.img`. *(...)*
    - Enable *Install U-Boot SPL binary image* to also install the first stage bootloader. Its name in *U-Boot SPL/TPL binary image name(s)* should be changed to `MLO` since that’s how U-Boot names it, and how the AM335x expects it to be named.
- *(...)*
- In *System Configuration*
    - Set *Custom scripts to run after creating filesystem images* to **board/pocketbeagle/post-image.sh**
- In *Host Utilities* enable `host genimage`, `host mtools` and `host dosfstools`.

You might want to check to make sure everything compiles correctly at this point.  Exit the configuration tool and simply run `make`.  Come back in 10-15 minutes and look for `~/buildroot/output/images/sdcard.img`.  If it's there, you now have a basic working image you can try on your PocketBeagle. This isn't a completed ChaosDrive, just a working Busybox running on your board.

## Enabling needed ChaosDrive packages

Search for the required options using `/` and make sure they are enabled with a `[*]` or a `[m]`

- Under `make linux-menuconfig`
    - `USB Gadget Support`
        - Choose (if there are options) `USB Gadget Only`
    - `USB_MUSB_DSPS`
    - `USB_MUSB_HDRC`
    - `NOP_USB_XCEIV`
    - Exit and Save
- Under `make menuconfig`
    - `dosfstools`
    - `inotify-tools`
    - `lrzsz`
        - To greatly improve the ability to load debugged scripts and code to the board over the debug terminal
    - `python`
        - Under *Target packages -> Interpreter languages and scripting*
        - Not Python 3..  I'm sorry..  I really am.  I need to fix this
    - `python-pyinotify`
    - Exit and Save
- Under `make busybox-menuconfig`
    - `fatattr`
    - `mkdosfs`
    - Exit and Save

## Enable ChaosDrive overlay

- Under `make menuconfig`
    - In *System Configuration*, change *Root filesystem overlay directories* to `board/pocketbeagle/overlay/`

## Make (!?)

Run `make` and see if it completes the build or not.  If it does, and you find `~/buildroot/output/images/sdcard.img` then follow the instructions for using the image located [here](../image).

## Troubleshooting

It's nearly impossible for me to know what may have gone wrong with your build.  But I personally had compilation issues with python 2 and the core gnulib.  Please check [here](package/) for possible solutions.
