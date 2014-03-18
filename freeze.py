#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import sys
from cx_Freeze import setup, Executable
sys.path.append("src")
sys.path.append("src/db_generator")

base = None
if sys.platform == "win32":
	base = "Win32GUI"

## cx_freeze ##
executables = [
 	Executable("DbGenerator.py", base=base)
]

buildOptions = dict(
	compressed = False,
	includes = ["gi", "global_var", "utilities", "word_code", "word_list", "code_list", "write_db"],
	packages = ["gi", "global_var", "utilities", "word_code", "word_list", "code_list", "write_db"]
)

setup(
	name = "cx_freeze executable",
	version = "1.0",
	description = "python3 + GTK3",
	options = dict(build_exe = buildOptions),
	executables = executables
)

# build with "python3 freeze.py build" or "./freeze.py build"