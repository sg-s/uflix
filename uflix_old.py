#! /usr/bin/env python
# uflix.py


import configparser
import os 
from os import listdir
from guessit import guessit
from os.path import isfile, join
import Cocoa
import sys


# read config file 
cf = configparser.RawConfigParser()   
configFilePath = r'config.txt'
cf.read(configFilePath)
movies_path = cf.get('uflix-config', 'movies_path')
bad_file_strings = cf.get('uflix-config', 'bad_file_strings')
bad_strings = cf.get('uflix-config', 'bad_strings')


print(sys.argv[1])


# this is a simpler bit -- just make sure every file is in a folder 
onlyfiles = [f for f in listdir(movies_path) if isfile(join(movies_path, f))]
# remove dot files
onlyfiles = [f for f in onlyfiles if not f[0] == '.']
allowed_ext = ['mp4','mkv','avi','mov','divx','xvid','m4v','mpg','mpeg']
# if these files have an extention that is in the list, make a folder with a cleaned 
# up name, and move it into it. if this folder already exists, then no worries -- move i
# in anyway
bad_title = []
bad_year = []
for i in range(0, len(onlyfiles)):
    this_file = onlyfiles[i]
    ok = False
    for j in range(0, len(allowed_ext)):
        if onlyfiles[i].find(allowed_ext[j]) > 0:
            ok = True
    if not ok:
        continue
        
    # clean up name
    g = guessit(this_file)
    
    new_name = this_file
    if ("year" in g.keys() and "title" in g.keys()):
        new_name = g['title'] + " (" + str(g['year']) + ")"
    elif ("title" in g.keys()):
        bad_year.append(this_file)
        new_name = g['title']
    else:
        bad_title.append(this_file)
    
    print(new_name)
    
    # check if this folder exists 
    folder_path = os.path.join(movies_path,new_name)
    new_full_path = os.path.join(folder_path, onlyfiles[i])
    old_full_path = os.path.join(movies_path,onlyfiles[i])
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
        
    # move this file into this directory
    os.rename(old_full_path,new_full_path)
    