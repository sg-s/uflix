# uflix.py 
# uflix is a python class to help you organize
# and enjoy your legally acquired video content 
# 
# Srinivas Gorur-Shandilya

import os
import stat
import io
import re
import glob
import time
import subprocess
import configparser
from guessit import guessit
import shutil
from fuzzywuzzy import process, fuzz
import pandas
from bisect import bisect_left 
import hashlib
import sys



class uflix():

	# define the path where you want uflix to operate in 
	movies_path = []
	tv_shows_path = []
	internet_videos_path = []
	virtual_copy_path = []
	allowed_ext = []

	# stores a list of movies from IMDB
	imdb_movies = []
	imdb_movies_year = []

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
 



	def clean(self, dry_run = False):
		'''Clean all file and folder names
		'''


		self.import_movie_list_from_imdb()

		if dry_run:

			print('Running in dry_run mode...')

			if not self.virtual_copy_path:
				raise ValueError('virtual_copy_path not set')

			self.movies_path = self.virtual_copy_path

		#else:
			# raise ValueError('not coded when dry_run is false')


		self.move_single_files_into_folders()

		self.clean_up_folder_names()


	def import_movie_list_from_imdb(self):
		'''reads out movies from imdb'''

		if self.imdb_movies:
			return

		print("[uflix] Importing list of movies from IMDB...")
		p = pandas.read_csv('imdb.tsv',sep='\t',usecols=[1,2,5])
		ismovie = p['titleType']=='movie'
		movies = p[ismovie]
		movies.sort_values(by=['primaryTitle'])
		self.imdb_movies = movies.primaryTitle.tolist()
		self.imdb_movies_year = movies.startYear.tolist()

	def resolve_name_from_imdb(self, name):
		'''resolves name from list of names using
		fuzzy string matching'''

		this_letter = name[0]
		a = bisect_left(self.imdb_movies,this_letter)
		next_letter = chr(ord(this_letter)+1)
		z = bisect_left(self.imdb_movies,next_letter)

		if a != 0 and z != 0 and z > a:
			imdb_name, score = process.extractOne(name,self.imdb_movies[a:z])

			# figure out the year too
			idx = self.imdb_movies.index(imdb_name)
			year = self.imdb_movies_year[idx]

			if score == 100:
				return (imdb_name, score, year)

		print("Could not get an exact match, will perform a full search...")

		imdb_name, score = process.extractOne(name,self.imdb_movies,scorer=fuzz.token_sort_ratio)

		# figure out the year too
		idx = self.imdb_movies.index(imdb_name)
		year = self.imdb_movies_year[idx]

		return (imdb_name, score, year)


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


	def md5sum(self,filename):
		BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
		md5 = hashlib.md5()
		with open(filename, 'rb') as f:
			while True:
				data = f.read(BUF_SIZE)
				if not data:
					break
				md5.update(data)
		return md5.hexdigest()


	def search(self, name):
		'''searches list of movies for a movie'''

		movies_path = self.movies_path;

		onlyfolders = [f for f in os.listdir(movies_path) if os.path.isdir(os.path.join(movies_path, f))]

		results = process.extractBests(name,onlyfolders)
		for result in results:
			print(result[0])

	
	def mergefolders(self,root_src_dir, root_dst_dir):
	    for src_dir, dirs, files in os.walk(root_src_dir):
	        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
	        if not os.path.exists(dst_dir):
	            os.makedirs(dst_dir)
	        for file_ in files:
	            src_file = os.path.join(src_dir, file_)
	            dst_file = os.path.join(dst_dir, file_)
	            if os.path.exists(dst_file):
	            	# are the source and destination the same?
	            	source_hash = self.md5sum(src_file)
	            	dest_hash = self.md5sum(dst_file)
	            	if source_hash == dest_hash:
	            		return
	            	else:
	                	os.remove(dst_file)
	            shutil.copy(src_file, dst_dir)


	def list(self):
		'''prints out a list of all missing movies'''
		movies_path = self.movies_path;

		onlyfolders = [f for f in os.listdir(movies_path) if os.path.isdir(os.path.join(movies_path, f))]

		for folder in onlyfolders:
			if not os.listdir(os.path.join(movies_path,folder)):
				print(folder)


	def add(self, name):
		'''adds a new movie and makes an empty folder to hold it'''
		full_path = os.path.join(self.movies_path, name)
		if not os.path.isdir(full_path):
			os.mkdir(full_path)



	def make_cli(self):
		'''make a copy of this script that is 
		callable from the command line'''

		f = open(sys.argv[0], "r")
		contents = f.readlines()
		f.close()

		hashbang = '#!'+sys.executable

		contents.insert(0, hashbang)

		outfile = sys.argv[0]
		outfile = outfile.replace('.py','')

		f = open(outfile, "w")
		contents = "".join(contents)
		f.write(contents)
		f.close()


		st = os.stat(outfile)
		os.chmod(outfile, st.st_mode | stat.S_IEXEC)

	def clean_up_folder_names(self):
		'''clean up folder names using guessit'''

		print("Cleaning up folder names...")

		movies_path = self.movies_path;

		onlyfolders = [f for f in os.listdir(movies_path) if os.path.isdir(os.path.join(movies_path, f))]

		for folder_name in onlyfolders:


			try:

				# is it already in an acceptable format? 
				# check for (YYYY) in the name
				if folder_name.find('(') > 0 and folder_name.find(')') > 0:
					a = folder_name.rfind('(')
					z = folder_name.rfind(')')
					YYYY = folder_name[a+1:z]
					if len(YYYY) == 4 and YYYY.isdigit():
						# it's probably OK
						print("[OK] " + folder_name)
						continue


				# we're now working with something that is probably not OK
				g = guessit(folder_name)


				guessit_title = folder_name
				guessit_year = []
				if ("year" in g.keys() and "title" in g.keys()):
					guessit_title = g['title']
					guessit_year = g['year']
				elif ("title" in g.keys()):
					guessit_title = g['title']
				else:
					print("This folder could not be cleaned up by guessit:")
					print(folder_name)
					continue



				# use the guessit-name to search IMDB
				print('\n\n\n')
				print(folder_name)
				# print(guessit_title)
				new_name = ''
				imdb_name, score, imdb_year = self.resolve_name_from_imdb(guessit_title)


				

				if (imdb_name == guessit_title and imdb_year == str(guessit_year)):
					# perfect match
					new_name = imdb_name + ' (' + str(imdb_year) + ')'
					
				elif  (imdb_name == guessit_title and imdb_year != str(guessit_year)):
					# years don't match, so go with guessityear if..
					if guessit_year:
						# use guessit year
						new_name = imdb_name + ' (' + str(guessit_year) + ')'
					elif imdb_year:
						# use imdb year
						new_name = imdb_name + ' (' + str(imdb_year) + ')'
					else:
						print('could not determine year')
					# print('years dont match but titles match')
					# print(imdb_name)
					# print('imdb year = ' + imdb_year)
					# print('guessit year  = ' + str(guessit_year))
				elif (imdb_name != guessit_title):
					print("titles dont match")
					if score == 100:
						print('perfect score on imdb')
						new_name = imdb_name + ' (' + str(imdb_year) + ')'
					else:
						print('Imperfect score: ' + str(score))
						print('imdb_name = ' + imdb_name)
				else:
					print('\nedge case!!!!')
					print('imdb_name = ' + imdb_name)
					print('guessit_name = ' + guessit_title)
					print('score = ' + str(score))
					print('imdb_year = ' + str(imdb_year))
					print('guessit_year = ' + str(guessit_year))

				if new_name:
					print(folder_name + '->' + new_name)
					# rename
					new_full_path = os.path.join(movies_path, new_name)
					old_full_path = os.path.join(movies_path,folder_name)

					# check if this directory already exists
					if os.path.isdir(new_full_path):
						# move everything in this folder to new folder
						self.mergefolders(old_full_path, new_full_path)

						# delete old folder
						shutil.rmtree(old_full_path)

					else:
						os.rename(old_full_path,new_full_path)

			except:
				print("Something went wrong with this folder:")
				print(folder_name)


if __name__ == '__main__':
	u = uflix()

	
		

	if len(sys.argv) > 1:
		verb = sys.argv[1]

	if (verb == "clean"):
		u.clean()
	elif (verb == "make-cli"):
		u.make_cli()
	elif (verb == "search"): 
		name = sys.argv[2]
		u.search(name)
	elif (verb == "add"):
		name = sys.argv[2]
		u.add(name)
	elif (verb == "list"):
		u.list()
	else:
		print('done')


