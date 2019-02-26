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


class uflix(BetterObjects):

	# define the path where you want uflix to operate in 
	movies_path = []
	tv_shows_path = []
	internet_videos_path = []

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



	def make_virtual_copy(self, copy_these, to_these):
		"""makes a copy of the movies dir, with 0 byte files

		useful for testing what uflix does on dummy data without
		touching your actual data
		"""

		if copy_these[-1] == '/':
			copy_these = copy_these[:-1]

		# get all files and folders
		allfiles = glob.glob(copy_these + '/**/*',recursive=True)


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
 

