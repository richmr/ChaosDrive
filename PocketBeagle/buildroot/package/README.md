# Package specific help

## Python 2

I had a segmentation fault while compiling Python 2 with GCC 8 (a known problem).  See the Python folder for my solutions

## gnulib

I had the following happen to me after my host updated glibc:

>freadahead.c: In function 'freadahead':
>freadahead.c:92:3: error: #error "Please port gnulib freadahead.c to your platform! Look at the definition of fflush, fread, ungetc on your system, then report this to bug-gnulib."

See the host-m4 folder for my solution
