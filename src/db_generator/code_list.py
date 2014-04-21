#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##


## var ##


## def ##
def add_to_code_list(police_code_list, word, code_list):
	"""
	code_list structure:
		{#police :
			{#code length :
				{#code's two first letters
					{code : [word, word, ...]}...
				}...
			}...
		}
	"""
	
	from global_var import police_list
	from word_code import word_code
	from utilities import first_letters
	
	for police in police_list:
		if code_list.get(police) == None:
			code_list[police] = {}
		
		word_codes = word_code(word, police, police_code_list)
		for code in word_codes:
			length = len(code)
			fl = first_letters(code, 2)
			if code_list[police].get(length) == None:
				code_list[police][length] = {fl:{code:[word]}}
			else:
				if code_list[police][length].get(fl) == None:
					code_list[police][length][fl] = {code:[word]}
				else:
					if code_list[police][length][fl].get(code) == None:
						code_list[police][length][fl][code] = [word]
					else:
						try:
							code_list[police][length][fl][code].index(word)
						except ValueError:
							code_list[police][length][fl][code].append(word)
		
	return code_list
	
def save_code_list(code_list, out_dir):
	"""save code list in a .pickle file"""
	
	import os
	import pickle
	from global_var import saved_db
	
	ifile = open(os.path.join(out_dir,saved_db),"wb")
	pickle.dump(code_list, ifile)
	ifile.close()
	
def import_code_list(ipath):
	"""import code_list from a previously saved .pickle"""
	
	import os
	import pickle
	
	ifile = open(ipath, "rb")
	code_list = pickle.load(ifile)
	ifile.close()
	return code_list