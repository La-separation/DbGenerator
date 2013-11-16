#!/usr/bin/python3
# -*- coding: utf-8 -*-

code_coupable_bas_min = [["o"],["a"],["a"],["a","o"],["a"],["i"],["g"],["ii"],["i","a"],["j"],["ii"],["i"],["iii"],["ii"],["a"],["p"],["q"],["i"],["a"],["i","a"],["a","o"],["b"],["e"],["ii"],["i","g","q"],["z"]]

code_coupable_bas_maj = [["II"],["O"],["O","L"],["O"],["L"],["I"],["O"],["II"],["I"],["O"],["II"],["L"],["III"],["II"],["O"],["I"],["Q"],["II"],["O"],["I"],["O"],["V"],["W"],["II"],["I"],["Z"]]

code_coupable_haut_min = [["o"],["h"],["o"],["d"],["o"],["f"],["o"],["h"],["i"],["i"],["ii","h"],["l"],["m"],["o"],["o"],["o"],["o"],["o"],["o"],["t"],["ii"],["ii"],["iii"],["ii"],["ii"],["z"]]

code_coupable_haut_maj = [["A"],["A"],["A","C"],["A"],["A","C"],["C"],["A","C"],["II"],["I"],["I","T"],["II"],["I"],["M"],["A","II"],["A"],["A"],["A"],["A"],["A","C"],["T"],["II"],["II"],["III"],["II"],["II"],["Z"]]

code_centrale = [["A"],["B"],["B"],["B"],["B"],["F"],["B"],["H"],["I"],["J"],["H"],["L"],["M"],["A"],["B"],["P"],["Q"],["A"],["B"],["T"],["U"],["V"],["W"],["H"],["Y"],["Z"]]

output_language = "php" # "js" or "php"
word_list = "input/en_word_list"
db_root = "output/local_db/en"
code_list_file = "output/code_list"
police_list = ["coupable_haut_min","coupable_haut_maj","coupable_bas_maj","coupable_bas_min","centrale"]
