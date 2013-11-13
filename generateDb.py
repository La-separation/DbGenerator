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
	code_list = generateCodeList(lines, police)
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
