#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import sys
from cx_Freeze import setup, Executable
#sys.path.append("src")
#sys.path.append("src/db_generator")

base = None
if sys.platform == "win32":
	base = "Win32GUI"

## cx_freeze ##
executables = [
	Executable("DbGenerator.py", base=base)
]

buildOptions = dict(
	compressed = False,
	#includes = ["gi", "global_var", "utilities", "word_code", "word_list", "code_list", "write_db"],
	packages = ["gi", "src.global_var", "src.utilities", "src.db_generator.word_code", "src.db_generator.word_list", "src.db_generator.code_list", "src.db_generator.write_db"],
	include_files = ["res", "gui.glade"],
	include_msvcr = True
)

setup(
	name = "DbGenerator",
	version = "1.0",
	description = "",
	options = dict(build_exe = buildOptions),
	executables = executables
)

# build with "pythonX freeze.py build" or "./freeze.py build"