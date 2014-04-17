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