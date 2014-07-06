#!/usr/bin/python3
# -*- coding: utf-8 -*-

## import ##
import sys
import time
import math
import os
import pickle
from gi.repository import Gtk
import ftplib
import socket
#bin_dir_path=os.path.realpath(os.path.dirname(sys.argv[0]))
#sys.path.append(os.path.join(bin_dir_path,"src"))
#sys.path.append(os.path.join(bin_dir_path,"src/db_generator"))

if __name__=="__main__":
	os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))

from src.global_var import *
from src.db_generator.word_code import *
from src.db_generator.word_list import *
from src.db_generator.code_list import *
from src.db_generator.write_db import *

## var ##
stop=False

## def ##
def ftp_thread(sender):
	import threading
	thread=threading.Thread(target=ftp_send_php_db)
	thread.start()

def ftp_send_php_db():
	server=server_entry.get_text()
	user=user_entry.get_text()
	passwd=passwd_entry.get_text()
	path=path_entry.get_text()
	db=php_db_chooser.get_filename()
	
	ftp_link = ftplib.FTP(server)
	ftp_link.login(user, passwd)
	print(path)
	ftp_link.cwd(path)
	if french_db_radio.get_active():
		ftp_remove("local_db", ftp_link)
		ftp_link.mkd("local_db")
		ftp_link.cwd("local_db")
	else:
		ftp_remove("local_db_en", ftp_link)
		ftp_link.mkd("local_db_en")
		ftp_link.cwd("local_db_en")
	for elt in os.listdir(db):
		ftp_send(db+"/"+elt, ftp_link)
	ftp_link.quit()
	print("done")
		
def ftp_remove(path, ftp_link):
	Gtk.main_iteration_do(False)
	print("removing : "+path)
	try:
		ftp_link.delete(path)
	except ftplib.error_perm:
		ftp_link.cwd(path)
		for elt in ftp_link.nlst():
			if elt not in [".",".."]:
				ftp_remove(elt, ftp_link)
		ftp_link.cwd("..")
		ftp_link.rmd(path)
	
def ftp_send(path, ftp_link):
	Gtk.main_iteration_do(False)
	print("sending : "+path)
	if os.path.isfile(path):
		ftp_link.storbinary("STOR "+path.split("/")[-1], open(path, "rb"))
	else:
		ftp_link.mkd(path.split("/")[-1])
		ftp_link.cwd(path.split("/")[-1])
		for elt in os.listdir(path):
			ftp_send(path+"/"+elt, ftp_link)
		ftp_link.cwd("..")

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
		
def close_button_file_dialog_chooser_clicked(sender):
	file_chooser_dialog.hide()
	
def save_button_file_dialog_chooser_clicked(sender):
	ipath = file_chooser_dialog.get_filename()
	file_chooser_dialog.hide()
	
	ifile = open(ipath, "w")
	for elt in treeview_list:
		for elt1 in elt:
			ifile.write(elt1+";")
		ifile.write("\n")
	ifile.close()

def search_button_clicked(sender):
	#search_spinner.set_sensitive(True)
	#search_spinner.start()
	
	treeview_list.clear()
	
	word_to_search = search_entry.get_text()
	db_pickle_file = search_db_chooser.get_filename()
	
	ifile = open(db_pickle_file, "rb")
	code_list = pickle.load(ifile)
	ifile.close()
	
	related_words = search_related_words(police_list, police_code_list, code_list, word_to_search)
	if related_words=={}:
		popup_label.set_text("No related words found")
		popup.show()
	else:
		for police in related_words:
			for code in related_words[police]:
				for word in related_words[police][code]:
					treeview_list.append([word, code, police])
				
	expander.set_expanded(False)
	
	#search_spinner.set_sensitive(False)
	#search_spinner.stop()
	
def save_view_button_clicked(sender):
	file_chooser_dialog.set_current_name("saved_view.csv")
	file_chooser_dialog.show_all()

## main ##
if __name__ == "__main__":
	# osx theme
	#if sys.platform=="mac" or sys.platform=="darwin":
		#if os.path.exists("/opt/local/share/themes/Adwaita")==False or os.path.exists("/opt/local/etc/gtk-3.0/settings.ini")==False:
			#os.system("sudo cp -rf \""+os.path.join(bin_dir_path,"opt")+"\" /")
	
	builder = Gtk.Builder()
	builder.add_from_file(os.path.join(bin_dir_path,"gui.glade"))
	
	if os.path.isdir(out_dir) == False:
		os.mkdir(out_dir)
	
	# glade imports
	window = builder.get_object("window")
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()
	
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
	
	search_db_chooser = builder.get_object("search_db_chooser")
	search_db_chooser.set_filename(os.path.join(out_dir, saved_db))
	search_entry = builder.get_object("search_entry")
	#search_spinner = builder.get_object("search_spinner")
	#search_spinner.set_sensitive(False)
	treeview_list = builder.get_object("treeview_list")
	expander = builder.get_object("expander1")
	
	file_chooser_dialog = builder.get_object("file_chooser_dialog")
	
	popup = builder.get_object("popup")
	popup_label = builder.get_object("popup_label")
	
	server_entry = builder.get_object("server_entry")
	server_entry.set_text("gator4154.hostgator.com")
	user_entry = builder.get_object("user_entry")
	user_entry.set_text("lasepa")
	passwd_entry = builder.get_object("passwd_entry")
	path_entry = builder.get_object("path_entry")
	path_entry.set_text("/public_html/beta/API")
	php_db_chooser = builder.get_object("php_db_chooser")
	php_db_chooser.set_filename("output/php_db")
	french_db_radio = builder.get_object("french_db_radio")
	english_db_radio = builder.get_object("english_db_ratio")
	ftp_label = builder.get_object("ftp_label")
	
	handler_list = {
		"launch_button_clicked" : launch_button_clicked,
		"stop_button_clicked" : stop_button_clicked,
		"popup_close_button_clicked" : popup_close_button_clicked,
		"saved_db_checkbox_toggled" : saved_db_checkbox_toggled,
		"close_button_file_dialog_chooser_clicked" : close_button_file_dialog_chooser_clicked,
		"save_button_file_dialog_chooser_clicked" : save_button_file_dialog_chooser_clicked,
		"search_button_clicked" : search_button_clicked,
		"save_view_button_clicked" : save_view_button_clicked,
		"ftp_send_button_clicked" : ftp_thread
	}
	builder.connect_signals(handler_list)
	
	Gtk.main()