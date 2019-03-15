# -*- coding:utf-8 -*-

import sys

with open(sys.argv[1]) as f:
    out = open(sys.argv[2], 'w')
    for line in f:
        count = 0
        for ch in line:
            if ch == ' ':
                count += 1
        line = line.strip(' ')
        out.write(' ' * (count / 2) + line)

print "OK"
