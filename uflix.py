# uflix.py 
# uflix is a python class to help you organize
# and enjoy your legally acquired video content 
# 
# Srinivas Gorur-Shandilya

import os
import io
import re
import glob
import time
import subprocess
import configparser
from guessit import guessit
from BetterObjects import BetterObjects
import shutil




class uflix():

	# define the path where you want uflix to operate in 
	movies_path = []
	tv_shows_path = []
	internet_videos_path = []
	virtual_copy_path = []
	allowed_ext = []

	# define a set of strings to remove from the folder_name before searching
	bad_strings  = []
	bad_file_strings = []


	def __init__(self):
		"""read the config file and load attributes """
		cf = configparser.RawConfigParser()   
		configFilePath = r'config.txt'
		cf.read(configFilePath)

		movies_path = cf.get('uflix-config', 'movies_path')
		if os.path.exists(movies_path):
			print("Setting movies_path")
			self.movies_path = movies_path
		else:
			raise ValueError('movies_path does not exist. Check your config file')


		tv_shows_path = cf.get('uflix-config', 'tv_shows_path')
		if os.path.exists(tv_shows_path):
			self.tv_shows_path = tv_shows_path
		else: 
			raise ValueError('tv_shows_path does not exist. Check your config file')

		self.internet_videos_path = cf.get('uflix-config', 'internet_videos_path')

		self.bad_file_strings = cf.get('uflix-config', 'bad_file_strings')
		self.bad_strings = cf.get('uflix-config', 'bad_strings')
		self.allowed_ext = cf.get('uflix-config', 'allowed_ext')



	def make_virtual_copy(self, to_these):
		"""makes a copy of the movies dir, with 0 byte files

		useful for testing what uflix does on dummy data without
		touching your actual data
		"""

		print('Making virtual copy...')

		copy_these = self.movies_path

		if copy_these[-1] == '/':
			copy_these = copy_these[:-1]

		# get all files and folders
		allfiles = glob.glob(copy_these + '/**/*',recursive=True)


		to_these = os.path.join(to_these,'virtual_copy')

		self.virtual_copy_path = to_these

		# first make all the folders
		for i in range(0,len(allfiles)-1):
			if os.path.isdir(allfiles[i]):
				new_name = allfiles[i].replace(copy_these,to_these)
				if os.path.isdir(new_name):
					continue
				os.makedirs(new_name)


		# now make empty files 
		for i in range(0,len(allfiles)-1):
			if os.path.isdir(allfiles[i]):
				continue
			new_name = allfiles[i].replace(copy_these,to_these)
			open(new_name,'a').close()
 



	def clean(self, dry_run = True):
		'''Clean all file and folder names
		'''
		if dry_run:

			print('Running in dry_run mode...')

			if not self.virtual_copy_path:
				raise ValueError('virtual_copy_path not set')

			self.movies_path = self.virtual_copy_path

		else:
			raise ValueError('not coded when dry_run is false')




		self.move_single_files_into_folders()

		self.clean_up_folder_names()


	def move_single_files_into_folders(self):
		'''Move all single movie files into folders
		'''
		movies_path = self.movies_path;


		onlyfiles = [f for f in os.listdir(movies_path) if os.path.isfile(os.path.join(movies_path, f))]


		# remove dot files from list
		onlyfiles = [f for f in onlyfiles if not f[0] == '.']
		allowed_ext = self.allowed_ext


		for file in onlyfiles:
			filename, file_extension = os.path.splitext(file)
			file_extension = file_extension.replace('.','')
			if file_extension in self.allowed_ext:
				print(filename)

				# move this into a folder with the same name
				if not os.path.exists(os.path.join(movies_path,filename)):
					os.mkdir(os.path.join(movies_path,filename))

				# now move this file into this folder
				shutil.move(os.path.join(movies_path,file),os.path.join(movies_path,filename,file))

			else:
				print("This extension not allowed:")
				print(file_extension)


		# for i in range(0, len(onlyfiles)):
		# 	this_file = onlyfiles[i]
		# 	ok = False
		# 	for j in range(0, len(allowed_ext)):
		# 		if onlyfiles[i].find(allowed_ext[j]) > 0:
		# 			ok = True
		# 		if not ok:
		# 			continue
		

		# 	# clean up name
		# 	g = guessit(this_file)
	
		# 	new_name = this_file
		# 	if ("year" in g.keys() and "title" in g.keys()):
		# 		new_name = g['title'] + " (" + str(g['year']) + ")"
		# 	elif ("title" in g.keys()):
		# 		bad_year.append(this_file)
		# 		new_name = g['title']
		# 	else:
		# 		bad_title.append(this_file)
		
		# 	print(this_file + '->' + new_name)
		
		# 	# check if this folder exists 
		# 	folder_path = os.path.join(movies_path,new_name)
		# 	new_full_path = os.path.join(folder_path, onlyfiles[i])
		# 	old_full_path = os.path.join(movies_path,onlyfiles[i])
		# 	if not os.path.isdir(folder_path):
		# 		print('making ' + folder_path)
		# 		os.mkdir(folder_path)
		# 		print('making ' + folder_path)
				
		# 	# move this file into this directory
		# 	print('moving: ' + old_full_path + '->' + new_full_path)
		# 	os.rename(old_full_path,new_full_path)
		# 	