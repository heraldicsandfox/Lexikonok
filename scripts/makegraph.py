#!/usr/bin/env python3
from itertools import combinations
from sys import argv
from parse import statistics


FWARD,BWARD = 1,-1

def graph(tfile,ofile):
	prob, prob2 = statistics(tfile)
	for l,r in combinations((k for k in prob.keys()), 2):
		w = sum(min(prob2[l][dir][w],prob2[r][dir].get(w,0)) for dir in (FWARD,BWARD) for w in prob2[l][dir].keys())
		if w:
			print("%s\t%s\t%f" % (l,r,w),file=ofile)

graph(open(argv[1],'r'),open(argv[2],'w'))

