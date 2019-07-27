#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
badlnk alchemy script for chaosDrive
- Looks on public lun (root only so far), replaces files with appropriately named
  link files
- These link files then call a vbscript that launches the target file and something of
  attacker's desire
"""

import argparse

description = 'Alchemy test for chaosDrive'
parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--publicLUN', type=str)
parser.add_argument('--secretLUN', type=str)

args = parser.parse_args()

print args.publicLUN
print args.secretLUN

f = open(args.publicLUN+"/kilroyWasHere.txt", "w")
f.close()

print "Alchemy test done"
