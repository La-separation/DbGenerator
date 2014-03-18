#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##


## var ##


## def ##
def recursive_rmdir(idir):
	""" remove a directory and its content """
	import os
	
	ilist = os.listdir(idir)
	for elt in ilist:
		if os.path.isdir(idir+"/"+elt)==True:
			recursive_rmdir(idir+"/"+elt)
		else:
			os.remove(idir+"/"+elt)
	os.rmdir(idir)

def first_letters(istr, lim=1):
	""" return the two first letters of a string """
	i=0
	first_letters=""
	while i < lim and i < len(istr):
		first_letters+=istr[i]
		i+=1
	return first_letters