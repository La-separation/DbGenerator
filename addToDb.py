#!/usr/bin/python3
# -*- coding: utf-8 -*-

from var import *
from functions import *
import time
import os

itime = time.time()
lines = readDicFile()

if os.path.exists(db_root+"."+output_language) == True and os.path.isfile(db_root+"."+output_language) == True:
	os.remove(db_root+"."+output_language)

ifile = open(db_root+"."+output_language,"w")

# init code
if output_language == "php":
	ifile.write("<?php"+"\n")

"""
db_root structure:
	gwc_police_length_XX = function(code) { switch(code) {
		case 'XXXXXX': return [[word, freq], ... ];
		...
	}}
	...
	scriptLoaded('#');
"""


for police in police_list:
	code_list = importCodeList(police)
	
	a=1
	for elt in lines: # elt = [word, freq]
		print(str(a)+" : "+elt)
		a+=1
		
		code_list = addToCodeList(elt, code_list, police)
		
	code_list.sort()
	
	saveCodeList(code_list, police)
	if output_language == "js":
		writeJsDb(code_list, police, ifile)
	elif output_language == "php":
		writePhpDb(code_list, police, ifile)
	
# end code
if output_language == "js":
	ifile.write("\n"+"scriptLoaded('"+db_root+"');")
elif output_language == "php":
	ifile.write("?>")
	
ifile.close()
print("done")
print(str(int(time.time())-int(itime))+"s")
