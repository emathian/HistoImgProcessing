from __future__ import division
from multiprocessing import Pool
import sys
import os
import argparse
# # necessary to add cwd to path when script run 
# # by slurm (since it executes a copy)
sys.path.append(os.getcwd()) 
import json
import cv2
import numpy as np
from openslide import OpenSlide
from PIL import Image
from resizeimage import resizeimage
import random 

global inputdir
global outputdir


def get_magnificiance(imgfilename, inputdir):
    sample = imgfilename.split('.')[0]
    print('imgfilename, inputdir')
    if imgfilename.find(".svs") != -1 or imgfilename.find("mrxs") != -1:
        try:
            filepath = os.path.join(inputdir, imgfilename)
            print(filepath)
            img  = OpenSlide(filepath)
        except:
            return(sample, -1)
    if imgfilename.find(".svs") != -1 :
        str_mag = str(img.properties.values.__self__.get('tiff.ImageDescription')).split("|")[1][9:]
        mag = int(str_mag) 
        return (sample, mag)
    if imgfilename.find(".mrxs") != -1 :
        mag = int(img.properties.values.__self__.get("mirax.GENERAL.OBJECTIVE_MAGNIFICATION"))
        return (sample, mag)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test set carcinoids for scanners.')
    parser.add_argument('--inputdir', type=str,    help="Input directory where the images are stored")
    parser.add_argument('--outputdir', type=str,    help='output directory where the files will be stored')
    args = parser.parse_args()
    outputdir = args.outputdir
    inputdir = args.inputdir
    images_l = []
    all_f = os.listdir(inputdir) # To change main folder
    for f in all_f:
       if f.find(".svs") != -1 or f.find(".mrxs") != -1:
           images_l.append(f)
    dict_magnificiance = {}
    for f in images_l:
        sample, mag = get_magnificiance(f, inputdir)
        dict_magnificiance[sample] = mag
    with open('/home/mathiane/DraftScripts/ScriptDownload/Magnificiance.txt', 'w') as f:
        f.write(json.dumps(dict_magnificiance))
 

	# for element in os.listdir(inputdir):
	# 	c_ele = element.split('.')[0]
	# 	if c_ele in empty_folder:
	# 		random_tiles(element , inputdir, outputdir)
