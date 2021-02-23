# HistoImgProcessing
## Full slide to Jpeg
`FullSlidesToJpeg.py`:

+ Create a single jpeg file from an .svs or an .mrxs file, reading independently 8*8=64 independent areas and then pasting them together after reducing each cell by a factor 10.

+ Argument: --inputdir : directory containing the slides
            --outputdir: directory where the jpeg files will be saved.
            
`FullSlidesToJpg.sh`:

Exemple of a bash file.

## Vahadane
`Vahadane.py`: 

Main script to normalize a picture through the Vahadane algorithm.

`HE_NormLNEN.py` to run with `VahanneLNENHE.sh`.

The target tile is a constant given at the begining of the script. 

Normalize all tiles to HE.

**Arg:**
 
--inputdir: Directory where the **tiles** to normalized are saved.
--outputdir : Directory where the **tiles** normalized will be stored.

Note: The inputdir and outputdir will have the same organisation such that:

Expected organisation:

- Main Folder:
    - Sample_id
        - Accept
            - .jpg
        - Reject
            - .jpg
           
