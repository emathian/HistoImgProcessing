import os
import cv2
import numpy as np
import pandas as pd
import random



def stats_tiles_data(folder_to_test_set, sample):
    list_tiles = os.listdir(os.path.join(folder_to_test_set, sample))
    #print(list_tiles)
    if len(list_tiles) > 100:
        list_tiles = random.sample(list_tiles,100)
    df_mean_var_channel_tile =  pd.DataFrame( columns=['tileName', 'mean_r', 'meqan_g', 'mean_b', 'var_r', 'var_g', 'var_b'] )
    list_colnames = list(df_mean_var_channel_tile.columns)
    for i in list_tiles:
        try:
            img_tiles = cv2.imread(os.path.join(folder_to_test_set, sample, i))
            rgb_channels = img_tiles.transpose(2,0,1).reshape(3,-1).transpose() 
            mean_channel = np.mean(rgb_channels, 0)
            var_channel = np.var(rgb_channels, 0) 
            res_tile = [i] + list(mean_channel) + list(var_channel)
            row_dict = {list_colnames[i] : res_tile[i] for i in range(len(list_colnames))}  
            df_mean_var_channel_tile = df_mean_var_channel_tile.append(row_dict, ignore_index = True)
        except:
            print(i)
    return df_mean_var_channel_tile


def pick_random_pixels_data(folder_to_test_set, sample):
    list_tiles = os.listdir(os.path.join(folder_to_test_set, sample))
    df_subset_slide =  pd.DataFrame( columns= ['tileName', 'R', 'G', 'B'] )
    list_colnames = list(df_subset_slide.columns)
    for i in list_tiles:
        img_tiles = cv2.imread(os.path.join(folder_to_test_set, sample, i))
        rgb_channels = img_tiles.transpose(2,0,1).reshape(3,-1).transpose() 
        rgb_channels_no_white = np.delete(rgb_channels , np.where(rgb_channels.sum(axis=1) == 0 ), axis =0 ) 
        vector_id = random.sample(range(0, rgb_channels_no_white.shape[0]), 15) 
        rgb_channels_no_white = rgb_channels_no_white[ vector_id, :]
        tiles_name = [[i]] * 15
        matrix_to_add = np.append(tiles_name, rgb_channels_no_white,  axis=1)
        sub_df = pd.DataFrame(matrix_to_add, columns = ['tileName', 'R', 'G', 'B'])
        df_subset_slide = df_subset_slide.append(sub_df)
    return df_subset_slide

if __name__ == "__main__":
    main_folder = "/home/mathiane/ln_LNEN_work_mathian/Tiles_512_512_1stBasth_VahanneNorm_HESHE"
    list_main_folder = os.listdir(main_folder)
    df_main = pd.DataFrame( columns=['tileName', 'R', 'G', 'B'])
    for sample in list_main_folder: 
        #try:
        df_main = df_main.append(stats_tiles_data("/home/mathiane/ln_LNEN_work_mathian/Tiles_512_512_1stBasth_VahanneNorm_HESHE", sample))
        #except:
#             print('operation failed for the sample {}'.format(sample))
    df_main.to_csv('RandomSamplingHEHESVahanne.csv')
