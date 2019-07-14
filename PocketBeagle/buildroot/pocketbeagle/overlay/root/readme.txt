Welcome to Chaos Drive!

If you booted this drive up for the first time and made it here, congrats!  
The following steps will get your Chaos Drive POC up and running.

These steps will result in a working Chaos Drive with the default reveal and squawk functions working

1: Increase the size of the partition containing this file structure to 
something over 2 GB.  This needs to be done using another host that can read
the sdcard.  I use gparted on Kali.  Reboot the drive when finished

2: Run "/etc/chaos/bfmake.sh /etc/chaos/backing/public.bin"

3: Run "/etc/chaos/bfmake.sh /etc/chaos/backing/secret.bin"

4: Ensure /mnt/chaos and /mnt/secret directories exist

5: Copy /etc/chaos/S60chaosdrive_run.sh to /etc/init.d: "cp /etc/chaos/S60chaosdrive_run.sh /etc/init.d"
   Remove /etc/init.d/S50chaosdrive_initial.sh: "rm /etc/init.d/S50chaosdrive_initial.sh"
   sync to ensure file changes are set: "sync"
   This will start Chaos Drive on the next reboot
   
6: Power cycle the board

7: You should get a 1 GB USB drive presented on the host
   - Activate reveal by placing a file named "revelio" with the word "loki" on 
     the first line on the root of the USB drive
   - Activate squawk by placing a file named "swordfish" on the root of
     the USB drive
   - The default setting includes debug logging, which generates a lot of logs
     You'll need to edit "/etc/init.d/S60chaosdrive_run.sh" and remove the 
     "-d" after chaosDrive_pb.py on line 18.

Due to the way I implemented squawk, you will have to power cycle the device if
you exit the terminal (basically no getty service, just a one off)

Enjoy!

Mike
@miketofet
July 2019
  