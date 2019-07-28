# Host-m4 compilation issues

Basically an update to glibc on my build system borked symbols used by gnulib.  Specifically the `_IO_ftrylockfile` symbol simply doesn't exist.

## Solution:

In `~/buildroot/output/build/host-m4-1.4.18/lib` run `sed -i 's/_IO_ftrylockfile/_IO_EOF_SEEN/g' *.c`

Then replace the `stdio-impl.h` in `~/buildroot/output/build/host-m4-1.4.18/lib` with the one here

`make` from the buildroot root
