#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Simple example alchemy script
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
