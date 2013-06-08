#!/usr/bin/env python3
from collections import Counter
from re import findall, match, split
from itertools import combinations
from sys import argv, stdin, stderr

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

def markov(text):
	prob = {}
	for s in text:
		last = None
		for w in s:
			w = w.lower()
			if last not in prob:
				prob[last] = {}
			prob[last][w] = 1 + prob[last].get(w,0)
			last = w
	return prob

def graph(prob, counts, groups, out):
	global LIMIT
	FWARD, BWARD = 1, -1
	G = {}
	recounts = {}
	for l in counts.keys():
		if l not in recounts:
			recounts[l] = {FWARD:{},BWARD:{}}
		sl = groups.get(l,l)
		for r in prob.get(l,{}).keys():
			sr = groups.get(r,r)
			if r not in recounts:
				recounts[r] = {FWARD:{},BWARD:{}}
			recounts[l][FWARD][sr] = recounts[l][FWARD].get(sr,0) + prob[l][r] / counts[l]
			recounts[r][BWARD][sl] = recounts[r][BWARD].get(sl,0) + prob[l][r] / counts[r]
	for l,r in combinations((k for k in counts.keys()), 2):
		w = sum(min(recounts[l][dir][w],recounts[r][dir].get(w,0)) for dir in (FWARD,BWARD) for w in recounts[l][dir].keys())
		if l == 'me' or r == 'me':
			print(l,r,w)
		if w:
			print("%s\t%s\t%f" % (l,r,w),file=out)
print("Reading '%s'" % argv[1])
text = [structure(s) for s in sentences(open(argv[1]))]
prob = markov(text)
counts = Counter(w.lower() for s in text for w in s)
counts[None] = len(text)
groups = {}
graph(prob,counts,groups,open(argv[2],'w'))


