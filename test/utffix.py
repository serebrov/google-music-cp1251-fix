#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

def writeLine(file, line, encoder):
    try:
        enc = encoder(line)
    except:
        out.write('[?] '+line)
        print '?'
        return

    try:
        out.write(enc)
    except:
        out.write('[-] '+line)

    try:
        print '+'+enc
    except:
        print '-'

wrong = "ÍÎÃÓ ÑÂÅËÎ"
right = "НОГУ СВЕЛО"

table = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
tableW= ""  #+0350 (848)


out = open("not-bug.txt", "w")
for line in ( open ('bug.txt','r')):
    #writeLine(out, line, lambda line: line)
    #writeLine(out, line, lambda line: line.encode('utf-8'))
    #writeLine(out, line, lambda line: line.encode('cp1251'))
    #writeLine(out, line, lambda line: line.decode('utf-8'))
    #writeLine(out, line, lambda line: line.decode('cp1251'))
    #writeLine(out, line, lambda line: unicode(line.encode('utf-8'), 'cp1251'))
    #writeLine(out, line, lambda line: unicode(line.encode('cp1251'), 'utf-8'))
    #writeLine(out, line, lambda line: unicode(line.decode('utf-8'), 'cp1251'))
    #writeLine(out, line, lambda line: unicode(line.decode('cp1251'), 'utf-8'))
    ln = u'';
    lnOrd = '';
    for c in line.decode('utf-8'):
        lnOrd = lnOrd + str(ord(c))
        if (ord(c) >= 0xC0 and ord(c)<=0xFF):
            c = unichr(ord(c)+0x350)
            lnOrd = lnOrd + '->' + str(ord(c))+'|'
        else:
            lnOrd = lnOrd + '|'
        ln = ln + c
    out.write(lnOrd + ln.encode('utf-8'))
    #writeLine(out, ln, lambda line: ln)