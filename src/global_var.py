#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import sys
import os
from src.db_generator.word_code import *

## var ##
#bin_dir_path=os.path.realpath(os.path.dirname(sys.argv[0]))
bin_dir_path=''
js_db = "js_db.js"
php_db = "php_db"
saved_db = "saved_db.pickle"
word_list_dir = os.path.join(bin_dir_path, "res", "word_list")
police_list_dir = os.path.join(bin_dir_path, "res", "police_code")
out_dir = os.path.join(bin_dir_path, "output")
police_list = import_police_list()
police_code_list = import_police_code_list()