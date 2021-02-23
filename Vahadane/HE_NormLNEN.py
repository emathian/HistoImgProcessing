import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import spams
import cv2
from PIL import Image
import utils
from vahadane import vahadane
from sklearn.manifold import TSNE
import os
import pandas as pd
import argparse

global inputdir
global outputdir


df_LNEN = pd.read_csv('/home/mathiane/ImgProcessing/Data/Slides_LNEN_CIRC.csv')

directory_target   = '/home/mathiane/ln_LNEN_work_mathian/Tiles512_512'
TARGET_PATH_HE = directory_target + '/TNE0535/'+'TNE0535_8741_106629.jpg'
TARGET_PATH_HES = directory_target + '/TNE0952/'+'TNE0952_15733_17481.jpg'
target_imageHE = utils.read_image(TARGET_PATH_HE)
target_imageHES = utils.read_image(TARGET_PATH_HES)

vhdHES = vahadane(STAIN_NUM=3, LAMBDA1=0.01, LAMBDA2=0.01, fast_mode=0, getH_mode=0, ITER=50)
vhdHES.fast_mode=0;
vhdHES.getH_mode=0;
WtHES, HtHES = vhdHES.stain_separate(target_imageHES)
vhdHES.setWt(WtHES); 
vhdHES.setHt(HtHES); 

vhdHE = vahadane(STAIN_NUM=2, LAMBDA1=0.01, LAMBDA2=0.01, fast_mode=0, getH_mode=0, ITER=50)
vhdHE.fast_mode=0;
vhdHE.getH_mode=0;
WtHE, HtHE = vhdHE.stain_separate(target_imageHE)
vhdHE.setWt(WtHE); 
vhdHE.setHt(HtHE); 

print('\n Sources \n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
## Separate the stain for all images in /Data
parser = argparse.ArgumentParser(description='Test set carcinoids for scanners.')
parser.add_argument('--inputdir', type=str,    help="Input directory where the images are stored")
parser.add_argument('--outputdir', type=str,    help='output directory where the files will be stored')
args = parser.parse_args()
outputdir = args.outputdir
inputdir = args.inputdir
list_images = os.listdir(inputdir)
Images = []
for folder in list_images:
    files = os.listdir(os.path.join(inputdir, folder))
    try:
         os.mkdir(os.path.join(outputdir, folder))
    except:
            print('folder ' , folder, ' already created')
    for f in files:
        if f.find('jpg') != -1:
            sample_id = f.split('.')[0].split(' ')[0].split('_')[0]
            HES_HE = str(list(df_LNEN[df_LNEN.iloc[:,0] == sample_id ].iloc[:,4])[0])
            SOURCE_PATH = os.path.join(inputdir,folder, f)        
            source_image = utils.read_image(SOURCE_PATH)

            if HES_HE == 'HES':
                Ws, Hs = vhdHE.stain_separate(source_image)
                res = vhdHE.SPCN(source_image, Ws, Hs)  
                res =  Image.fromarray(res)                                                           
                res.save( os.path.join(outputdir, sample_id, f ) , 'JPEG', optimize=True, quality=94) # n_Images = len(Images)
            elif HES_HE == 'HE':
                Ws, Hs = vhdHE.stain_separate(source_image)
                res = vhdHE.SPCN(source_image, Ws, Hs)# 
                res =  Image.fromarray(res)#:                                                     []
                res.save( os.path.join(outputdir, sample_id, f ) , 'JPEG', optimize=True, quality=94) 

#for ele in Images:
#    HES_HE = ele[1]
#    sample_id = ele.split('.')[0].split(' ')[0].split('_')[0]
#  
#    SOURCE_PATH = os.path.join(inputdir,sample_id, ele)
#    source_image = utils.read_image(SOURCE_PATH)
#    if HES_HE == 'HES':
#        Ws, Hs = vhdHES.stain_separate(source_image)
#        res = vhdHES.SPCN(source_image, Ws, Hs)
#        os.path.join(outputdir, sample_id, ele )
#        res.save( os.path.join(outputdir, sample_id, ele ) , 'JPEG', optimize=True, quality=94) 
#    elif HES_HE == 'HE':
#        Ws, Hs = vhdHE.stain_separate(source_image)
#        res = vhdHE.SPCN(source_image, Ws, Hs)
#        os.path.join(outputdir, sample_id, ele )
#        res.save( os.path.join(outputdir, sample_id, ele ) , 'JPEG', optimize=True, quality=94) 
#    else:
#        print('error l78 ', ele[0])
#

#









































