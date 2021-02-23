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



def full_slide_to_jpeg(imgfilename, inputdir, outputdir):
    # For TCGA SLIDES
    #print(imgfilename, inputdir, outputdir)
    #print('in loop')
    sample_id = imgfilename.split(".")[0]
    # try:
    img = OpenSlide(os.path.join(inputdir, imgfilename))
    print('img.dimensions  ', img.dimensions)
    x_0 = img.dimensions[0]
    x_1 = img.dimensions[1]
    y_0 = x_0 // 8
    y_1 = x_1 // 8
    r_0 = x_0 % 8
    r_1 = x_1 % 8
    print('x_0 ', x_0, ' x_1 ', x_1, ' y_0 ', y_0, ' y_1 ', y_1, ' r_0 ', r_0, ' r_1 ', r_1)
    list_coordsx = []
    list_coordsy = []
    for i in range(1,8):
        X = y_0 * (i -1)
        Y = y_1 * (i-1)
        list_coordsx.append(X)
        list_coordsy.append(Y)
    list_coordsx.append(y_0 * 7)
    list_coordsy.append(y_1 * 7)
    
    np_array_f = np.zeros((int(x_0//8/10 * 8  + (x_0 - y_0*7 ) /10),  int(x_1//8/10 * 8  + (x_1 - y_1*7 ) /10) , 3))
    print(np_array_f.shape)
    cx = 0
    for elex in list_coordsx:
        cy = 0
        for eley in list_coordsy:
            ele = (elex, eley)
            if cy < 8 and cx < 8:
                try:
                    img1=img.read_region(location=ele, level=0, size=(y_0 -1 , y_1 - 1 ))
                    img11=img1.convert("RGB")
                    img111=img11.resize((int(round(y_0 / 10)), 
                                            int(round(y_1 / 10))),Image.ANTIALIAS)

                    img111 = np.array(img111).transpose(1,0,2)
                    print('img111 ', img111.shape)
                    np_array_f[int(round(ele[0]/10)):  int(round(ele[0]/10)) + img111.shape[0], 
                                int(round(ele[1]/10)): int(round(ele[1]/10)) + img111.shape[1],:] = img111
                except:
                    with open('errorFullSlides1stBatch_806_2159.txt', 'a') as f:
                        f.write('\n{}\t{}\t{}'.format(sample_id,elex,eley))

            elif cy >= 8 and cx <8:
                try:
                    img1=img.read_region(location=ele, level=0, size=(y_0 -1 , y_1 - 1  + r_1))
                    img11=img1.convert("RGB")
                    img111=img11.resize((int(round(y_0 / 10)), 
                                            int(round(y_1 / 10))),Image.ANTIALIAS)
                    img111 = np.array(img111).transpose(1,0,2)
                    np_array_f[int(round(ele[0]/10)):  int(round(ele[0]/10)) + img111.shape[0], 
                                int(round(ele[1]/10)): ,:] = img111
                except:
                    with open('errorFullSlides1stBatch_806_2159.txt', 'a') as f:
                        f.write('\n{}\t{}\t{}'.format(sample_id,elex,eley))

            
            elif cx >= 8 and cy <8:
                try:
                    img1=img.read_region(location=ele, level=0, size=(y_0 -1  + r_0, y_1 - 1 ))
                    img11=img1.convert("RGB")
                    img111=img11.resize((int(round(y_0 / 10)),   int(round(y_1 / 10))),Image.ANTIALIAS)
                    img111 = np.array(img111).transpose(1,0,2)
                    
                    np_array_f[int(round(ele[0]/10)): ,  
                                    int(round(ele[1]/10)): int(round(ele[1]/10)) + img111.shape[1] ,:] = img111
                except:
                    with open('errorFullSlides1stBatch_806_2159.txt', 'a') as f:
                        f.write('\n{}\t{}\t{}'.format(sample_id,elex,eley))

            else:
                try:
                    img1=img.read_region(location=ele, level=0, size=(y_0 -1 + r_0 , y_1 - 1  + r_1))
                    img11=img1.convert("RGB")
                    img111=img11.resize((int(round(y_0 / 10)), 
                                            int(round(y_1 / 10))),Image.ANTIALIAS)
                    img111 = np.array(img111).transpose(1,0,2)
                    np_array_f[int(round(ele[0]/10)): ,  
                                int(round(ele[1]/10)): ,:] = img111
                except:
                    with open('errorFullSlides1stBatch_806_2159.txt', 'a') as f:
                        f.write('\n{}\t{}\t{}'.format(sample_id,elex,eley))

            cy +=1
        cx += 1
    im = Image.fromarray(np_array_f.astype(np.uint8))
    im.save( os.path.join(outputdir, sample_id + '.jpg'  ) , 'JPEG', optimize=True, quality=94)

    
    #   print('Error with the file : ', sample_id)               
    
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
        if f.find(".mrxs") != -1 or f.find(".svs") != -1:
            sample_id = f.split('.')[0]
            num = int(f.split('.')[0].split('TNE')[-1])
            #print(num)
            outputfilename = sample_id + '.jpg' 
            print(sample_id)
            if num>806 and num<=2159  and outputfilename not in os.listdir(outputdir) and f not in os.listdir('/data/gcs/lungNENomics/work/follm/Images/2nd_batch_LNEN_HES') :
                print('Accept ', num)
                images_l.append(f)
                

    array_of_args = [(i, inputdir, outputdir) for i in images_l]
    with Pool(len(images_l)) as p:
        p.starmap(full_slide_to_jpeg, array_of_args)
