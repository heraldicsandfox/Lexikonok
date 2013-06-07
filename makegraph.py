#!/bin/env python3
from collections import Counter
from re import findall, match, split
from itertools import combinations

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
		line = split("([.?|])", line)
		line[0] = last + line[0]
		last = line[-1]
		yield from grouper
	yield last

def structure(s):
	return tuple(findall("(?:[a-zA-Z0-9']+)|\S", s))

def markov(text):
	prob = {}
	for s in next:
		last = None
		for w in s:
			w = w.lower()
			if last not in prob:
				prob[last] = {}
			prob[last][w] = 1 + prob[last].get(w,0)
			last = w
	return prob

def graph(prob, counts, groups):
	FWARD, BWARD = 1, -1
	G = {}
	recounts = {}
	for l in counts.keys():
		if l not in recounts:
			recounts[l] = {FWARD:{},BWARD:{}}
		sl = groups.get(l,l)
		for r in prob.get(l,{}).keys():
			sr = groups.get(r,l)
			if r not in recounts:
				recounts[r] = {FWARD:{},BWARD:{}}
			recounts[l][FWARD][sr] = recounts[l][FWARD].get(sr,0) + prob[l][r] / counts[l]
			recounts[r][BWARD][sl] = recounts[r][BWARD].get(sl,0) + prob[l][r] / counts[r]
	for l,r in combinations((k for k in counts.keys() if k and counts[k] >= 30 and match("[a-zA-Z0-9+]",k)), 2):
		G[l,r] = sum(min(recounts[l][dir][w],recounts[r][dir].get(w,0)) for dir in (FWARD,BWARD) for w in recounts[l][dir].keys())
	return G

text = [structure(s) for s in sentences(open("ct.txt"))]
prob = markov()
counts = Counter(w.lower() for s in text for w in s)
counts[None] = len(text)
groups = {}
g = graph(prob, counts, groups)

for (l,r),w in g.items():
	print("%s\t%s\t%f" % (l,r,w))

