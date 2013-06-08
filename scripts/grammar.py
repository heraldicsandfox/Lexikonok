#!/usr/bin/env python3
from sys import argv, stdin
from re import findall, split

def grouper(it, n, merge=tuple):
        result = []
        for k,i in enumerate(it):
                result.append(i)
                if (k + 1) % n == 0:
                        yield merge(result)
                        result = []

def sentences(file):
        last = ''
        for line in file:
                line = split("([.?!])", line)
                line[0] = last + line[0]
                last = line[-1]
                yield from grouper(line, 2, merge="".join)
        yield last

def structure(s):
        return tuple(findall("(?:[a-zA-Z0-9']+)|\S", s))

groups = dict((val,i) for (i,line) in enumerate(open(argv[1],'r')) for val in line.split())
text = [structure(s) for s in sentences(open(argv[2],'r'))]

srep = set(tuple(groups.get(w.lower(),w.lower()) for w in line) for line in text)




