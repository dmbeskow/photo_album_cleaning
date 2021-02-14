#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 19:30:40 2021

@author: dbeskow
"""

#%%
import os
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
suffixes = ['.jpg','.JPG','.jpeg','.JPEG','.mp4','.MOV','.AVI', '.bmp', '.pdf', '.MPG','.mov', '.PNG','.png','.avi']

for suffix in suffixes:
    fname = [x for x in files if x.endswith(suffix)]
    #%%
    
    for file in fname:
        root, file_name = os.path.split(file)
        h = get_md5(file)
        new_path = './0temp/' + h + suffix
        print(file, '----->', new_path)
        os.rename(file, new_path)
    
#%%