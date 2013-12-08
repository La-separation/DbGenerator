#!/usr/bin/python3
# -*- coding: utf-8 -*-

from var import *

def recursiveRmdir(idir):
	""" remove a directory and its content """
	import os
	
	ilist = os.listdir(idir)
	for elt in ilist:
		if os.path.isdir(idir+"/"+elt)==True:
			recursiveRmdir(idir+"/"+elt)
		else:
			os.remove(idir+"/"+elt)
	os.rmdir(idir)

def firstLetters(istr, lim=1):
	""" return the two first letters of a string """
	i=0
	first_letters=""
	while i < lim and i < len(istr):
		first_letters+=istr[i]
		i+=1
	return first_letters

def wordCode(word, police):
	"""" generate all possible codes for a word in a font """
	word_codes = [""]
	i=0
	
	ascii = ord("a")
		
	while i < len(word):
		if police == police_list[0]:
			ilist = code_coupable_haut_min[ord(word[i]) - ascii]
		elif police == police_list[1]:
			ilist = code_coupable_haut_maj[ord(word[i]) - ascii]
		elif police == police_list[2]:
			ilist = code_coupable_bas_maj[ord(word[i]) - ascii]
		elif police == police_list[3]:
			ilist = code_coupable_bas_min[ord(word[i]) - ascii]
		elif police == police_list[4]:
			ilist = code_centrale[ord(word[i]) - ascii]
		
		word_codes = word_codes*len(ilist)
		j=1
		k=0
		while j <= len(ilist):
			while k < ((len(word_codes)/len(ilist))*j):
				word_codes[k] = word_codes[k]+ilist[j-1]
				k+=1
			j+=1
		i+=1
	
	return word_codes

def readDicFile():
	""" open and read the dictionnary file """
	ifile = open(word_list, "r")
	lines = ifile.readlines()
	ifile.close()
	i=0
	while i < len(lines) and lines[i]!="":
		lines[i] = lines[i].lower()
		lines[i] = lines[i].replace("\n","")
		#~ lines[i] = lines[i].split(";")
		#~ lines[i][1] = lines[i][1].replace(",",".")
		#~ if len(lines[i]) > 10:
			#~ del(lines[i])
			#~ i-=1
		i+=1
		
	return lines
	
def generateCodeList(lines, police):
	"""
	generate the code_list variable
	code_list structure:
		[[# code length
			[# code's two first letters
				[code, word, word, ...]...
			]...
		]...]
	"""
	code_list=[]
	a=1
	for elt in lines: # elt = word
		print(str(a)+" : "+elt)
		a+=1
		
		code_list = addToCodeList(elt, code_list, police)
		
	return code_list
	
def addToCodeList(elt, code_list, police): # elt = [word, freq]
	"""add a word to code_list"""
	elt_codes = wordCode(elt, police)
	for code in elt_codes:
		added = False
		if len(code_list)!=0:
			# search if code already exists in code_list
			i = 0
			while i < len(code_list) and added == False:
				if len(code_list[i][0][0][0]) == len(code):
					j = 0
					while j < len(code_list[i]) and added == False:
						if firstLetters(code) == firstLetters(code_list[i][j][0][0]):
							k=0
							while k < len(code_list[i][j]) and added == False:
								if code == code_list[i][j][k][0]:
									l=1
									while l < len(code_list[i][j][k]) and added == False:
										if code_list[i][j][k][l] == elt:
											added = True
										l+=1
									if added == False:
										# si le mot n'existe pas deja
										code_list[i][j][k].append(elt)
										added = True
								k+=1
							if added == False:
								# si pas de code identique
								code_list[i][j].append([code, elt])
								added = True
						j+=1
					if added == False:
						# si pas de premieres lettres identiques
						code_list[i].append([[code, elt]])
						added = True
				i+=1
		if added == False:
			code_list.append([[[code, elt]]])
			added = True
			
	return code_list

def saveCodeList(code_list, police):
	"""save code_list var in files with pickle"""
	import pickle
	
	ifile = open(code_list_file+"_"+police,"wb")
	pickle.dump(code_list, ifile)
	ifile.close()
	
def importCodeList(police):
	"""import code_list var from files with pickle"""
	import pickle
	
	ifile = open(code_list_file+"_"+police, "rb")
	code_list = pickle.load(ifile)
	ifile.close()
	
	return code_list
	
def writeJsDb(code_list, police, ifile):
	"""write the JS database --> one unique file"""
	print("writing file "+db_root+"."+output_language+"...")
	i=0
	while i < len(code_list):
		length = len(code_list[i][0][0][0])
		j=0
		while j < len(code_list[i]):
			fletters = firstLetters(code_list[i][j][0][0])
			ifile.write("gwc_"+police+"_"+str(length)+"_"+fletters+"=function(code){switch(code){"+"\n")
			
			k=0
			while k < len(code_list[i][j]):
				code = code_list[i][j][k][0]
				ifile.write("case'"+code+"':return[")
				
				l=1
				while l < len(code_list[i][j][k]):
					if l!=1:
						ifile.write(",")
					ifile.write("'"+code_list[i][j][k][l]+"'")
					l+=1
				
				ifile.write("];"+"\n")
				k+=1
			
			ifile.write("}}"+"\n")
			j+=1
		i+=1

def writePhpDb(code_list, police):
	"""write the PHP database --> multiple files in a dir strucutre"""
	import os
	
	print("writing PHP database...")
	i=0
	while i < len(code_list):
		length = len(code_list[i][0][0][0])
		os.mkdir(db_root+"/"+police+"/"+str(length))
		j=0
		while j < len(code_list[i]):
			fletters = firstLetters(code_list[i][j][0][0])
			ifile = open(db_root+"/"+police+"/"+str(length)+"/"+fletters+".php", "w")
			ifile.write("<?php"+"\n")
			ifile.write("function gwc_"+police+"_"+str(length)+"_"+fletters+"($code){switch($code){"+"\n")
			
			k=0
			while k < len(code_list[i][j]):
				code = code_list[i][j][k][0]
				ifile.write("case'"+code+"':return array(")
				
				l=1
				while l < len(code_list[i][j][k]):
					if l!=1:
						ifile.write(",")
					ifile.write("'"+code_list[i][j][k][l]+"'")
					l+=1
				
				ifile.write(");"+"\n")
				k+=1
			
			ifile.write("default: return array();")
			ifile.write("}}"+"\n")
			ifile.write("?>")
			ifile.close()
			
			j+=1
		i+=1
