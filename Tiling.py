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
        img  = OpenSlide(filepath)
        sample_id = imgfilename.split(".")[0]
        try:
            os.mkdir(os.path.join(outputdir))
        except:
            print("The Folder already exist")
        try:
            os.mkdir(os.path.join(outputdir, sample_id))
        except:
            print("The Folder for the sample id {} already exist".format(sample_id))
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
                # try:
                img1=img.read_region(location=(x,y), level=0, size=(sz,sz))
                img11=img1.convert("RGB")
                img111=img11.resize((512,512),Image.ANTIALIAS)
                pix = np.array(img111)
                grad=getGradientMagnitude(pix)
                unique, counts = np.unique(grad, return_counts=True)
                mean_ch = np.mean(pix, axis=2)
                bright_pixels_count = np.argwhere(mean_ch > 220).shape[0]
                if counts[np.argwhere(unique<=15)].sum() < 512*512*0.6 and bright_pixels_count <  512*512*0.5 :
                    couple_coords_accepted.append((x,y) )
            # except:
            #     print('error Tiles {}, pos {}, {} '.format(sample_id, x, y  ))
        print("WRITE")
        sample_random_accepted_slides = random.sample(couple_coords_accepted, 100)
        for (x,y) in sample_random_accepted_slides:
            img1=img.read_region(location=(x,y), level=0, size=(sz,sz))
            img11=img1.convert("RGB")
            img111=img11.resize((512,512),Image.ANTIALIAS)
            img111.save( os.path.join(outputdir, sample_id, sample_id + "_" +  str(x) + "_" + str(y) + '.jpg'  ) , 'JPEG', optimize=True, quality=94)
            

def full_pictures_to_tiles(imgfilename, inputdir, outputdir):
    # For TCGA SLIDES
    print(imgfilename, inputdir, outputdir)
    print(os.path.join(inputdir, imgfilename), "\n \n ")
    sample_id = imgfilename.split(".")[0]
    try:
        os.mkdir(os.path.join(outputdir))
    except:
        print("The Folder already exist")
    try:
        os.mkdir(os.path.join(outputdir, sample_id))
    except:
        print("The Folder for the sample id {} already exist".format(sample_id))

    if imgfilename.find(".svs") != -1 or imgfilename.find("mrxs") != -1:
        filepath = os.path.join(inputdir, imgfilename) 
        img  = OpenSlide(filepath)
        if imgfilename.find(".svs") != -1 :
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
    for x in range(1, w, seq):
        for y in range(1, h, seq):
            try:
                img  = OpenSlide(filepath)
                img1=img.read_region(location=(x,y), level=0, size=(sz,sz))
                img11=img1.convert("RGB")
                img111=img11.resize((512,512),Image.ANTIALIAS)
                pix = np.array(img111)
                grad=getGradientMagnitude(pix)
                unique, counts = np.unique(grad, return_counts=True)
                mean_ch = np.mean(pix, axis=2)
                bright_pixels_count = np.argwhere(mean_ch > 220).shape[0]
                if counts[np.argwhere(unique<=15)].sum() < 512*512*0.6 and bright_pixels_count <  512*512*0.5 :
                    print( os.path.join(outputdir, sample_id, sample_id + "_" +  str(x) + "_" + str(y) + '.jpg'  ))
                    img111.save( os.path.join(outputdir, sample_id, sample_id + "_" +  str(x) + "_" + str(y) + '.jpg'  ) , 'JPEG', optimize=True, quality=94)
            except:
                with open('errorReadingSlides.txt', 'a') as f:
                    f.write('\n{}\t{}\t{}'.format(sample_id,x,y))
                #print('error Tiles {}, pos {}, {} '.format(sample_id, x, y  ))
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test set carcinoids for scanners.')
    parser.add_argument('--inputdir', type=str,    help="Input directory where the images are stored")
    parser.add_argument('--outputdir', type=str,    help='output directory where the files will be stored')
    args = parser.parse_args()
    outputdir = args.outputdir
    inputdir = args.inputdir

    nb_l = []
    images_l = []
    all_f = os.listdir(inputdir) # To change main folder

    for f in all_f:
        if f.find(".svs") != -1 or f.find(".mrxs") != -1:
            sample = f.split('.')[0]
            images_l.append(f)
    array_of_args = [(i, inputdir, outputdir) for i in images_l]
    with Pool(80) as p:
      p.starmap(full_pictures_to_tiles, array_of_args)

        # for f in all_f:
    #     if f.find(".svs") != -1 or f.find(".mrxs") != -1:
    #         sample = f.split('.')[0]
    #         nb = sample[3: ] 
    #         nb_l.append(nb)
           
    # print(nb_l, '\n', sorted(nb_l ) , len(nb_l) ) 
    # nb_l = sorted(nb_l)
    # # for f in all_f:
    #     if f.find(".svs") != -1 or f.find(".mrxs") != -1:
    #         sample = f.split('.')[0]
    #         nb = sample[3: ] 
    #         if nb in nb_l[:56]
    #             images_l.append(f)
    #             try:
    #                 os.mkdir(os.path.join(outputdir, sample))
    #             except :
    #                 print('The folder {} already exists.'.format(sample))
            #try:
            #   os.mkdir(os.path.join(outputdir, sample, "Tiles_512_512"))
            #except:
            #    print('The folder {} already exist.'.format(os.path.join(outputdir, sample, "Tiles_512_512")))
    
    # print(images_l, len(images_l) )
    # full_pictures_to_tiles('TNE0544.mrxs', inputdir, outputdir)
    # main_folder  = '/data/gcs/tcgadata/files/DiagnosisSlides/DataExtraction_DataManagement'
    # folder_TCGA_Fully_downloaded = ['TCGA-KICH', 'TCGA-KIRC', 'TCGA-KIRP', 'TCGA-PAAD', 'TCGA-PRAD'] #
    # for folder in os.listdir(main_folder):
    #     if folder in folder_TCGA_Fully_downloaded:
    #         # Go to slide renamed folder
    #         list_svs_files = os.listdir(os.path.join(main_folder, folder, 'SlidesImagesRenamed'))   
    #         inputdir_to_process = os.path.join(main_folder, folder, 'SlidesImagesRenamed')  
    #         try:
    #             os.mkdir(os.path.join(main_folder, folder, "Tiles_512_512"))
    #         except:
    #             print("the folder : {} already exists.".format(os.path.join(main_folder, folder, "Tiles_512_512")))
    #         outputdir_prepro = os.path.join(main_folder, folder, "Tiles_512_512")
    #         array_of_args = [(i, inputdir_to_process, outputdir_prepro) for i in list_svs_files]
    #         with Pool(80) as p:
    #             p.starmap(full_pictures_to_tiles, array_of_args)
       
