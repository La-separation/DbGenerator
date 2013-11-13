#!/usr/bin/python3
# -*- coding: utf-8 -*-

from var import *
from functions import *
import time
import os

itime = time.time()
lines = readDicFile()

if os.path.exists(db_root) == True and os.path.isfile(db_root) == True:
	os.remove(db_root)

ifile = open(db_root,"w")

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
	writeDb(code_list, police, ifile)
	
ifile.write("\n"+"scriptLoaded('"+db_root+"');")
ifile.close()
print("done")
print(str(int(time.time())-int(itime))+"s")
