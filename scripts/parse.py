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

def markov2(m, counts, groups):
	FWARD, BWARD = 1, -1
	recounts = {}
	for l in counts.keys():
		if l not in recounts:
			recounts[l] = {FWARD:{},BWARD:{}}
		sl = groups.get(l,l)
		for r in m.get(l,{}).keys():
			sr = groups.get(r,r)
			if r not in recounts:
				recounts[r] = {FWARD:{},BWARD:{}}
			recounts[l][FWARD][sr] = recounts[l][FWARD].get(sr,0) + m[l][r] / counts[l]
			recounts[r][BWARD][sl] = recounts[r][BWARD].get(sl,0) + m[l][r] / counts[r]
	return recounts

def statistics(tfile,gfile=None):
	if gfile:
		groups = dict((val,i) for (i,line) in enumerate(gfile) for val in line.split())
	else:
		groups = {}
	text = [structure(s) for s in sentences(tfile)]
	prob = markov(text)
	counts = Counter(w.lower() for s in text for w in s)
	counts[None] = len(text)
	prob2 = markov2(prob, counts, groups)
	return prob, prob2

