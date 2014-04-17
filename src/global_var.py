#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import sys
import os
from word_code import *

## var ##
bin_dir_path=os.path.realpath(os.path.dirname(sys.argv[0]))
police_list = ["centrale","coupable_bas_maj","coupable_haut_maj","coupable_bas_min","coupable_haut_min"]
js_db = "js_db.js"
php_db = "php_db"
word_list_dir = os.path.join(bin_dir_path, "res", "word_list")
police_list_dir = os.path.join(bin_dir_path, "res", "police_code")
out_dir = os.path.join(bin_dir_path, "output")
police_code_list = import_police_code_list()