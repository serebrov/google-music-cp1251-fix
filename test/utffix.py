#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

def writeLine(file, line, encoder):
    try:
        enc = encoder(line)
    except:
        out.write('[?] '+line)
        return

    try:
        out.write(enc)
    except:
        out.write('[-] '+line)


wrong = "ÍÎÃÓ ÑÂÅËÎ"
right = "НОГУ СВЕЛО"

out = open("not-bug.txt", "w")
for line in ( open ('bug.txt','r')):
    writeLine(out, line, lambda line: line)
    writeLine(out, line, lambda line: line.encode('utf-8'))
    writeLine(out, line, lambda line: line.encode('cp1251'))
    writeLine(out, line, lambda line: line.decode('utf-8'))
    writeLine(out, line, lambda line: line.decode('cp1251'))
    writeLine(out, line, lambda line: unicode(line.encode('utf-8'), 'cp1251'))
    writeLine(out, line, lambda line: unicode(line.encode('cp1251'), 'utf-8'))
    writeLine(out, line, lambda line: unicode(line.decode('utf-8'), 'cp1251'))
    writeLine(out, line, lambda line: unicode(line.decode('cp1251'), 'utf-8'))