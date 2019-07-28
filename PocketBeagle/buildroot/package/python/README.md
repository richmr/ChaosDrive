# Python 2 compilation issues

gcc8 does not play well with Python 2.  As if I needed another reminder to stop working in Python 2.

This is a [known issue](https://bugs.python.org/issue33374)

## Solution:

```
cd ~/buildroot/output/build/host-python-2.7.14/include
patch -b < ~/ChaosDrive/PocketBeagle/buildroot/package/python/0035-gcc8-fix.patch
```

Then run the `make` from the buildroot root

I 'think' you can put this patch file in `~/buildroot/board/pocketbeagle/patches/host-python-2.7.14/` and it may patch automagically, but I haven't tested it.
