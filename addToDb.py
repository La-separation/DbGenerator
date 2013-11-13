#!/usr/bin/python3
# -*- coding: utf-8 -*-

from var import *
from functions import *
import time
import os

itime = time.time()
lines = readDicFile()

if output_language == "js":
	if os.path.exists(db_root+"."+output_language) == True and os.path.isfile(db_root+"."+output_language) == True:
		os.remove(db_root+"."+output_language)
	
	ifile = open(db_root+"."+output_language,"w")
	for police in police_list:
		code_list = importCodeList(police)
		
		a=1
		for elt in lines:
			print(str(a)+" : "+elt)
			a+=1
			
			code_list = addToCodeList(elt, code_list, police)
			
		saveCodeList(code_list, police)
		writeJsDb(code_list, police, ifile)
	ifile.write("\n"+"scriptLoaded('"+db_root+"');")
	ifile.close()
	
elif output_language == "php":
	if os.path.exists(db_root) == True and os.path.isdir(db_root) == True:
		recursiveRmdir(db_root)
	os.mkdir(db_root)
	
	for police in police_list:
		os.mkdir(db_root+"/"+police)
		code_list = importCodeList(police)
		
		a=1
		for elt in lines:
			print(str(a)+" : "+elt)
			a+=1
			
			code_list = addToCodeList(elt, code_list, police)
		saveCodeList(code_list, police)
		writePhpDb(code_list, police)

print("done")
print(str(int(time.time())-int(itime))+"s")
