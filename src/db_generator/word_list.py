#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##


## var ##


## def ##
def import_word_list(ipath):
	"""import word_list from a dictionnary file"""
	ifile = open(ipath, "r")
	lines = ifile.read().lower().split("\n")
	i=0
	while i < len(lines):
		if lines[i] == "":
			del(lines[i])
		else:
			i+=1
	return lines