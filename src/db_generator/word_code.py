#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import os

## var ##


## def ##
def import_police_code_list():
	"""retrieve police_code_list from the files in res/police_code"""
	
	from global_var import police_list, police_list_dir
	
	global police_list
	police_code_list = []
	
	for elt in police_list:
		ifile = open(os.path.join(police_list_dir,"code_"+elt+".txt"), "r")
		lines = ifile.read().split("\n")
		
		i = 0
		while i < len(lines):
			if lines[i] != "":
				lines[i] = lines[i].split(":")
				temp = lines[i][1].split(",")
				del(lines[i][1])
				for elt1 in temp:
					lines[i].append(elt1)
				i+=1
			else:
				del(lines[i])
			
		police_code_list.append(lines)
		
		ifile.close()
	
	return police_code_list
	
def word_code(word, police, police_code_list):
	"""generate all possible codes of a word in a police based on police_code_list"""
	
	from global_var import police_list
	
	word_codes = [""]
	police_nb = police_list.index(police)
	
	for letter in word:
		
		i=0
		found = False
		while i < len(police_code_list[police_nb]) and found == False:
			if police_code_list[police_nb][i][0] == letter:
				letter_codes = police_code_list[police_nb][i]
				found = True
			i+=1
			
		old_len = len(word_codes)
		word_codes = word_codes*(len(letter_codes)-1)
		i=0
		j=1
		
		while i < len(word_codes):
			word_codes[i] += letter_codes[j]
			if (i+1)%old_len == 0:
				j+=1
			i+=1
	
	return word_codes