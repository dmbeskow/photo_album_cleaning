#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 19:46:40 2021

@author: dbeskow
"""

import os
import progressbar
path = "."
from pathlib import Path
import hashlib
#%%

if not os.path.exists('0temp'):
    os.makedirs('0temp')

def file_as_bytes(file):
    with file:
        return file.read()
    
    
def get_md5(file):
    '''
    This function returns the md5 hash of a file
    '''
    h = hashlib.md5(file_as_bytes(open(file, 'rb'))).hexdigest()
    return(h)
#%%

files = []
for root,d_names,f_names in os.walk(path):
	for f in f_names:
		files.append(os.path.join(root, f))
        
        
#%%
# I reversed the original intent here in order to create dictionary of exact duplicates
duplicates = {}
bar = progressbar.ProgressBar()
for file in bar(files):
    try:
        h = get_md5(file)
        if str(h) in duplicates:
            duplicates[str(h)].append(file)
        else:
            duplicates[str(h)] = [file]
    except:
        continue

#%%
not_found = []
bar = progressbar.ProgressBar()
for file in bar(files):
    try:
        h = get_md5(file)
        if str(h) in duplicates:
            continue
        else:
            not_found.append(file)
    except:
        continue
    
#%%
for file in not_found:
    root, file_name = os.path.split(file)
    new_path = '../not_found/' + file_name
    print(file, '----->', new_path)
    os.rename(file, new_path)