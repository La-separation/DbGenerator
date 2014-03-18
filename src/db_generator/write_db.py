#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import os

## var ##


## def ##
def write_js_db(code_list, out_dir):
	"""write the JS database --> one unique file"""
	from global_var import js_db
	
	ifile = open(os.path.join(out_dir,js_db), "w")
	
	for police in code_list.keys():
		for length in code_list[police].keys():
			for fletters in code_list[police][length].keys():
				ifile.write("gwc_"+police+"_"+str(length)+"_"+fletters+"=function(code){switch(code){"+"\n")
				for code in code_list[police][length][fletters].keys():
					ifile.write("case'"+code+"'return[")
					i=0
					while i < len(code_list[police][length][fletters][code]):
						if i!=0:
							ifile.write(",")
						ifile.write("'"+code_list[police][length][fletters][code][i]+"'")
						i+=1
					ifile.write("];"+"\n")
				ifile.write("}}"+"\n")
	
	ifile.close()

def write_php_db(code_list, out_dir):
	"""write the PHP database --> multiple files in a dir strucutre"""
	from global_var import php_db
	from utilities import recursive_rmdir
	
	if os.path.isdir(os.path.join(out_dir,php_db)):
		recursive_rmdir(os.path.join(out_dir,php_db))
	os.mkdir(os.path.join(out_dir,php_db))
	
	for police in code_list.keys():
		os.mkdir(os.path.join(out_dir,php_db,police))
		for length in code_list[police].keys():
			os.mkdir(os.path.join(out_dir,php_db,police,str(length)))
			for fletters in code_list[police][length].keys():
				ifile = open(os.path.join(out_dir,php_db,police,str(length),fletters)+".php","w")
				ifile.write("<?php"+"\n")
				ifile.write("function gwc_"+police+"_"+str(length)+"_"+fletters+"($code){switch($code){"+"\n")
				for code in code_list[police][length][fletters].keys():
					ifile.write("case'"+code+"':return array(")
					i=0
					while i < len(code_list[police][length][fletters][code]):
						if i != 0:
							ifile.write(",")
						ifile.write("'"+code_list[police][length][fletters][code][i]+"'")
						i+=1
					ifile.write(");"+"\n")
				ifile.write("default:return array();")
				ifile.write("}}"+"\n")
				ifile.write("?>")
				ifile.close()