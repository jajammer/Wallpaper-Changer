#!/usr/bin/python

import sys

OUTPUT = '/home/james/.idesktop/command.txt'

if len(sys.argv) > 1:
    command = sys.argv[1]
else:
    command = 'none'

with open(OUTPUT,'w') as stream:
    stream.write(command)
