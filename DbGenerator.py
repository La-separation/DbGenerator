#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import sys
import time
import math
import os
from gi.repository import Gtk

bin_dir_path=os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.join(bin_dir_path,"src"))
sys.path.append(os.path.join(bin_dir_path,"src/db_generator"))

from global_var import *
from word_code import *
from word_list import *
from code_list import *
from write_db import *

## var ##
stop=False

## def ##
def generate_db(add_to_saved_code_list, write_js, write_php):
	global stop
	
	itime = time.time()
	launch_button.set_sensitive(False)
	stop_button.set_sensitive(True)
	if add_to_saved_code_list and os.path.exists(saved_db_button.get_filename()):
		code_list = import_code_list(saved_db_button.get_filename())
	else:
		code_list = {}
	i=0
	progress = 0
	progressbar.set_fraction(0)
	progressbar_label.set_text("generating database...")
	length = len(word_list)
	gtk_quit=False
	while i < length and gtk_quit==False and stop==False:
		if i%10 == 0:
			gtk_quit=Gtk.main_iteration_do(False)
		if (i/length) >= (progress+0.005):
			progress+=0.005
			progressbar.set_fraction(progress)
		code_list = add_to_code_list(police_code_list, word_list[i], code_list)
		i+=1
	if gtk_quit==False and stop==False:
		progressbar_label.set_text("writing databases...")
		Gtk.main_iteration_do(False)
		save_code_list(code_list, out_dir)
		if write_js:
			write_js_db(code_list, out_dir)
		if write_php:
			write_php_db(code_list, out_dir)
		progressbar_label.set_text("done, execution time : "+str(math.ceil(time.time()-itime))+"s")
		progressbar.set_fraction(1)
	elif stop==True:
		progressbar_label.set_text("aborted")
		stop=False
	launch_button.set_sensitive(True)
	stop_button.set_sensitive(False)
	
def launch_button_clicked(sender):
	global word_list
	global out_dir
	
	word_list_file = word_list_button.get_filename()
	out_dir = out_dir_button.get_filename()
	write_js = js_checkbox.get_active()
	write_php = php_checkbox.get_active()
	add_to_saved_code_list = saved_db_checkbox.get_active()
	if  word_list_file == None:
		error_popup("Please specify a file containing a list of words before continuing")
	elif out_dir == None:
		error_popup("Please specify an output directory for the database(s)")
	else:
		word_list=import_word_list(word_list_file)
		#thread = Thread(target=generate_db, args=(write_js, write_php))
		#thread.start()
		generate_db(add_to_saved_code_list, write_js, write_php)
	
def popup_close_button_clicked(sender):
	popup.hide()
	
def error_popup(txt):
	popup_label.set_text(txt)
	popup.show_all()
	
def stop_button_clicked(sender):
	global stop
	stop=True
	
def saved_db_checkbox_toggled(sender):
	if sender.get_active() == True:
		saved_db_button.set_sensitive(True)
	else:
		saved_db_button.set_sensitive(False)

## main ##
if __name__ == "__main__":
	# osx theme
	if sys.platform=="mac" or sys.platform=="darwin":
		if os.path.exists("/opt/local/share/themes/Adwaita")==False or os.path.exists("/opt/local/etc/gtk-3.0/settings.ini")==False:
			os.system("sudo cp -rf \""+os.path.join(bin_dir_path,"opt")+"\" /")
	
	builder = Gtk.Builder()
	builder.add_from_file(os.path.join(bin_dir_path,"gui.glade"))
	
	if os.path.isdir(out_dir) == False:
		os.mkdir(out_dir)
	
	# glade imports
	window = builder.get_object("window")
	popup = builder.get_object("popup")
	popup_label = builder.get_object("popup_label")
	progressbar = builder.get_object("progressbar")
	progressbar_label = builder.get_object("progressbar_label")
	js_checkbox = builder.get_object("js_checkbox")
	php_checkbox = builder.get_object("php_checkbox")
	word_list_button = builder.get_object("word_list_button")
	word_list_button.set_filename(os.path.join(word_list_dir,"fr_word_list.txt"))
	out_dir_button = builder.get_object("out_dir_button")
	out_dir_button.set_filename(out_dir)
	launch_button = builder.get_object("launch_button")
	stop_button = builder.get_object("stop_button")
	saved_db_button = builder.get_object("saved_db_button")
	saved_db_button.set_filename(os.path.join(out_dir, saved_db))
	saved_db_checkbox = builder.get_object("saved_db_checkbox")
	
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	
	handler_list = {
		"launch_button_clicked" : launch_button_clicked,
		"stop_button_clicked" : stop_button_clicked,
		"popup_close_button_clicked" : popup_close_button_clicked,
		"saved_db_checkbox_toggled" : saved_db_checkbox_toggled
	}
	builder.connect_signals(handler_list)
	
	Gtk.main()