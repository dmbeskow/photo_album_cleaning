#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 11:36:46 2021

@author: dbeskow
"""


import glob, progressbar
from PIL import Image
import imagehash
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

#%%
path = "."
files = []
for root,d_names,f_names in os.walk(path):
	for f in f_names:
		files.append(os.path.join(root, f))
        
#%%
suffixes = ['.jpg','.JPG','.jpeg','.JPEG', '.bmp', '.PNG','.png']
fnames = []
for suffix in suffixes:
    fnames = fnames + [x for x in files if x.endswith(suffix)]
    
#%%
hash = imagehash.phash(Image.open(files[0]))
print(hash)
#%%

# I reversed the original intent here in order to create dictionary of exact duplicates
duplicates = {}
bar = progressbar.ProgressBar()
for file in bar(files):
    try:
        h = imagehash.phash(Image.open(file))
        if str(h) in duplicates:
            duplicates[str(h)].append(file)
        else:
            duplicates[str(h)] = [file]
    except:
        continue
 

#templates = {}
#files = glob.glob('template/*')
#bar = progressbar.ProgressBar()
#for file in bar(files):
#    try:
#        h = imagehash.phash(Image.open(file)).hash.flatten()
#        templates[file] = h
#    except:
#        continue
#    
#%%   
from shutil import copyfile

for file in files:
    new_path = os.path.split(file)[1]
    copyfile(file, 'temp/' + new_path)    
    
    
    
    
#%%
#import pickle
#with open('phash_template.p', 'wb') as outfile:
#    pickle.dump(templates, outfile)
with open('phash_template.p', 'rb') as infile:
    templates = pickle.load(infile)
#%%
k = list(templates.keys())
t = list(templates.values())
from sklearn.metrics import pairwise_distances
dists = pairwise_distances(hash.hash.flatten().reshape((1, -1)),t, metric = 'hamming', n_jobs = -1) * 64

#%%
def query(file, n = 1):
    print('Query Image')
    print('-----------')
    q = cv2.imread(file)
    imgplot = plt.imshow(q)
    plt.show()
    
    hash = imagehash.phash(Image.open(file))
    dists = pairwise_distances(hash.hash.flatten().reshape((1, -1)),t, metric = 'hamming', n_jobs = -1) * 64
    top_indices = np.argsort(dists[0])[:n]#[::-1]
    print(top_indices)
    for item in top_indices:
        print('Match file', k[item])
        print('Distance:', dists[0,item])
        temp = cv2.imread(k[item])
        imgplot = plt.imshow(temp)
        plt.show()
#%%
f = files[0]
query(f, n = 10)     
#%% 
f = 'sweden/img/1268_20190113-220528.jpg'
query(f, n = 10)     
#%%
def check_file(file):
    hash = imagehash.phash(Image.open(file))
    dists = pairwise_distances(hash.hash.flatten().reshape((1, -1)),t, metric = 'hamming', n_jobs = -1) * 64
    m = np.min(dists)
    return(m < 10)
    
    
sweden = glob.glob('img/*')
#sweden = glob.glob('sweden/us_election/sample_img/*')
final = []
bar = progressbar.ProgressBar()
for file in bar(sweden):
    try:
        final.append(check_file(file))
    except:
        final.append(False)