from __future__ import division
from multiprocessing import Pool
import sys
import os
import argparse
# # necessary to add cwd to path when script run 
# # by slurm (since it executes a copy)
sys.path.append(os.getcwd()) 

import cv2
import numpy as np
from openslide import OpenSlide
from PIL import Image
from resizeimage import resizeimage
import random 

global inputdir
global outputdir


def getGradientMagnitude(im):
    "Get magnitude of gradient for given image"
    ddepth = cv2.CV_32F
    dx = cv2.Sobel(im, ddepth, 1, 0)
    dy = cv2.Sobel(im, ddepth, 0, 1)
    dxabs = cv2.convertScaleAbs(dx)
    dyabs = cv2.convertScaleAbs(dy)
    mag = cv2.addWeighted(dxabs, 0.5, dyabs, 0.5, 0)
    return mag


def random_tiles(imgfilename, inputdir, outputdir):
	print(imgfilename, inputdir, outputdir)
	print(os.path.join(inputdir, imgfilename), "\n \n ")
	if imgfilename.find(".svs") != -1 or imgfilename.find("mrxs") != -1:
		filepath = os.path.join(inputdir, imgfilename)
		sample_id = imgfilename.split(".")[0]
		#try:	
		img  = OpenSlide(filepath)
		if len(os.listdir(os.path.join(outputdir, sample_id))) == 0: 
			print("Sample ID in process   ", sample_id)
			try:
				os.mkdir(os.path.join(outputdir))
			except:
				print("The Folder already exist")
			try:
				os.mkdir(os.path.join(outputdir, sample_id))
			except:
				print("The Folder for the sample id {} already exist".format(sample_id))
				print("HERE")
			if imgfilename.find(".svs") != -1 :
				if str(img.properties.values.__self__.get('tiff.ImageDescription')).split("|")[1] == "AppMag = 40":
					sz=2048
					seq=1748
				else:
					sz=1024
					seq=874
			elif  imgfilename.find("mrxs") != -1:
				if str(img.properties.values.__self__.get("mirax.GENERAL.OBJECTIVE_MAGNIFICATION")) == 20:
					sz=1024
					seq=874
				else: 
					sz=2048
					seq=1748
			[w, h] = img.dimensions
			couple_coords_accepted = []
			for x in range(1, w, seq):
				for y in range(1, h, seq):
					#try:
					img1=img.read_region(location=(x,y), level=0, size=(sz,sz))
					print('img1')
					img11=img1.convert("RGB")
					print('img11')
					img111=img11.resize((512,512),Image.ANTIALIAS)
					print('img111')
					pix = np.array(img111)
					print('pix')
					grad=getGradientMagnitude(pix)
					print('grad')
					unique, counts = np.unique(grad, return_counts=True)
					print('unique')
					mean_ch = np.mean(pix, axis=2)
					print('mean_ch')
					bright_pixels_count = np.argwhere(mean_ch > 220).shape[0]
					print('bright_pixels_count')
					if counts[np.argwhere(unique<=15)].sum() < 512*512*0.6 and bright_pixels_count <  512*512*0.5 :
						couple_coords_accepted.append((x,y))
						img111.save( os.path.join(outputdir, sample_id, sample_id + "_" +  str(x) + "_" + str(y) + '.jpg'  ) , 'JPEG', optimize=True, quality=94)
						print('tiles written ', os.path.join(outputdir, sample_id, sample_id + "_" +  str(x) + "_" + str(y) + '.jpg'  ))
					# except:
					# 	print('error ', x,y)
			# print("WRITE")
			# if len(couple_coords_accepted) > 100:
			# 	sample_random_accepted_slides = random.sample(couple_coords_accepted, 100)
			# else:
			# 	print('len couples accepted  ', len(couple_coords_accepted))
			# 	sample_random_accepted_slides = couple_coords_accepted  
			# for (x,y) in sample_random_accepted_slides:
			# 	img1=img.read_region(location=(x,y), level=0, size=(sz,sz))
			# 	img11=img1.convert("RGB")
			# 	img111=img11.resize((512,512),Image.ANTIALIAS)
			# 	img111.save( os.path.join(outputdir, sample_id, sample_id + "_" +  str(x) + "_" + str(y) + '.jpg'  ) , 'JPEG', optimize=True, quality=94)
			#   print('tiles written ', os.path.join(outputdir, sample_id, sample_id + "_" +  str(x) + "_" + str(y) + '.jpg'  ))
		#except:	
		#	print("sample_ID   ==  ", sample_id)
				

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test set carcinoids for scanners.')
    parser.add_argument('--inputdir', type=str,    help="Input directory where the images are stored")
    parser.add_argument('--outputdir', type=str,    help='output directory where the files will be stored')
    args = parser.parse_args()
    outputdir = args.outputdir
    inputdir = args.inputdir
    images_l = []
    #all_f = os.listdir(inputdir) # To change main folder
    #for f in all_f:
    #    if f.find(".svs") != -1 or f.find(".mrxs") != -1:
    #        images_l.append(f)
    #for f in images_l:
    #    sample = f.split(".")[0]
    #    filepath = os.path.join(outputdir, sample)
    #    if len(os.listdir(filepath)) < 100:
    #        images_l.append(f)		
    #        #print("sample empty ", sample)
    #        #try:
    #        random_tiles(f, inputdir, outputdir)
    #        #except:
    #        #    print("operation failed for file {}".format(f))
    #print(images_l)
    #print(inputdir, '\n', outputdir)
    #array_of_args = [(i, inputdir, outputdir) for i in images_l]
    #with Pool(80) as p:
    #    p.starmap(random_tiles, array_of_args)
    #empty_folder = []
    #with open('empty_files_list.txt', 'r') as f:
    #    empty_folder.append(f.readline())
    #print(empty_folder)
    for element in os.listdir(inputdir):
        c_ele = element.split('.')[0 ]
        try:
            os.mkdir(os.path.join(outputdir, c_ele))
        except:
            print('The folder {} already exists.'.format(c_ele))
        #if len(os.listdir(os.path.join(outputdir, c_ele))) == 0 :
         print(element)
         try:	
             random_tiles(element , inputdir, outputdir)
         except:
             print('Error ', element)
